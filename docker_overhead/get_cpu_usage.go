package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"os/exec"
	"strconv"
	"strings"
	"time"
)

func main() {
	// fmt.Println("CPU usage % at %d ms intervals:\n", 200)

	var prevIdleTime, prevTotalTime uint64
	for {
		// CPU usage
		file, err := os.Open("/proc/stat")
		if err != nil {
			log.Fatal(err)
		}
		scanner := bufio.NewScanner(file)
		scanner.Scan()
		firstLine := scanner.Text()[5:] // get rid of cpu plus 2 spaces
		file.Close()
		if err := scanner.Err(); err != nil {
			log.Fatal(err)
		}
		split := strings.Fields(firstLine)
		idleTime, _ := strconv.ParseUint(split[3], 10, 64)
		totalTime := uint64(0)
		for _, s := range split {
			u, _ := strconv.ParseUint(s, 10, 64)
			totalTime += u
		}

		deltaIdleTime := idleTime - prevIdleTime
		deltaTotalTime := totalTime - prevTotalTime
		cpuUsage := (1.0 - float64(deltaIdleTime)/float64(deltaTotalTime)) * 100.0
		fmt.Printf("CPU: %d : %6.3f\n", time.Now().UnixMilli(), cpuUsage)

		prevIdleTime = idleTime
		prevTotalTime = totalTime

		// GPU busy
		file, err = os.Open("/sys/class/kgsl/kgsl-3d0/gpu_busy_percentage")
		if err != nil {
			log.Fatal(err)
		}
		scanner = bufio.NewScanner(file)
		scanner.Scan()
		gpuBusyPercentage := scanner.Text()[:2]
		fmt.Printf("GPU: %d: %s\n", time.Now().UnixMilli(), gpuBusyPercentage)

		// mem usage
		output, err := exec.Command("sh", "-c", "free -m").Output()
		if err != nil {
			log.Fatal(err)
		}
		scanner = bufio.NewScanner(strings.NewReader(string(output)))
		scanner.Scan()
        scanner.Scan()
		memLine := scanner.Text()
		fmt.Println(memLine)

		time.Sleep(time.Millisecond * 300)
	}
}
