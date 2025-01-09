package main

import (
	"crypto/rand"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"math/big"
	"os"
	"strings"
)

var CharSet = map[rune]string{
	'0': "🐱", '1': "🐈", '2': "😸", '3': "😹",
	'4': "😺", '5': "😻", '6': "😼", '7': "😽",
	'8': "😾", '9': "😿", 'A': "🙀", 'B': "🐱‍👤",
	'C': "🐱‍🏍", 'D': "🐱‍💻", 'E': "🐱‍👓", 'F': "🐱‍🚀",
}

func catify(input string, keys []int) string {
	var keyedText string
	var result string

	for i, char := range input {
		keyedText += string(rune(int(char) + keys[i]))
	}
	fmt.Printf("I2Keyed: %s\n", keyedText)

	hexEncoded := strings.ToUpper(hex.EncodeToString([]byte(keyedText)))
	fmt.Printf("K2Hex: %s\n", hexEncoded)

	for _, rune := range hexEncoded {
		result += CharSet[rune]
	}

	return result
}

func savePair(name, input, output string) {
	inputFile, err := os.OpenFile(name+"_input.txt", os.O_RDWR|os.O_CREATE|os.O_TRUNC, 0644)
	if err != nil {
		fmt.Println(err)
		return
	}
	defer inputFile.Close()

	outputFile, err := os.OpenFile(name+"_output.txt", os.O_RDWR|os.O_CREATE|os.O_TRUNC, 0644)
	if err != nil {
		fmt.Println(err)
		return
	}
	defer outputFile.Close()

	if _, err := inputFile.Write([]byte(input)); err != nil {
		fmt.Println(err)
		return
	}
	if _, err := outputFile.Write([]byte(output)); err != nil {
		fmt.Println(err)
		return
	}
}

func getKeys(length int) []int {
	var keys = []int{}
	keyFileName := fmt.Sprintf("keys_%d.json", length)

	file, err := os.Open(keyFileName)
	if err != nil {

		for i := 0; i < length; i++ {
			num, _ := rand.Int(rand.Reader, big.NewInt(60000))

			keys = append(keys, int(num.Int64()))
		}

		keyFile, err := os.OpenFile(keyFileName, os.O_RDWR|os.O_CREATE|os.O_TRUNC, 0644)
		if err != nil {
			fmt.Println(err)
			return []int{}
		}
		defer keyFile.Close()

		encoded, _ := json.Marshal(keys)
		keyFile.Write(encoded)

		return keys
	}

	json.NewDecoder(file).Decode(&keys)

	return keys
}

func main() {
	input := "You fools! You will never get my catnip!!!!!!!"

	keys := getKeys(len(input))

	encoded := catify(input, keys)

	savePair("example", input, encoded)
}
