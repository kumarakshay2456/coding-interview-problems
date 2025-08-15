package main

import (
	"encoding/json"
	"net/http"
	"github.com/gorilla/mux"
)

// GET /books
func GetBooks(w http.ResponseWriter, r *http.Request) {
	json.NewEncoder(w).Encode(books)
}

// GET /books/{id}
func GetBook(w http.ResponseWriter, r *http.Request) {
	params := mux.Vars(r)
	for _, book := range books {
		if book.ID == params["id"] {
			json.NewEncoder(w).Encode(book)
			return
		}
	}
	http.NotFound(w, r)
}

// POST /books
func CreateBook(w http.ResponseWriter, r *http.Request) {
	var book Book
	_ = json.NewDecoder(r.Body).Decode(&book)
	books = append(books, book)
	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(book)
}

// PUT /books/{id}
func UpdateBook(w http.ResponseWriter, r *http.Request) {
	params := mux.Vars(r)
	for i, book := range books {
		if book.ID == params["id"] {
			books = append(books[:i], books[i+1:]...)
			var updated Book
			_ = json.NewDecoder(r.Body).Decode(&updated)
			updated.ID = params["id"]
			books = append(books, updated)
			json.NewEncoder(w).Encode(updated)
			return
		}
	}
	http.NotFound(w, r)
}

// DELETE /books/{id}
func DeleteBook(w http.ResponseWriter, r *http.Request) {
	params := mux.Vars(r)
	for i, book := range books {
		if book.ID == params["id"] {
			books = append(books[:i], books[i+1:]...)
			w.WriteHeader(http.StatusNoContent)
			return
		}
	}
	http.NotFound(w, r)
}