package main

import (
	"fmt"
	"runtime"
	"time"
)

func main() {
	// Captura dados reais do hardware
	cores := runtime.NumCPU()
	timestamp := time.Now().Format("15:04:05")

	// Retorna uma linha simples que o Python consegue ler
	fmt.Printf("CORE_ATIVO: %d | STATUS: SOBERANO | UTC: %s", cores, timestamp)
}
