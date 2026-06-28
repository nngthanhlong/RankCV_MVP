from app.rag.retriever import retrieve_fpt_context

query = """
Java
Spring Boot
React
Cloud
"""

print(retrieve_fpt_context(query))