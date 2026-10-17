import numpy as np

EMBEDDING_MODEL = "gemini-embedding-001"

def generate_text(client, model_name, prompt):
    response = client.interactions.create(
        model=model_name,
        input=prompt,
    )

    text = getattr(response, "output_text", None)

    if not text:
        raise RuntimeError("The model returned an empty response.")

    return text.strip()

def embed_texts(client, texts):
    if isinstance(texts, str):
        texts = [texts]
    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=texts,
    )
    embeddings = getattr(response, "embeddings", None)
    if not embeddings:
        raise RuntimeError("The embedding API returned no vectors.")
    result = []
    for item in embeddings:
        values = getattr(item, "values", None)
        if values is None and isinstance(item, dict):
            values = item.get("values")
        if not values:
            raise RuntimeError("An embedding vector was empty.")
        result.append(np.asarray(values, dtype=np.float32))
    return result

def retrieve_relevant_chunks(client, query, chunks, chunk_embeddings, top_k=4):
    if not chunks or chunk_embeddings is None or len(chunk_embeddings) != len(chunks):
        raise ValueError("Process a PDF before asking questions.")
    query_vector = embed_texts(client, [query])[0]
    matrix = np.vstack(chunk_embeddings)
    query_norm = np.linalg.norm(query_vector)
    matrix_norms = np.linalg.norm(matrix, axis=1)
    scores = (matrix @ query_vector) / (matrix_norms * query_norm + 1e-10)
    indexes = np.argsort(scores)[::-1][:top_k]
    return [{"text": chunks[int(i)], "score": float(scores[int(i)])} for i in indexes]
