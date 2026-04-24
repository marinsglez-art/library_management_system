import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";
import { MethodButton } from "../components/MethodButton";

const Book: React.FC = () => {
  return (
    <div id="page-book-0">
    <div id="id3fo" style={{"height": "100vh", "fontFamily": "Arial, sans-serif", "display": "flex", "--chart-color-palette": "default"}}>
      <nav id="i6214" style={{"width": "250px", "padding": "20px", "display": "flex", "overflowY": "auto", "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", "color": "white", "--chart-color-palette": "default", "flexDirection": "column"}}>
        <h2 id="i2u8k" style={{"fontSize": "24px", "fontWeight": "bold", "marginTop": "0", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"BESSER"}</h2>
        <div id="ie6vj" style={{"display": "flex", "--chart-color-palette": "default", "flexDirection": "column", "flex": "1"}}>
          <a id="iof5a" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "rgba(255,255,255,0.2)", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/book">{"Book"}</a>
          <a id="i660i" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/library">{"Library"}</a>
          <a id="ifuv2" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/author">{"Author"}</a>
        </div>
        <p id="i1mon" style={{"fontSize": "11px", "paddingTop": "20px", "marginTop": "auto", "textAlign": "center", "opacity": "0.8", "borderTop": "1px solid rgba(255,255,255,0.2)", "--chart-color-palette": "default"}}>{"© 2026 BESSER. All rights reserved."}</p>
      </nav>
      <main id="iglfg" style={{"padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default", "flex": "1"}}>
        <h1 id="ifo9y" style={{"fontSize": "32px", "marginTop": "0", "marginBottom": "10px", "color": "#333", "--chart-color-palette": "default"}}>{"Book"}</h1>
        <p id="ipk1q" style={{"marginBottom": "30px", "color": "#666", "--chart-color-palette": "default"}}>{"Manage Book data"}</p>
        <TableBlock id="table-book-0" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="Book List" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 5, "actionButtons": true, "columns": [{"label": "Title", "column_type": "field", "field": "title", "type": "str", "required": true}, {"label": "Pages", "column_type": "field", "field": "pages", "type": "int", "required": true}, {"label": "Stock", "column_type": "field", "field": "stock", "type": "int", "required": true}, {"label": "Price", "column_type": "field", "field": "price", "type": "float", "required": true}, {"label": "Release", "column_type": "field", "field": "release", "type": "date", "required": true}, {"label": "Genre", "column_type": "field", "field": "genre", "type": "enum", "options": ["Adventure", "Cookbooks", "Fantasy", "History", "Horror", "Philosophy", "Poetry", "Romance", "Technology", "Thriller"], "required": true}, {"label": "Library", "column_type": "lookup", "path": "library", "entity": "Library", "field": "name", "type": "list", "required": true}, {"label": "Authors", "column_type": "lookup", "path": "authors", "entity": "Author", "field": "name", "type": "list", "required": true}], "formColumns": [{"column_type": "field", "field": "title", "label": "title", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "pages", "label": "pages", "type": "int", "required": true, "defaultValue": null}, {"column_type": "field", "field": "stock", "label": "stock", "type": "int", "required": true, "defaultValue": null}, {"column_type": "field", "field": "price", "label": "price", "type": "float", "required": true, "defaultValue": null}, {"column_type": "field", "field": "release", "label": "release", "type": "date", "required": true, "defaultValue": null}, {"column_type": "field", "field": "genre", "label": "genre", "type": "enum", "required": true, "defaultValue": null, "options": ["Adventure", "Cookbooks", "Fantasy", "History", "Horror", "Philosophy", "Poetry", "Romance", "Technology", "Thriller"]}, {"column_type": "lookup", "path": "library", "field": "library", "lookup_field": "name", "entity": "Library", "type": "list", "required": true}, {"column_type": "lookup", "path": "authors", "field": "authors", "lookup_field": "name", "entity": "Author", "type": "list", "required": true}]}} dataBinding={{"entity": "Book", "endpoint": "/book/"}} />
        <div id="i63lj" style={{"marginTop": "20px", "display": "flex", "--chart-color-palette": "default", "flexWrap": "wrap", "gap": "10px"}}>
          <MethodButton id="i9ez4" className="action-button-component" style={{"padding": "6px 14px", "fontSize": "13px", "fontWeight": "600", "textDecoration": "none", "letterSpacing": "0.01em", "display": "flex", "cursor": "pointer", "transition": "background 0.2s", "background": "linear-gradient(90deg, #2563eb 0%, #1e40af 100%)", "color": "#fff", "borderRadius": "4px", "border": "none", "boxShadow": "0 1px 4px rgba(37,99,235,0.10)", "--chart-color-palette": "default", "alignItems": "center"}} endpoint="/book/{book_id}/methods/decrease_stock/" label="+ decrease_stock" parameters={[{"name": "qty", "type": "int", "required": true}]} isInstanceMethod={true} instanceSourceTableId="table-book-0" />
        </div>
      </main>
    </div>    </div>
  );
};

export default Book;
