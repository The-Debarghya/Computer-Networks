package main

import (
	"bytes"
	"encoding/binary"
	"fmt"
	"io"
	"net"
	"os"
	"strings"
)

// DNSHeader describes the request/response DNS header
type DNSHeader struct {
	TransactionID  uint16
	Flags          uint16
	NumQuestions   uint16
	NumAnswers     uint16
	NumAuthorities uint16
	NumAdditionals uint16
}

// DNSResourceRecord describes individual records in the request and response of the DNS payload body
type DNSResourceRecord struct {
	DomainName         string
	Type               uint16
	Class              uint16
	TimeToLive         uint32
	ResourceDataLength uint16
	ResourceData       []byte
}

// Type and Class values for DNSResourceRecord
const (
	TypeA                  uint16 = 1 
	ClassINET              uint16 = 1 
	FlagResponse           uint16 = 1 << 15
	UDPMaxMessageSizeBytes uint   = 512 
)

func Write(w io.Writer, data interface{}) error {
	return binary.Write(w, binary.BigEndian, data)
}

func dbLookup(queryResourceRecord DNSResourceRecord) ([]DNSResourceRecord, []DNSResourceRecord, []DNSResourceRecord) {
	var answerResourceRecords = make([]DNSResourceRecord, 0)
	var authorityResourceRecords = make([]DNSResourceRecord, 0)
	var additionalResourceRecords = make([]DNSResourceRecord, 0)

	names, err := GetNames()
	if err != nil {
		return answerResourceRecords, authorityResourceRecords, additionalResourceRecords
	}
	if queryResourceRecord.Type != TypeA || queryResourceRecord.Class != ClassINET {
		return answerResourceRecords, authorityResourceRecords, additionalResourceRecords
	}
	for _, name := range names {
		if strings.Contains(queryResourceRecord.DomainName, name.Name) {
			fmt.Println(queryResourceRecord.DomainName, "resolved to", name.Address)
			answerResourceRecords = append(answerResourceRecords, DNSResourceRecord{
				DomainName:         name.Name,
				Type:               TypeA,
				Class:              ClassINET,
				TimeToLive:         31337,
				ResourceData:       name.Address[12:16], // ipv4 address
				ResourceDataLength: 4,
			})
		}
	}
	if len(answerResourceRecords) == 0 {
		ips, err := net.LookupIP(queryResourceRecord.DomainName)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Could not get IPs: %v\n", err)
			//os.Exit(1)
		}
		for _, ip := range ips {
			fmt.Println(queryResourceRecord.DomainName, "resolved to", ip)
			if ip.To4() != nil {
				answerResourceRecords = append(answerResourceRecords, DNSResourceRecord{
					DomainName:         queryResourceRecord.DomainName,
					Type:               TypeA,
					Class:              ClassINET,
					TimeToLive:         31337,
					ResourceData:       ip[12:16],
					ResourceDataLength: 4,
				})
				WriteNames(Name{
					Name:    queryResourceRecord.DomainName,
					Address: ip,
				})
			}
		}
	}
	return answerResourceRecords, authorityResourceRecords, additionalResourceRecords
}

func readDomainName(requestBuffer *bytes.Buffer) (string, error) {
	var domainName string

	b, err := requestBuffer.ReadByte()

	for ; b != 0 && err == nil; b, err = requestBuffer.ReadByte() {
		labelLength := int(b)
		labelBytes := requestBuffer.Next(labelLength)
		labelName := string(labelBytes)

		if len(domainName) == 0 {
			domainName = labelName
		} else {
			domainName += "." + labelName
		}
	}

	return domainName, err
}

func writeDomainName(responseBuffer *bytes.Buffer, domainName string) error {
	labels := strings.Split(domainName, ".")

	for _, label := range labels {
		labelLength := len(label)
		labelBytes := []byte(label)

		responseBuffer.WriteByte(byte(labelLength))
		responseBuffer.Write(labelBytes)
	}

	err := responseBuffer.WriteByte(byte(0))

	return err
}

func handleDNSClient(requestBytes []byte, serverConn *net.UDPConn, clientAddr *net.UDPAddr) {
	/**
	 * read request
	 */
	var requestBuffer = bytes.NewBuffer(requestBytes)
	var queryHeader DNSHeader
	var queryResourceRecords []DNSResourceRecord

	err := binary.Read(requestBuffer, binary.BigEndian, &queryHeader)

	if err != nil {
		fmt.Println("Error decoding header: ", err.Error())
	}

	queryResourceRecords = make([]DNSResourceRecord, queryHeader.NumQuestions)

	for idx, _ := range queryResourceRecords {
		queryResourceRecords[idx].DomainName, err = readDomainName(requestBuffer)

		if err != nil {
			fmt.Println("Error decoding label: ", err.Error())
		}

		queryResourceRecords[idx].Type = binary.BigEndian.Uint16(requestBuffer.Next(2))
		queryResourceRecords[idx].Class = binary.BigEndian.Uint16(requestBuffer.Next(2))
	}
	/**
	 * lookup values
	 */
	var answerResourceRecords = make([]DNSResourceRecord, 0)
	var authorityResourceRecords = make([]DNSResourceRecord, 0)
	var additionalResourceRecords = make([]DNSResourceRecord, 0)

	for _, queryResourceRecord := range queryResourceRecords {
		newAnswerRR, newAuthorityRR, newAdditionalRR := dbLookup(queryResourceRecord)

		answerResourceRecords = append(answerResourceRecords, newAnswerRR...)
		authorityResourceRecords = append(authorityResourceRecords, newAuthorityRR...)
		additionalResourceRecords = append(additionalResourceRecords, newAdditionalRR...)
	}
	/**
	 * write response
	 */
	var responseBuffer = new(bytes.Buffer)
	var responseHeader = DNSHeader{
		TransactionID:  queryHeader.TransactionID,
		Flags:          FlagResponse,
		NumQuestions:   queryHeader.NumQuestions,
		NumAnswers:     uint16(len(answerResourceRecords)),
		NumAuthorities: uint16(len(authorityResourceRecords)),
		NumAdditionals: uint16(len(additionalResourceRecords)),
	}
	err = Write(responseBuffer, &responseHeader)
	if err != nil {
		fmt.Println("Error writing to buffer: ", err.Error())
	}

	for _, queryResourceRecord := range queryResourceRecords {
		err = writeDomainName(responseBuffer, queryResourceRecord.DomainName)
		if err != nil {
			fmt.Println("Error writing to buffer: ", err.Error())
		}
		Write(responseBuffer, queryResourceRecord.Type)
		Write(responseBuffer, queryResourceRecord.Class)
	}

	for _, answerResourceRecord := range answerResourceRecords {
		err = writeDomainName(responseBuffer, answerResourceRecord.DomainName)
		if err != nil {
			fmt.Println("Error writing to buffer: ", err.Error())
		}
		Write(responseBuffer, answerResourceRecord.Type)
		Write(responseBuffer, answerResourceRecord.Class)
		Write(responseBuffer, answerResourceRecord.TimeToLive)
		Write(responseBuffer, answerResourceRecord.ResourceDataLength)
		Write(responseBuffer, answerResourceRecord.ResourceData)
	}

	for _, authorityResourceRecord := range authorityResourceRecords {
		err = writeDomainName(responseBuffer, authorityResourceRecord.DomainName)
		if err != nil {
			fmt.Println("Error writing to buffer: ", err.Error())
		}
		Write(responseBuffer, authorityResourceRecord.Type)
		Write(responseBuffer, authorityResourceRecord.Class)
		Write(responseBuffer, authorityResourceRecord.TimeToLive)
		Write(responseBuffer, authorityResourceRecord.ResourceDataLength)
		Write(responseBuffer, authorityResourceRecord.ResourceData)
	}

	for _, additionalResourceRecord := range additionalResourceRecords {
		err = writeDomainName(responseBuffer, additionalResourceRecord.DomainName)
		if err != nil {
			fmt.Println("Error writing to buffer: ", err.Error())
		}
		Write(responseBuffer, additionalResourceRecord.Type)
		Write(responseBuffer, additionalResourceRecord.Class)
		Write(responseBuffer, additionalResourceRecord.TimeToLive)
		Write(responseBuffer, additionalResourceRecord.ResourceDataLength)
		Write(responseBuffer, additionalResourceRecord.ResourceData)
	}
	serverConn.WriteToUDP(responseBuffer.Bytes(), clientAddr)
}

func main() {
	serverAddr, err := net.ResolveUDPAddr("udp", "localhost:1053")

	if err != nil {
		fmt.Println("Error resolving UDP address: ", err.Error())
		os.Exit(1)
	}
	serverConn, err := net.ListenUDP("udp", serverAddr)
	if err != nil {
		fmt.Println("Error listening: ", err.Error())
		os.Exit(1)
	}
	fmt.Println("Listening at: ", serverAddr)
	defer serverConn.Close()

	for {
		requestBytes := make([]byte, UDPMaxMessageSizeBytes)
		_, clientAddr, err := serverConn.ReadFromUDP(requestBytes)
		if err != nil {
			fmt.Println("Error receiving: ", err.Error())
		} else {
			fmt.Println("Received request from ", clientAddr)
			go handleDNSClient(requestBytes, serverConn, clientAddr) // array is value type (call-by-value), i.e. copied
		}
	}
}
