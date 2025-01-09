package main

import (
	"crypto/rand"
	"encoding/hex"
	"fmt"
	"os"
)

// dont brute force! read the code, and you'll see how to find the kelp value ;3

func generateKey(length int) ([]rune, error) {
	key := make([]byte, length)
	_, err := rand.Read(key)
	if err != nil {
		return nil, fmt.Errorf("error generating key: %v", err)
	}

	runes := make([]rune, length)
	for i, b := range key {
		runes[i] = rune(b)
	}

	return runes, nil
}

func runeToHex(runes []rune) string {
	return hex.EncodeToString([]byte(string(runes)))
}

func encodeRunes(data, key []rune, kelp int) []rune {
	result := make([]rune, len(data))
	for i := 0; i < len(data); i++ {
		result[i] = (data[i] ^ key[i]) + rune(kelp)
	}
	return result
}

func encodeString(s string, kelp int) (string, error) {
	runeData := []rune(s)
	key, err := generateKey(len(runeData))
	if err != nil {
		return "", fmt.Errorf("error encoding string: %v", err)
	}
	encodedData := encodeRunes(runeData, key, kelp)
	encodedKey := encodeRunes(key, encodedData, kelp)

	finalData := append(encodedData, rune(kelp))
	finalData = append(finalData, encodedKey...)

	return runeToHex(finalData), nil
}

func main() {
	var kelp int
	var note string

	fmt.Print("Enter your kelp: ")
	fmt.Scanln(&kelp)
	fmt.Print("Enter secure note: ")
	fmt.Scanln(&note)

	encodedString, err := encodeString(note, kelp)
	if err != nil {
		fmt.Println("Error encoding string:", err)
		return
	}

	file, err := os.OpenFile("kelpfile", os.O_RDWR|os.O_CREATE|os.O_TRUNC, 0644)
	if err != nil {
		fmt.Println(err)
		return
	}

	defer file.Close()
	if _, err := file.Write([]byte(encodedString)); err != nil {
		fmt.Println(err)
		return
	}
}
