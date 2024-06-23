import React, { useState, useEffect } from "react";
import axios from "axios";

function BookList() {
  const [books, setBooks] = useState([]);

  useEffect(() => {
    const fetchBooks = async () => {
      const response = await axios.get("https://api.pdfdrive.com/v1/new"); // Hypothetical API endpoint
      setBooks(response.data.books);
    };
    fetchBooks();
  }, []);

  return (
    <div>
      <h2>New Books</h2>
      <div className="book-list">
        {books.map((book) => (
          <div key={book.id} className="book">
            <img src={book.cover_url} alt={book.title} />
            <a
              href={book.download_url}
              target="_blank"
              rel="noopener noreferrer"
            >
              {book.title}
            </a>
          </div>
        ))}
      </div>
    </div>
  );
}

export default BookList;
