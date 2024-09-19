
# Import necessary modules
from dotenv import load_dotenv
import os
from neo4j import GraphDatabase
import pandas as pd
from xlsx_to_csv import *
from kg import *
from langchain_community.graphs import Neo4jGraph
from langchain.chains import GraphCypherQAChain
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI
import warnings
warnings.filterwarnings("ignore")

load_dotenv()

NEO4J_URI = os.getenv('NEO4J_URI')
NEO4J_USERNAME = os.getenv('NEO4J_USERNAME')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')

URI = NEO4J_URI
AUTH = (NEO4J_USERNAME, NEO4J_PASSWORD)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()

graph = Neo4jGraph()

def get_schema():
    """Refresh and return the graph schema."""
    graph.refresh_schema()
    schema = graph.schema
    print(schema)
    return schema

def explicit_retrieve(question):
    """Explicit retrieval: Retrieve a response from the graph based on the provided question using a specific model."""
    llm = ChatOpenAI(
        model='gpt-4',
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2
    )

    chain = GraphCypherQAChain.from_llm(
        graph=graph,
        llm=llm,
        verbose=True,
        allow_dangerous_requests=True
    )
    
    response = chain.invoke({'query': question})
    
    print(response)
    return response

def implicit_retrieve(question):
    """Implicit retrieval: Use an LLM to infer information and answer the question without querying the graph directly."""
    llm = ChatOpenAI(
        model='gpt-4',
        temperature=0,
        max_tokens=2048,
        timeout=None,
        max_retries=2
    )
    
    # Using the LLM directly for open-ended questions
    response = llm(question)
    print(response)
    return response

def generate_creative_sentences(base_sentence):
    """
    Use OpenAI's API to generate creative variations of a base sentence.
    
    :param base_sentence: The input sentence to rephrase.
    :return: A creatively rephrased sentence.
    """

    prompt = f"Rephrase the following sentence in an concise manner:\n'{base_sentence}'"
    
    client = OpenAI(
        api_key=OPENAI_API_KEY,
    )

    completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-4",
    )

    return completion.choices[0].message.content

def get_query_embedding(question):
    """Convert the input question to an embedding using OpenAI."""
    embedding_model = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=OPENAI_API_KEY)
    embedding = embedding_model.embed_query(question)
    return embedding

def vector_search(question, top_k=3):
    """
    Perform a vector search in Neo4j based on the input question and return results in natural language.
    
    :param question: The input question as a string.
    :param top_k: Number of top results to return based on similarity.
    :return: Natural language description of the most similar nodes.
    """
    query_vector = get_query_embedding(question)
    
    with driver.session() as session:
        # Cypher query to perform vector similarity search using GDS
        query = """
        WITH $query_vector AS queryVec
        CALL gds.knn.stream(
            'book1',  
            {
                nodeProperties: ['embedding'],
                topK: $top_k,                       
                similarityCutoff: 0.9
            }
        )
        YIELD node1, node2, similarity
        WITH gds.util.asNode(node1) AS node1, gds.util.asNode(node2) AS node2, similarity
        WHERE node1.name = 'Harry' 
        RETURN node2.name AS Node, similarity
        ORDER BY similarity DESC
        """
        
        # Set up parameters
        params = {
            "query_vector": query_vector,
            "top_k": top_k,
            "nodeProjection": "Person",  
            "nodeProperties": "embedding",  
        }
        
        # Run the query with the input parameters and retrieve top K similar nodes
        result = session.run(query, params)
        
        # Parse the results and return them in natural language
        responses = []
        
        for record in result:
            node2 = record["Node"]  
            base_sentence = f"Harry and {node2} are similar based on the query {question}."
            creative_sentences = generate_creative_sentences(base_sentence)
            responses.append(creative_sentences)
        
        return generate_creative_sentences("\n".join(responses))


if __name__ == "__main__":
    import sys

    # Check if the function name was passed as an argument
    if len(sys.argv) > 1:
        function_name = sys.argv[1]

        # Dynamically call the function by name
        if function_name == "get_schema":
            get_schema()
            
        elif function_name == "explicit_retrieve":
            if len(sys.argv) == 3:  # Expecting the question as an argument
                question = sys.argv[2]
                explicit_retrieve(question)
            else:
                print("Function 'explicit_retrieve' requires one argument: question.")
                
        elif function_name == "implicit_retrieve":
            if len(sys.argv) == 3:  # Expecting the question as an argument
                question = sys.argv[2]
                implicit_retrieve(question)
            else:
                print("Function 'implicit_retrieve' requires one argument: question.") 
                       
        elif function_name == "vector_search":
            if len(sys.argv) >= 3:  # Expecting the question and optional top_k
                question = sys.argv[2]
                top_k = int(sys.argv[3]) if len(sys.argv) > 3 else 3  # Default top_k is 3
                print(vector_search(question, top_k))
            else:
                print("Error: Function 'vector_search' requires at least a question as an argument.")
        else:
            print(f"Function '{function_name}' not recognized.")
    else:
        print("No function specified. Usage: python script.py <function_name> <arguments>")
