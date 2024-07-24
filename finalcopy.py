import requests
from bs4 import BeautifulSoup
import spacy
from datetime import datetime
from py2neo import Graph, Node, Relationship
import openai
import psycopg2
import json

# Load spacy model fro nlp, mkae sure u have it downloaded
nlp = spacy.load("en_core_web_sm")

# Connect 2 neo4j
graph = Graph("bolt://localhost:7687", auth=("neo4j", "samraat21"))
openai.api_key = 'ENETRYOUROWNKEY!!!!!!'

# URL of whatevre page or article we need
URL = "https://edition.cnn.com/2024/07/15/style/ambani-wedding-mumbai-modi-kardashian/index.html"
content = requests.get(URL)

soup = BeautifulSoup(content.content, "lxml")
paragraphs = soup.find_all('p')
titles = soup.find_all(['h1', 'h2'])
publication_date = soup.find('meta', attrs={'name': 'pubdate'}) or soup.find('meta', attrs={'name': 'date'})

# Append all titles into a list because it looks neater and better retrievak whenever needed ofc
title_list = [title.get_text() for title in titles]

# Merge all paragraphs into a single string !!
paragraph_text = ' '.join([paragraph.get_text() for paragraph in paragraphs])

# Performinf ner using spacy,setting up a label map because netb said so STUDY WHYY
doc = nlp(paragraph_text)
entity_label_map = {
    'PERSON': 'Famous_Person',
    'ORG': 'Organization',
    'GPE': 'Political_Influence',
    'LOC': 'Location',
    'GRP': 'Group',
    'EVENT': 'Event',
    'WORK_OF_ART': 'Creative_Work',
    'PRODUCT': 'Product',
}
entities = [(ent.text, entity_label_map.get(ent.label_, ent.label_)) for ent in doc.ents]
keywords = [token.text for token in doc if token.is_alpha and not token.is_stop]

# Extracting publication date PLEASE WORKK
if publication_date:
    pub_date = publication_date.get('content')
    if pub_date:
        try:
            publication_date = datetime.fromisoformat(pub_date).strftime('%Y-%m-%d')
        except ValueError:
            publication_date = None
    else:
        publication_date = None
else:
    publication_date = None

url = URL

# Output results to check if we're moving in the right direction
print("Titles:", title_list)
print("Publication Date:", publication_date)
print("URL:", url)
print("Paragraph:", paragraph_text)
print("Entities:", entities)
print("Keywords:", keywords)

# Function to analyze article via open ai api, wast stuck on this for a while asked gpt and internt told me to use json array , worked
def analyze_content_with_openai(text, entities):
    entity_string = "; ".join([f"{ent[0]} ({ent[1]})" for ent in entities])
    prompt = (
        f"Entities: {entity_string}\n\n"
        f"Article: {text}\n\n"
        "Analyze the above article and identify relationships between entities, "
        "including familial relationships (e.g., father, mother, sibling), cause-and-effect relationships, "
        "and other implied relationships. Return the relationships in the format of a JSON array of dictionaries."
    )
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a knowledgeable assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500  # Used thoda extra token limit bcz text ended abruptly causing parsing issues
    )
    
    response_text = response['choices'][0]['message']['content'].strip()

    # Ensure the response is a valid JSON string otherwise idk erros aate just work plz
    try:
        relationships_list = json.loads(response_text)
    except json.JSONDecodeError:
        relationships_list = []
    
    return relationships_list

relationships_list = analyze_content_with_openai(paragraph_text, entities)
print("Additional Relationships Identified by OpenAI:", relationships_list)

# Display a portion of new relationsjips
print("Displaying a bit of new relationsips:")
for i, rel in enumerate(relationships_list[:5]):  # Display the first 5 relationships
    print(f"Relationship {i+1}: {rel}")

# Establish the graph inneo4j
def create_knowledge_graph():
    # Create Article node
    article_node = Node("Article", title=title_list[0] if title_list else None, publication_date=publication_date, url=url, content=paragraph_text)
    graph.create(article_node)

    # Create Title node
    if title_list:
        title_node = Node("Title", name=title_list[0])
        graph.create(Relationship(article_node, "HAS_TITLE", title_node))

    # Create Entity nodes
    entity_nodes = {}
    for entity_text, entity_label in entities:
        if entity_text not in entity_nodes:
            entity_node = Node(entity_label, name=entity_text)
            graph.create(entity_node)
            entity_nodes[entity_text] = entity_node
        graph.create(Relationship(article_node, "MENTIONS", entity_nodes[entity_text]))

    # Create and link Keyword nodes
    keyword_nodes = {}
    for keyword in keywords:
        if keyword not in keyword_nodes:
            keyword_node = Node("Keyword", name=keyword)
            graph.create(keyword_node)
            keyword_nodes[keyword] = keyword_node
        graph.create(Relationship(article_node, "CONTAINS_KEYWORD", keyword_nodes[keyword]))

    # For api rels
    for rel in relationships_list:
        try:
            entity1, relationship, entity2 = rel['entity1'], rel['relationship'].replace(' ', '_').upper(), rel['entity2']
            if entity1 in entity_nodes and entity2 in entity_nodes:
                graph.create(Relationship(entity_nodes[entity1], relationship, entity_nodes[entity2]))
        except Exception as e:
            print(f"Error processing relationship '{rel}': {e}")
            continue

create_knowledge_graph()

# Establish links between articles based on shared keywords
def create_article_relationships():
    articles = graph.nodes.match("Article").all()
    for i in range(len(articles)):
        for j in range(i + 1, len(articles)):
            keywords_i = set(rel.end_node["name"] for rel in graph.match((articles[i],), r_type="CONTAINS_KEYWORD"))
            keywords_j = set(rel.end_node["name"] for rel in graph.match((articles[j],), r_type="CONTAINS_KEYWORD"))
            shared_keywords = keywords_i.intersection(keywords_j)
            if shared_keywords:
                graph.create(Relationship(articles[i], "SHARES_KEYWORD_WITH", articles[j], shared_keywords=list(shared_keywords)))

create_article_relationships()

# Database Schema first time using postgres so just used docs and stackoverflow help
def create_database_schema():
    conn = psycopg2.connect(
        dbname="postgres", 
        user="postgres", 
        password="samraat21", 
        host="localhost"
    )
    cursor = conn.cursor()

    # Drop tables because god knows how many times my work has fialed ugh
    cursor.execute("DROP TABLE IF EXISTS relationships")
    cursor.execute("DROP TABLE IF EXISTS entities")
    cursor.execute("DROP TABLE IF EXISTS articles")

    # Create tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id SERIAL PRIMARY KEY,
            title TEXT,
            publication_date DATE,
            url TEXT,
            content TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS entities (
            id SERIAL PRIMARY KEY,
            name TEXT UNIQUE,
            label TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id SERIAL PRIMARY KEY,
            article_id INTEGER REFERENCES articles(id),
            entity1_name TEXT,
            entity2_name TEXT,
            relationship_type TEXT
        )
    """)
    
    conn.commit()
    cursor.close()
    conn.close()

# Function to store data 
def store_data_in_db(article, entities, relationships_list):
    conn = psycopg2.connect(
        dbname="postgres", 
        user="postgres", 
        password="samraat21", 
        host="localhost"
    )
    cursor = conn.cursor()
    
    # Insert article data
    cursor.execute("""
        INSERT INTO articles (title, publication_date, url, content) 
        VALUES (%s, %s, %s, %s) RETURNING id
    """, (article['title'], article['publication_date'], article['url'], article['content']))
    article_id = cursor.fetchone()[0]
    
    # Insert entity data
    for entity in entities:
        cursor.execute("""
            INSERT INTO entities (name, label) 
            VALUES (%s, %s) ON CONFLICT (name) DO NOTHING
        """, (entity['name'], entity['label']))
    
    # Insert relationship data
    for rel in relationships_list:
        try:
            entity1, relationship, entity2 = rel['entity1'], rel['relationship'].replace(' ', '_').upper(), rel['entity2']
            cursor.execute("""
                INSERT INTO relationships (article_id, entity1_name, entity2_name, relationship_type) 
                VALUES (%s, %s, %s, %s)
            """, (article_id, entity1.strip(), entity2.strip(), relationship.strip()))
        except Exception as e:
            print(f"Error inserting relationship '{rel}': {e}")
    
    conn.commit()
    cursor.close()
    conn.close()

article_data = {
    'title': title_list[0] if title_list else None,
    'publication_date': publication_date if publication_date else None,
    'url': url,
    'content': paragraph_text
}
entity_data = [{'name': ent[0], 'label': ent[1]} for ent in entities]
relationship_data = [{'entity1': rel['entity1'].strip(), 'relationship': rel['relationship'].strip(), 'entity2': rel['entity2'].strip()} for rel in relationships_list]

create_database_schema()
store_data_in_db(article_data, entity_data, relationship_data)
