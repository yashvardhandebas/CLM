#converts text into chunks, embeds them, and stores them in ChromaDB and then asks Gemini a question about the contract
from rag.text_splitter import split_text
from rag.embeddings import embed_texts
from rag.vector_store import store_chunks, retrieve_chunks
from memory.session_memory import (
    init_session,
    set_user_profile,
    add_message,
    get_memory_context,
)
from memory.profile_extractor import extract_profile_info

def ingest_contract(contract_text: str, client):
    """
    Splits contract, embeds chunks, and stores them in ChromaDB
    """
    chunks = split_text(contract_text)
    embeddings = embed_texts(client, chunks)
    store_chunks(chunks, embeddings)


def ask_contract(question: str, client, session_id: str):
    """
    Retrieves relevant contract chunks, uses conversational memory,
    and asks Gemini.
    """
    # Initialize / update session
    init_session(session_id)

    # Extract & store profile info from the question
    profile_info = extract_profile_info(question)
    for k, v in profile_info.items():
        set_user_profile(session_id, k, v)

    # Log user message
    add_message(session_id, "user", question)

    # RAG retrieval
    query_embedding = embed_texts(client, [question])[0]
    relevant_chunks = retrieve_chunks(query_embedding)
    context = "\n\n".join(relevant_chunks)

    # Build memory context for the model
    memory_context = get_memory_context(session_id)

    prompt = f"""
You are a contract analysis assistant.

Use the contract context AND conversation memory to answer.
If info is missing, say "Not found".

{memory_context}

Contract Context:
{context}

Question:
{question}
"""

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt,
    )

    answer = response.text
    add_message(session_id, "assistant", answer)
    return answer

