Combines two complementary retrieval paradigms — [[Full-text Search]] and [[Vector Search]] — into a single database query to produce significantly more acurate search results.

By leveraging native [[Postgres]]


[[BM25]]
[[Vector Search]]
[[Re-ranking]]
[[RRF Fusion Algorithm]]



## [[LangChain]] example

```python
import os
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document

# 1. Database & Model Configurations
CONNECTION_STRING = "postgresql+psycopg://postgres:postgres@localhost:5432/vectordb"
COLLECTION_NAME = "documents_collection"

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 2. Initialize PGVector Store
vector_store = PGVector(
    embeddings=embeddings,
    collection_name=COLLECTION_NAME,
    connection=CONNECTION_STRING,
    use_jsonb=True,
)

# Insert sample documents (run once or as needed)
sample_docs = [
    Document(page_content="PostgreSQL supports vector similarity search via the pgvector extension."),
    Document(page_content="HNSW indexes in pgvector accelerate nearest neighbor search for high-dimensional vectors."),
    Document(page_content="Reciprocal Rank Fusion (RRF) combines lexical full-text search with vector search."),
]
vector_store.add_documents(sample_docs)

# 3. Create Retriever
retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 2}
)

# 4. Helper function to format retrieved documents
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# 5. Define Prompt Template
prompt_template = """Answer the question based only on the following context:

Context:
{context}

Question: {question}

Answer:"""

prompt = ChatPromptTemplate.from_template(prompt_template)

# 6. Build LCEL Chain using standard pipe syntax
rag_chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough()
    }
    | prompt
    | llm
    | StrOutputParser()
)

# 7. Execute Chain
query = "How does pgvector perform vector similarity search efficiently?"
response = rag_chain.invoke(query)

print("Query:", query)
print("Response:", response)
```
