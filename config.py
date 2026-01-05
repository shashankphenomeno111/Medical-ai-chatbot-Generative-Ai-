# Medical AI Chatbot Configuration
# All settings centralized here for easy customization

# LLM Model Settings
MODEL_NAME = "google/flan-t5-base"  # Free, runs locally, no API key needed
MAX_NEW_TOKENS = 512
TEMPERATURE = 0.7

# Vector Store Settings
VECTORSTORE_PATH = "vectorstore"
TOP_K_RESULTS = 4  # Number of documents to retrieve

# Embedding Model
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# System Prompts
SYSTEM_PROMPT = """You are an advanced medical AI assistant with access to a Global Knowledge Base (Wikipedia, Web Search, and Medical Journals). 
Your goal is to provide comprehensive, accurate, and detailed information about ANY disease or condition.

Instructions:
1. Use the provided context (which may include Wikipedia summaries, Web results, or Local PDFs) to answer the user.
2. Structure your answer with clear sections: Overview, Symptoms, Causes, Treatment.
3. Be professional and empathetic.
4. If the context contains a Wikipedia summary, use it to provide a high-quality global overview.
5. Always advise consulting a doctor for serious issues."""

# Medical Disclaimer
DISCLAIMER = """⚠️ **Medical Disclaimer**: This AI provides general health information only. 
It is NOT a substitute for professional medical advice, diagnosis, or treatment. 
Always consult a qualified healthcare provider for medical concerns."""

# UI Theme Colors
THEME = {
    "primary": "#00D4AA",      # Teal/Mint
    "secondary": "#1E3A5F",     # Dark Blue
    "background": "#0E1117",    # Dark background
    "text": "#FFFFFF",          # White text
    "accent": "#FF6B6B",        # Coral for warnings
    "success": "#4CAF50",       # Green for success
}
