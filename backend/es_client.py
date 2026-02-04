"""
es_client.py

Initialize Elasticsearch client.

- INDEX_NAME: Name of the index where LinkedIn profiles will be stored.
- es: Elasticsearch client connected to the local server at http://localhost:9200.
"""
from elasticsearch import Elasticsearch

INDEX_NAME = "linkedin_profiles"
es = Elasticsearch("http://localhost:9200")
