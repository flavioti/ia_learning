#cosine_similarity

Embedding Distance-Based
### Python example
```python
import re
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def semantic_chunking(
    text: str,
    threshold_percentile: float = 80.0,
    buffer_size: int = 1,
    embedding_model_name: str = "all-MiniLM-L6-v2",
) -> list[str]:
    """Splits a document into chunks based on semantic shifts between sentences.
    
    Args:
        text: Raw input document string.
        threshold_percentile: Percentile (0-100) of distances to trigger a chunk split.
        buffer_size: Number of neighboring sentences to group when computing sentence context.
        embedding_model_name: SentenceTransformer model name.
    """
    # 1. Split text into sentences using basic regex boundary detection
    sentences = [s.strip() for s in re.split(r"(?<=[.?!])\s+", text.strip()) if s.strip()]
    if len(sentences) <= 1:
        return sentences

    model = SentenceTransformer(embedding_model_name)

    # 2. Combine sentences with surrounding buffers for smoother contextual embeddings
    buffered_sentences = []
    for i in range(len(sentences)):
        start = max(0, i - buffer_size)
        end = min(len(sentences), i + buffer_size + 1)
        buffered_sentences.append(" ".join(sentences[start:end]))

    # Generate embeddings
    embeddings = model.encode(buffered_sentences)

    # 3. Calculate cosine distances between consecutive sentence embeddings
    distances = []
    for i in range(len(embeddings) - 1):
        similarity = cosine_similarity([embeddings[i]], [embeddings[i + 1]])[0][0]
        distance = 1.0 - similarity
        distances.append(distance)

    # 4. Determine dynamic distance threshold based on specified percentile
    threshold = np.percentile(distances, threshold_percentile)

    # 5. Build chunks by splitting whenever distance exceeds threshold
    chunks = []
    current_chunk = [sentences[0]]

    for i, dist in enumerate(distances):
        if dist > threshold:
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentences[i + 1]]
        else:
            current_chunk.append(sentences[i + 1])

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


# Example usage
if __name__ == "__main__":
    sample_text = (
        "Database indexes improve query speed significantly by creating lookup structures. "
        "B-Trees and Hash indexes are common indexing strategies used in relational engines. "
        "However, indexes increase write latency because every insert requires updating the index. "
        "In cooking, caramelization occurs when carbohydrates like sugar are heated to high temperatures. "
        "This pyrolysis reaction produces dark brown compounds with complex nutty flavors. "
        "Chef tips often suggest adding a pinch of baking soda to accelerate brown butter sauce."
    )

    chunks = semantic_chunking(sample_text, threshold_percentile=75.0)
    for idx, chunk in enumerate(chunks, 1):
        print(f"--- Chunk {idx} ---\n{chunk}\n")
```
