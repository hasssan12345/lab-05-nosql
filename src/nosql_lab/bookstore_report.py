#!/usr/bin/env python3

import os
import logging
from pymongo import MongoClient

MONGODB_ATLAS_URL = os.getenv("MONGODB_ATLAS_URL")
MONGODB_ATLAS_USER = os.getenv("MONGODB_ATLAS_USER")
MONGODB_ATLAS_PWD = os.getenv("MONGODB_ATLAS_PWD")

logging.basicConfig(level=logging.INFO)


def main():
    """Print authors and their books from MongoDB."""
    client = None

    try:
        if not all([MONGODB_ATLAS_URL, MONGODB_ATLAS_USER, MONGODB_ATLAS_PWD]):
            raise ValueError("Missing MongoDB environment variables")

        client = MongoClient(
            MONGODB_ATLAS_URL,
            username=MONGODB_ATLAS_USER,
            password=MONGODB_ATLAS_PWD,
            serverSelectionTimeoutMS=10000
        )

        client.admin.command("ping")
        logging.info("Connected to MongoDB")

        database = client["bookstore"]
        authors = database["authors"]
        books = database["books"]

        # Select existing authors and the new author.
        author_ids = ["author_001", "author_002", "author_004"]

        total = authors.count_documents({"_id": {"$in": author_ids}})
        print(f"Authors: {total}")

        for author in authors.find({"_id": {"$in": author_ids}}):
            print(f"\n{author['name']}")

            # Find books linked to this author.
            for book in books.find({"author_ids": author["_id"]}):
                print(f"  {book['title']} ({book['published_year']})")

    except Exception as error:
        logging.error("MongoDB error: %s", error)

    finally:
        if client is not None:
            client.close()


if __name__ == "__main__":
    main()
