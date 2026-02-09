from typing import Dict, List, Optional
from backend.config import settings
from backend.services.groq_client import get_groq_client
from backend.storage.in_memory_store import DocChunk
from backend.services.retrieval_service import retrieve_top_k

SYSTEM_RULES = """
You are a highly intelligent, expert-level AI Study Buddy Agent specializing ONLY in STEM subjects (IT, Math, Coding, Logic, Engineering).

STRICT SUBJECT RESTRICTIONS:
1. **Allowed Topics**: 
   - Information Technology (IT), Computer Science, Networking, Cybersecurity.
   - Mathematics (Calculus, Algebra, Statistics, etc.).
   - Software Engineering, Programming (Python, JS, C++, etc.), Databases.
   - Physical Sciences (Physics, Engineering) and Logic.

2. **Forbidden Topics (REFUSE THESE)**:
   - Biology, Medicine (e.g., medical advice, headache relief).
   - Politics, Social Issues, Religion.
   - General Life Advice (e.g., fixing a tyre, cooking recipes).
   - Humanities (History, Literature, Arts), unless directly relevant to a Tech/Math document.

3. **Refusal Protocol**:
   - If asked about a Forbidden Topic, say exactly: "I am a specialized Tech and Math Study Buddy. I cannot provide information on [Subject]. Please ask me something related to IT, Coding, or Mathematics!"

CORE BEHAVIORS:
1. **Expert Solver**: Solve math/coding problems step-by-step. Apply concepts rather than just quoting. Use general knowledge for STEM gaps.
2. **Teacher Persona**: Use examples, analogies, and real-world context. Break down complexity.
3. **Document Priority**: Check provided EXCERPTS first. Cite sources (e.g., [Source 1]).
4. **Hybrid Knowledge**: Seamlessly blend your vast STEM knowledge with document info.
5. **Natural Conversation**: Greetings and small talk are allowed.
"""

def answer_question_from_docs(
    question: str,
    all_chunks: List[DocChunk],
    top_k: int = 5
) -> Dict[str, object]:
    """
    Retrieves relevant chunks and generates an answer using Groq.
    Now allows general conversation and fallback to general knowledge.
    """
    
    # 1. Retrieve relevant chunks
    # We always try to find relevant chunks first
    if not all_chunks:
         relevant_chunks_with_scores = []
    else:
        relevant_chunks_with_scores = retrieve_top_k(question, all_chunks, top_k=top_k)
    
    used_excerpts = []
    context_text = ""
    
    for i, (chunk, score) in enumerate(relevant_chunks_with_scores):
        # We can enforce a minimum score threshold here if needed
        # For now, we include them but the LLM decides if they are useful
        excerpt = f"[Source {i+1}] (Doc: {chunk.doc_name}): {chunk.text}\n"
        context_text += excerpt
        used_excerpts.append({
            "doc_name": chunk.doc_name,
            "chunk_id": chunk.chunk_id,
            "text": chunk.text,
            "score": score
        })

    # 2. Prepare prompt
    if not context_text:
        context_text = "No relevant document excerpts found."

    messages = [
        {"role": "system", "content": SYSTEM_RULES},
        {
            "role": "user",
            "content": f"User Question: {question}\n\nDOCUMENT EXCERPTS:\n{context_text}"
        }
    ]

    # 3. Call Groq API
    client = get_groq_client()
    try:
        completion = client.chat.completions.create(
            messages=messages,
            model=settings.groq_model,
            temperature=0.6, # Increased for more creativity and depth
            max_tokens=1500, # Increased for longer explanations
        )
        answer = completion.choices[0].message.content
    except Exception as e:
        answer = f"Error generating answer: {e}"

    return {
        "answer": answer,
        "used_excerpts": used_excerpts
    }