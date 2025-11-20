package main

import (
    "net/http"
    "fmt"
)

func main() {
    http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
        w.WriteHeader(http.StatusOK)
        fmt.Fprint(w, "OK")
    })
    fmt.Println("Session collector running on :8001")
    http.ListenAndServe(":8001", nil)
}
