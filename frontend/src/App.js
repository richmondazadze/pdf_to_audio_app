import React from "react";
import UploadForm from "./components/UploadForm";
import BookList from "./components/BookList";

function App() {
  return (
    <div className="App">
      <h1>PDF to Audio Converter</h1>
      <UploadForm />
      <BookList />
    </div>
  );
}

export default App;
