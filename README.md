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

### 3. Installing Neo4j Desktop Version

#### 1. Download Neo4j Desktop

- Go to the official Neo4j website: [https://neo4j.com/download/](https://neo4j.com/download/)
- Choose **Neo4j Desktop** and click **Download**.

#### 2. Install Neo4j Desktop

#### **For Windows**

- Open the `.exe` file you downloaded.
- Follow the installation prompts.
- Once installed, launch **Neo4j Desktop**.

#### **For macOS**

- Open the `.dmg` file you downloaded.
- Drag and drop the **Neo4j Desktop** icon to your Applications folder.
- Launch **Neo4j Desktop** from your Applications folder.

#### **For Linux**

- Open a terminal and run the following commands:

  ```bash
  wget https://dist.neo4j.com/neo4j-desktop-5.23.0-x86_64.AppImage
  chmod a+x neo4j-desktop-5.23.0-x86_64.AppImage
  ./neo4j-desktop-5.23.0-x86_64.AppImage
  ```

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

### 6. Create `.env` File

You need to create a `.env` file in the root directory of the project with the following content:

```
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=your_neo4j_username
NEO4J_PASSWORD=your_neo4j_password
OPENAI_API_KEY=your_openai_api_key
```

Replace the placeholders with your actual credentials.

## Instructions

### 1. Creating Knowledge Graph

- Open your terminal (or command prompt) and navigate to the directory containing the script using the `cd` command.

  For example:

  ```bash
  cd /path/to/your/kg.py
  ```

- Ensure that Neo4j Desktop is running and the database is started.
- Run the script using Python by executing the following command:

  ```bash
  py kg.py
  ```

  The `kg.py` script will preprocess the data and create a knowledge graph in your Neo4j database. All data preprocessing is handled within the script, so no additional steps are required.

- After running the script, you should see a confirmation sentence indicating that the knowledge graph has been successfully created.

  Example output:

  ```bash
  Knowledge Graph created with 33 nodes and 96 relationships.
  ```

### 2. Query Retrieval

After setting up the knowledge graph using `kg.py`, you can run the `harry_potter_rag.py` script to retrieve relevant information.

#### Retrieve Schema

You can refresh and print the graph schema by running:

```bash
py harry_potter_rag.py get_schema
```

This will refresh and display the schema of the graph in the console.

#### Explicit Retrieval

To retrieve a response based on a specific question using the knowledge graph:

Example:

```bash
python harry_potter_rag.py explicit_retrieve "List all the people who are not enemies with Harry"
```

This will invoke a Cypher query on the graph and return a natural response based on the provided question.

Here are a few example queries you can try:

- "List all the people who are not enemies with Harry"
- "Show all the relationships in the graph"
- "Who are the allies of Harry?"

These queries will retrieve information based on the graph structure created by `kg.py`.

#### Implicit Retrieval

To retrieve a response using a language model without directly querying the graph:

```bash
py harry_potter_rag.py implicit_retrieve "Your question here"
```

For example:

```bash
py harry_potter_rag.py implicit_retrieve "Who are Harry's allies?"
```

#### Vector Search

To perform a vector search for similar nodes based on a query, and return the top K most similar results:

```bash
py harry_potter_rag.py vector_search "Your question here" <top_k>
```

If you do not specify the second parameter (`<top_k>`), the default value will be `3`.

For example, to get the top 5 similar nodes based on a question:

```bash
py harry_potter_rag.py vector_search "Who are similar to Harry?" 5
```

To get the top 3:

```bash
py harry_potter_rag.py vector_search "Who are similar to Harry?"
```

## Notes

#### Neo4j and OpenAI Configuration

Ensure that your `.env` file contains the correct configuration for Neo4j and OpenAI:

- **NEO4J_URI**: The URI of your Neo4j database (e.g., `bolt://localhost:7687`)
- **NEO4J_USERNAME**: Your Neo4j username
- **NEO4J_PASSWORD**: Your Neo4j password
- **OPENAI_API_KEY**: Your OpenAI API key

#### Vector Search Method

- The `vector_search` function uses OpenAI's embedding model to find similarities within the graph. Make sure Neo4j is set up with GDS (Graph Data Science) and the nodes are embedded.
- You can adjust the `top_k` parameter to return more or fewer similar nodes based on your needs. The default is 3.
