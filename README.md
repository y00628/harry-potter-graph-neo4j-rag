# harry-potter-graph-neo4j-rag

The RAG Stack featuring Knowledge Graphs with Harry Potter Dataset

## Project Description

This project involves creating a Retrieval-Augmented Generation (RAG) system utilizing knowledge graphs, with a focus on the Harry Potter dataset. Over five weeks, we explore key concepts like Neo4j-based knowledge graph creation, integration of graph-based retrieval techniques, and advanced strategies like multi-hop reasoning.

## Setup

### 1. Clone the Repository

First, clone the repository to your local machine:

```
git clone https://github.com/y00628/harry-potter-graph-neo4j-rag
cd harry-potter-graph-neo4j-rag
```

### 2. (OPTIONAL) Downloading Data

You will need to manually download the necessary data from the provided SharePoint link. Follow the steps below:

- Go to the following link: https://nuochenpku.github.io/HPD.github.io/download
- Click on `EN-Relations`
- Click on a chapter of your choice and save it in the data folder (Chapter 1 already in there)

### 4. Create and Activate Virtual Environment

After cloning the repository, create a virtual environment to isolate project dependencies. This step ensures that the dependencies for this project don't interfere with others.

#### On macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

#### On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 5. Install Dependencies

With the virtual environment activated, install the necessary dependencies using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```
