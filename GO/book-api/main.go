package main

import (
	"log"
	"net/http"
	"github.com/gorilla/mux"
)

func main(){
	r := mux.NewRouter()
	r.HandleFunc("/books", GetBooks).Methods("GET")
	r.HandleFunc("/books/{id}", GETBook).Methods("GET")
	r.HandleFunc("/books", CreateBook).Methods("POST")
	r.HandleFunc("/books/{id}", UpdateBook).Methods("PUT")
	r.HandleFunc("/books/{id}", DeleteBook).Methods("DELETE")

	log.Println("Server is running on the port 8000")
	log.Fatal(http.ListenAndServe(":8000", r))
}