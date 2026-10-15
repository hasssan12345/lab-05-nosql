// Step 2: Select the bookstore database
db = db.getSiblingDB("bookstore");

// Step 3: Load authors
db.authors.drop();
let authors = JSON.parse(fs.readFileSync("authors.json", "utf8"));
db.authors.insertMany(authors);

// Step 4: Load books
db.books.drop();
let books = JSON.parse(fs.readFileSync("books.json", "utf8"));
db.books.insertMany(books);

// Step 5: List authors and books
printjson(db.authors.find().toArray());
printjson(db.books.find().toArray());

// Step 6: Add two books
db.books.insertMany([
  {
    title: "The Hobbit",
    published_year: 1937,
    author_ids: ["author_004"]
  },
  {
    title: "Pride and Prejudice: An Illustrated Edition",
    published_year: 2010,
    author_ids: ["author_001"]
  }
]);

// Step 7: Add missing author
db.authors.insertOne({
  _id: "author_004",
  name: "J. R. R. Tolkien",
  nationality: "British",
  bio: {
    short: "English author and scholar.",
    long: "J. R. R. Tolkien was an English writer best known for The Hobbit and The Lord of the Rings."
  }
});

// Step 8: Filter books by author
printjson(
  db.books.find({
    author_ids: { $in: ["author_001", "author_004"] }
  }).toArray()
);
