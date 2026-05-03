#!/usr/bin/env python3
"""
Simple RAGFlow MCP Server
A basic MCP server that provides RAG (Retrieval-Augmented Generation) functionality.
"""

import asyncio
import json
import os
from typing import Any, Dict, List, Optional

from fastmcp import FastMCP

# Mock data for demonstration
MOCK_DOCUMENTS = [
    {
        "id": "doc1",
        "title": "Getting Started with AI",
        "content": "Artificial Intelligence (AI) is transforming how we work and live. Machine learning algorithms can process vast amounts of data to make predictions and decisions.",
        "source": "ai-guide.pdf",
        "score": 0.95
    },
    {
        "id": "doc2",
        "title": "Team Development Best Practices",
        "content": "Effective team development requires clear communication, version control, and regular code reviews. Use Git for version control and establish coding standards.",
        "source": "dev-practices.md",
        "score": 0.87
    },
    {
        "id": "doc3",
        "title": "MCP Protocol Overview",
        "content": "The Model Context Protocol (MCP) enables AI assistants to access external tools and data sources. It provides a standardized way to integrate various services.",
        "source": "mcp-docs.html",
        "score": 0.92
    }
]

app = FastMCP("ragflow-mcp-server")

@app.tool()
async def rag_search(query: str, repo: Optional[str] = None, top_k: int = 5) -> Dict[str, Any]:
    """
    Search for relevant documents using RAG (Retrieval-Augmented Generation).

    Args:
        query: The search query
        repo: Optional repository filter
        top_k: Maximum number of results to return (1-8)

    Returns:
        Dictionary containing search results
    """
    # Limit top_k to reasonable bounds
    top_k = max(1, min(8, top_k))

    # Simple keyword-based search (in a real implementation, this would use embeddings/vector search)
    results = []
    query_lower = query.lower()

    for doc in MOCK_DOCUMENTS:
        content_lower = doc["content"].lower()
        title_lower = doc["title"].lower()

        # Calculate a simple relevance score
        if query_lower in content_lower or query_lower in title_lower:
            score = doc["score"] * 1.2  # Boost score for matches
        else:
            # Check for partial matches
            query_words = set(query_lower.split())
            content_words = set(content_lower.split())
            title_words = set(title_lower.split())

            word_overlap = len(query_words & (content_words | title_words))
            if word_overlap > 0:
                score = doc["score"] * (word_overlap / len(query_words))
            else:
                continue

        results.append({
            "title": doc["title"],
            "source": f"file://{doc['source']}",
            "score": round(score, 3),
            "content": doc["content"][:500] + "..." if len(doc["content"]) > 500 else doc["content"]
        })

    # Sort by score and limit results
    results.sort(key=lambda x: x["score"], reverse=True)
    results = results[:top_k]

    return {"results": results}

@app.tool()
async def rag_get_doc(doc_id: str) -> Dict[str, Any]:
    """
    Retrieve a specific document by ID.

    Args:
        doc_id: The document ID to retrieve

    Returns:
        Dictionary containing the document details
    """
    for doc in MOCK_DOCUMENTS:
        if doc["id"] == doc_id:
            return {
                "id": doc["id"],
                "title": doc["title"],
                "content": doc["content"],
                "source": f"file://{doc['source']}",
                "score": doc["score"]
            }

    return {"error": f"Document with ID '{doc_id}' not found"}

@app.tool()
async def rag_answer_with_sources(question: str, repo: Optional[str] = None) -> Dict[str, Any]:
    """
    Answer a question using RAG with source citations.

    Args:
        question: The question to answer
        repo: Optional repository filter

    Returns:
        Dictionary containing the answer and sources
    """
    # First, search for relevant documents
    search_results = await rag_search(question, repo, top_k=3)

    if not search_results["results"]:
        return {
            "answer": "I couldn't find relevant information to answer this question.",
            "sources": [],
            "confidence": 0.0
        }

    # Generate a simple answer based on the top result
    top_result = search_results["results"][0]

    # Mock answer generation (in a real implementation, this would use an LLM)
    answer = f"Based on the available information: {top_result['content'][:200]}..."

    return {
        "answer": answer,
        "sources": search_results["results"],
        "confidence": top_result["score"]
    }

if __name__ == "__main__":
    print("🚀 Starting RAGFlow MCP Server...", file=__import__("sys").stderr)
    print(f"📚 Loaded {len(MOCK_DOCUMENTS)} documents", file=__import__("sys").stderr)
    app.run()