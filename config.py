from dotenv import load_dotenv
import os

load_dotenv()

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/paraphrase-multilingual-mpnet-base-v2")
LLM_MODEL = os.getenv("LLM_MODEL", "mistral")
URL_CHAT = os.getenv("URL_CHAT", "http://localhost:11434/api/chat")
FAQ_TOP_K = int(os.getenv("FAQ_TOP_K", 3))
THRESHOLD_DIFF = float(os.getenv("THRESHOLD_DIFF", 0.05))
