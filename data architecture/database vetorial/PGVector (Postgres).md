[[Postgres]]


### **Hybrid Search Support (`TSVECTOR`):**
- Using a `GENERATED ALWAYS` column automatically computes and updates PostgreSQL full-text search tokens whenever the `content` field is updated, eliminating the need for manual database triggers.

### The Best Practice: Text Chunks (Not Entire Books/PDFs)
Embedding models have strict token limits (e.g., 512, 1024, or 8192 tokens), and semantic search works best when vectors represent focused, specific topics.
Instead of putting a 50-page PDF into one row, you split the document into smaller **chunks** (e.g., 500–1000 characters).
- Each row in `document_embeddings` stores **one chunk** in the `content` column.
- The `embedding` vector represents the semantic meaning of that **specific chunk**.
### Linking Chunks Back to the Full Parent Document
To preserve the original document context while storing small chunks in the vector table, use a **Parent-Child relational structure**:

```sql
-- Parent Table: Stores the full, unchunked document
CREATE TABLE parent_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    full_text TEXT NOT NULL,  -- Entire original document/book/file
    file_path TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Child Table: Stores individual chunks and their embeddings
CREATE TABLE document_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    parent_id UUID REFERENCES parent_documents(id) ON DELETE CASCADE,
    
    chunk_index INT NOT NULL,  -- Order of chunk (0, 1, 2...)
    chunk_text TEXT NOT NULL,  -- The specific chunk text (~500 words)
    
    embedding VECTOR(1536) NOT NULL
);
```

### Summary
- **For short texts** (tweets, customer support tickets, product reviews): The `content` column holds the **entire text**.
- **For long documents** (PDFs, articles, code files): The `content` column holds a **single chunk**, linked back to a parent record or referenced via metadata (`{"source_file": "manual.pdf", "page": 12}`).
