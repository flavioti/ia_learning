[[vector]] | [[embeddings (vector)]]

Is a specialized storage system designed to capture, index, and query data as high-dimensional vectors, commonly know as embeddings, Unlike tradicional databases that store data in rigid rows and columns or text documents, vector database are purpose-build to handle unstructured data like text, images, video, and audio by turning them into numerical representations.

The core breakthrough of this technology is **semantic search**. Instead of searching for exact keywords, a vector database looks for results based on the meaning or context behing the query.

## How it works?

1. ***Creating Embeddings***: An AI model process unstructured data - like a sentence or an image - and translates it into a long string of numbers (a vector). This vector represents the mathematical meaning of the data.
2. ***The vector space***: The vector are placed into a mult-dimensional map. Data points with similar meanings or contexts (e.g., the word "puppy" and a photo of a golden retriever) are **plotted geometrically close to one another**.
3. ***Similarity search***: When you run a query, the database converts syour search term into a vector, measures the mathematical distance to the other vectors (using metrics like [[cosine similarity]]), and instantly returns the closest matches.
## Key use cases

Vector databases have become a critical pillar of modern Artificial Intelligence and machine learning applications:
- ***[[RAG (Retrieval-Augmented Generation)]]***
- ***[[Recomendation systems]]
- ***[[Multimodal search]]***

Popular vector databases in the industry include standalone systemas like [[vetorial databases/Pinecone|Pinecone]], [[Qdrant]], [[Weaviate]], and [[Milvus]], as well as vector extensions for tradional systems like pgvector for PostgresSQL.
## Re ranking

???
