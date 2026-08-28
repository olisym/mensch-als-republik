package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
)

func main() {
	if err := process(os.Stdin, os.Stdout); err != nil {
		fmt.Fprintf(os.Stderr, "%v\n", err)
		os.Exit(1)
	}
}

func process(r io.Reader, w io.Writer) error {
	sc := bufio.NewScanner(r)
	sc.Buffer(make([]byte, 0, 64*1024), 1024*1024)
	for sc.Scan() {
		fmt.Fprintln(w, verifyHex(sc.Text()).line())
	}
	return sc.Err()
}
