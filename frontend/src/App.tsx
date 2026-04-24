import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { TableProvider } from "./contexts/TableContext";
import Book from "./pages/Book";
import Library from "./pages/Library";
import Author from "./pages/Author";

function App() {
  return (
    <TableProvider>
      <div className="app-container">
        <main className="app-main">
          <Routes>
            <Route path="/book" element={<Book />} />
            <Route path="/library" element={<Library />} />
            <Route path="/author" element={<Author />} />
            <Route path="/" element={<Navigate to="/book" replace />} />
            <Route path="*" element={<Navigate to="/book" replace />} />
          </Routes>
        </main>
      </div>
    </TableProvider>
  );
}
export default App;
