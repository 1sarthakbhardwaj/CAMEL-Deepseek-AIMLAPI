"""
app.py

This module provides the core functionality for processing user queries using
the CAMEL framework with DeepSeek‑R1 on the AIML platform. It retrieves context
from an uploaded document and generates an answer using a ChatAgent.
"""

import os
from camel.embeddings import OpenAIEmbedding
from camel.types import EmbeddingModelType
from camel.agents import ChatAgent
from camel.models import ModelFactory
from camel.types import ModelPlatformType
from camel.retrievers import AutoRetriever
from camel.types import StorageType

# Initialize the OpenAI embedding instance.
embedding_instance = OpenAIEmbedding(model_type=EmbeddingModelType.TEXT_EMBEDDING_3_LARGE)

def process_query(query: str, file_path: str) -> str:
    """
    Processes a user query by retrieving relevant context from an uploaded document
    and generating an answer using the DeepSeek‑R1 model (via the AIML platform) in CAMEL.

    Parameters:
    - query (str): The user's question.
    - file_path (str): The local file path of the uploaded document.

    Returns:
    - str: The answer provided by the AI agent.
    """
    if not file_path:
        return "No document uploaded. Please upload a file."

    # Define the system message that guides the assistant's behavior.
    assistant_sys_msg = (
        "You are a helpful assistant. Answer questions based on the retrieved context. "
        "If you cannot answer, simply state 'I don't know'."
    )

    # Set up the auto retriever for document context extraction.
    auto_retriever = AutoRetriever(
        vector_storage_local_path="local_data2/",
        storage_type=StorageType.QDRANT,
        embedding_model=embedding_instance
    )

    # Retrieve relevant context from the document.
    retrieved_info = auto_retriever.run_vector_retriever(
        query=query,
        contents=[file_path],
        top_k=1,
        return_detailed_info=False,
        similarity_threshold=0.5
    )

    if not retrieved_info:
        return "No relevant information found in the document."

    # Create the DeepSeek‑R1 model using the AIML platform.
    deepseek_model = ModelFactory.create(
        model_platform=ModelPlatformType.AIML,  # Use AIML as the platform
        model_type="deepseek/deepseek-r1",
        model_config_dict={"max_tokens": 2000}
    )

    # Prepare the user's message using the retrieved context.
    user_msg = str(retrieved_info)

    # Initialize the ChatAgent with the system message and DeepSeek model.
    agent = ChatAgent(
        system_message=assistant_sys_msg,
        model=deepseek_model
    )

    # Get the response from the agent.
    assistant_response = agent.step(user_msg)
    if assistant_response and assistant_response.msgs:
        return assistant_response.msgs[0].content
    else:
        return "No response from the agent."
