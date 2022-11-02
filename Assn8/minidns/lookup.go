package main

import (
	"encoding/json"
	"fmt"
	"os"
	"net"
)

type DomainName struct {
	Name    string `json:"name"`
	Address string `json:"address"`
}

type Name struct {
	Name    string
	Address net.IP
}

func WriteNames(name Name) error {
	data, err := os.ReadFile("./entries.json")
	if err != nil {
		fmt.Print(err)
		return err
	}
	var models []DomainName
	err = json.Unmarshal(data, &models)
	if err != nil {
		fmt.Print(err)
		return err
	}
	models = append(models, DomainName{
		Name: name.Name,
		Address: name.Address.String(),
	})
	final, err := json.Marshal(models)
	if err != nil {
		fmt.Print(err)
		return err
	}
	err = os.WriteFile("./entries.json", []byte(final), 0777)
	return err
}

func GetNames() ([]Name, error) {
	data, err := os.ReadFile("./entries.json")
	if err != nil {
		fmt.Print(err)
		return nil, err
	}
	var models []DomainName
	err = json.Unmarshal(data, &models)
	if err != nil {
		fmt.Println("error:", err)
		return nil, err
	}
	return To(models), nil
}

func To(models []DomainName) []Name {
	names := make([]Name, 0, len(models))
	for _, value := range models {
		names = append(names, Name{
			Name:    value.Name,
			Address: net.ParseIP(value.Address),
		})
	}
	return names
}