package main

import (
	"encoding/json"
	"fmt"
	"os"
	"net"
)

type Entry struct {
	DomainName    string `json:"name"`
	Address string `json:"address"`
}

type Record struct {
	DomainName    string
	Address net.IP
}

func WriteNames(name Record) error {
	data, err := os.ReadFile("./entries.json")
	if err != nil {
		fmt.Print(err)
		return err
	}
	var entries []Entry
	err = json.Unmarshal(data, &entries)
	if err != nil {
		fmt.Print(err)
		return err
	}
	entries = append(entries, Entry{
		DomainName: name.DomainName,
		Address: name.Address.String(),
	})
	final, err := json.Marshal(entries)
	if err != nil {
		fmt.Print(err)
		return err
	}
	err = os.WriteFile("./entries.json", []byte(final), 0777)
	return err
}

func GetNames() ([]Record, error) {
	data, err := os.ReadFile("./entries.json")
	if err != nil {
		fmt.Print(err)
		return nil, err
	}
	var entries []Entry
	err = json.Unmarshal(data, &entries)
	if err != nil {
		fmt.Println("error:", err)
		return nil, err
	}
	return To(entries), nil
}

func To(entries []Entry) []Record {
	names := make([]Record, 0, len(entries))
	for _, entry := range entries {
		names = append(names, Record{
			DomainName:    entry.DomainName,
			Address: net.ParseIP(entry.Address),
		})
	}
	return names
}