from typing import Dict, List

# In-memory session store
SESSION_MEMORY: Dict[str, Dict] = {}


def init_session(session_id: str):
    if session_id not in SESSION_MEMORY:
        SESSION_MEMORY[session_id] = {
            "user_profile": {},
            "conversation": [],
        }


def set_user_profile(session_id: str, key: str, value: str):
    SESSION_MEMORY[session_id]["user_profile"][key] = value


def add_message(session_id: str, role: str, content: str):
    SESSION_MEMORY[session_id]["conversation"].append(
        {
            "role": role,
            "content": content,
        }
    )


def get_memory_context(session_id: str) -> str:
    profile = SESSION_MEMORY[session_id]["user_profile"]
    convo: List[Dict] = SESSION_MEMORY[session_id]["conversation"][-6:]  # last 6 messages

    profile_text = "\n".join([f"{k}: {v}" for k, v in profile.items()])
    convo_text = "\n".join([f"{m['role']}: {m['content']}" for m in convo])

    return f"""
User Profile:
{profile_text}

Recent Conversation:
{convo_text}
"""


