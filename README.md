# Harry Potter Graph Neo4j RAG

This project implements a Retrieval-Augmented Generation (RAG) system using a knowledge graph based on the Harry Potter dataset, integrated with Neo4j and OpenAI. The system supports explicit and implicit retrieval from the graph and vector search capabilities.

## Prerequisites

Ensure the following software and packages are installed:

- **Python 3.8+**
- **Neo4j Desktop** (or any other running Neo4j instance)
- **Required Python libraries**: The libraries should be installed using the `requirements.txt` file.

Make sure you have the following environment variables configured in your `.env` file.

### Create `.env` File

You need to create a `.env` file in the root directory of the project with the following content:

```
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=your_neo4j_username
NEO4J_PASSWORD=your_neo4j_password
OPENAI_API_KEY=your_openai_api_key
```

Replace the placeholders with your actual credentials.

## Setup

### 1. Clone the Repository

First, clone the repository:

```bash
git clone https://github.com/y00628/harry-potter-graph-neo4j-rag
cd harry-potter-graph-neo4j-rag
```

### 2. Install Dependencies

Activate your virtual environment and install the dependencies:

```bash
pip install -r requirements.txt
```

### 3. Run Neo4j

Ensure Neo4j is running, and the database you intend to use is active.

## How to Run the Script

This script allows you to interact with a Neo4j-based knowledge graph, perform explicit and implicit retrievals, and execute vector search using OpenAI embeddings.

### 1. Refresh and View Schema

To refresh and print the schema of the graph:

```bash
py harry_potter_rag.py get_schema
```

### 2. Explicit Retrieval

To retrieve a response based on a specific question using the knowledge graph:

```bash
py harry_potter_rag.py explicit_retrieve "Your question here"
```

For example:

```bash
py harry_potter_rag.py explicit_retrieve "List all the people who are not enemies with Harry"
```

### 3. Implicit Retrieval

To retrieve a response using a language model without directly querying the graph:

```bash
py harry_potter_rag.py implicit_retrieve "Your question here"
```

For example:

```bash
py harry_potter_rag.py implicit_retrieve "Who are Harry's allies?"
```

### 4. Vector Search

To perform a vector search for similar nodes based on a query, and return the top K most similar results:

```bash
py harry_potter_rag.py vector_search "Your question here" <top_k>
```

If you do not specify the second parameter (`<top_k>`), the default value will be `3`.

For example, to get the top 3 similar nodes based on a question:

```bash
py harry_potter_rag.py vector_search "Who are similar to Harry?"
```

To get the top 5:

```bash
py harry_potter_rag.py vector_search "Who are similar to Harry?" 5
```

### Notes

- The `vector_search` function uses OpenAI's embedding model to find similarities within the graph. Make sure Neo4j is set up with GDS (Graph Data Science) and the nodes are embedded.
- You can adjust the `top_k` parameter to return more or fewer similar nodes based on your needs. The default is 3.

### Troubleshooting

If you encounter any issues:

- Verify that Neo4j is running and the credentials are correct in the `.env` file.
- Ensure OpenAI API key is correctly set and accessible.
