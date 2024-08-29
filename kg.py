from dotenv import load_dotenv
import os
from neo4j import GraphDatabase
import pandas as pd
from xlsx_to_csv import *
import warnings
warnings.filterwarnings("ignore")

load_dotenv()

NEO4J_URI = os.getenv('NEO4J_URI')
NEO4J_USERNAME = os.getenv('NEO4J_USERNAME')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')

URI = NEO4J_URI
AUTH = (NEO4J_USERNAME, NEO4J_PASSWORD)

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()

combine_data()

def create_characters(tx, name):
    tx.run("MERGE (p:Person {name: $name})", name=name)

def create_relationship(tx, person1, relationship, person2, attributes):
    safe_relationship = relationship.replace(" ", "_").upper()

    query = (
        f"MATCH (a:Person {{name: $person1}}), (b:Person {{name: $person2}}) "
        f"MERGE (a)-[r:{safe_relationship}]->(b) "
        "SET r += $attributes"
    )
    
    tx.run(query, person1=person1, person2=person2, attributes=attributes)
    
def count_nodes(tx):
    result = tx.run("MATCH (n) RETURN COUNT(n) AS node_count")
    return result.single()["node_count"]

def count_relationships(tx):
    result = tx.run("MATCH ()-[r]->() RETURN COUNT(r) AS relationship_count")
    return result.single()["relationship_count"]

def create_kg():
    with driver.session() as session:
        with open('./data/combined_data.csv', 'r') as file:
            # Define Harry and relationship types
            session.write_transaction(create_characters, 'Harry')
            titles = next(file)
            titles = titles.strip().split(',')[1:]
            titles = [title.upper() for title in titles]
            
            for line in file:
                name = line.strip().split(',')[0]
                relationships = line.strip().split(',')[1:]
                session.write_transaction(create_characters, name) # Create nodes
                relations = dict(zip(titles, relationships)) # Create relationships
                existing_relations = [key for key, value in relations.items() if int(value) == 1]
                
                for existing_relation in existing_relations:
                    session.write_transaction(create_relationship, 'Harry', existing_relation, name, {})
                    session.write_transaction(create_relationship, name, existing_relation, 'Harry', {})
                    
            node_count = session.write_transaction(count_nodes)
            relationship_count = session.write_transaction(count_relationships)
            
            print(f'Knowledge Graph created with {node_count} nodes and {relationship_count} relationships.')

    driver.close()

if __name__ == "__main__":
    create_kg()
