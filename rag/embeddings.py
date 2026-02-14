"""
Utility to embed texts into a vector space using Gemini embeddings.
"""


def embed_texts(client, texts):
    embeddings = []

    for text in texts:
        # Use the current Gemini embedding model.
        # NOTE: older models like `models/embedding-gecko-001` are deprecated.
        response = client.models.embed_content(
            model="gemini-embedding-001",
            contents=text,
        )

        # `EmbedContentResponse` exposes embeddings on `response.embeddings`.
        # We request a single text at a time, so take the first embedding.
        embedding_vector = response.embeddings[0].values
        embeddings.append(embedding_vector)

    return embeddings
