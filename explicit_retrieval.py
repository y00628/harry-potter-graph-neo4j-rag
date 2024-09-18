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
    
    
create_kg()

graph = Neo4jGraph()

def get_schema():
    
    graph.refresh_schema()
    return graph.schema

def retrieve(model_name, question):
    llm = ChatOpenAI(
        model=model_name,
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2
    )

    chain = GraphCypherQAChain.from_llm(graph=graph, llm=llm, verbose=True)
    response = chain.invoke({'query': question})
    
    return response

