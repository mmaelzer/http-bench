package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"time"
)

func handleHello(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/plain")
	fmt.Fprint(w, "Hello World")
}

func handleJson(w http.ResponseWriter, r *http.Request) {
	decoder := json.NewDecoder(r.Body)
	var j []map[string]interface{}
	err := decoder.Decode(&j)
	if err != nil {
		panic(err)
	}
	jstr, err := json.Marshal(j)
	if err != nil {
		panic(err)
	}
	w.Header().Set("Content-Type", "application/json")
	fmt.Fprint(w, string(jstr))
}

func handleDelay(w http.ResponseWriter, r *http.Request) {
	time.Sleep(100 * time.Millisecond)
	handleHello(w, r)
}

func main() {
	http.HandleFunc("/hello", handleHello)
	http.HandleFunc("/json", handleJson)
	http.HandleFunc("/delay", handleDelay)

	fmt.Println("=== server running on 127.0.0.1:8080 ===")
	fmt.Println("begin benchmark")
	fmt.Println(http.ListenAndServe(":8080", nil))
}
