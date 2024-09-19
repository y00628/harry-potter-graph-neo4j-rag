from dotenv import load_dotenv
import os
from neo4j import GraphDatabase
import pandas as pd
from xlsx_to_csv import *
from kg import *
from langchain_community.graphs import Neo4jGraph
from langchain.chains import GraphCypherQAChain
from langchain_openai import ChatOpenAI
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
    
    
# create_kg() # Should've already been created

graph = Neo4jGraph()

def get_schema():
    """Refresh and return the graph schema."""
    graph.refresh_schema()
    schema = graph.schema
    print(schema)
    return schema

def retrieve(question):
    """Retrieve a response from the graph based on the provided question using a specific model."""
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

if __name__ == "__main__":
    import sys

    # Check if the function name was passed as an argument
    if len(sys.argv) > 1:
        function_name = sys.argv[1]

        # Dynamically call the function by name
        if function_name == "get_schema":
            get_schema()
        elif function_name == "retrieve":
            if len(sys.argv) == 3:  # Expecting model name and question as arguments
                question = sys.argv[2]
                retrieve(question)
            else:
                print("Function 'retrieve' requires one argument: question.")
        else:
            print(f"Function '{function_name}' not recognized.")
    else:
        print("No function specified. Usage: py explicit_retrieval.py <function_name> <arguments>")
