# Regulatory–SOP Gap Detection System

## Overview
This system detects gaps between USFDA regulatory expectations and a manufacturer’s current SOPs. It uses a RAG (Retrieval-Augmented Generation) architecture to identify missing, outdated, or weakly defined procedures.

## Architecture
1.  **Ingestion**: `pypdf` for parsing PDF documents.
2.  **Storage**: `chromadb` for vector storage and semantic search.
3.  **Analysis**: LLM-based comparison of SOP sections vs. retrieved regulations.

## Setup
1.  Install dependencies:
    ```bash
    pip install chromadb pypdf
    ```
2.  Run the system:
    ```bash
    python3 main.py
    ```

## Project Structure
- `gap_system.py`: Core logic for loading, processing, and analyzing documents.
- `main.py`: Entry point script.

