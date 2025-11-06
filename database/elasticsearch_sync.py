
from elasticsearch import Elasticsearch
from config import Config
from database.movies_db import get_all_movies


def get_es_client():
    es_url = f"http://{Config.ELASTICSEARCH_HOST}:{Config.ELASTICSEARCH_PORT}"
    return Elasticsearch([es_url], request_timeout=10)


def create_movies_index():
    es = get_es_client()
    
    index_name = 'movies'
    
    
    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)
        print(f"Deleted existing index: {index_name}")
    
    
    settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0,
            "analysis": {
                "analyzer": {
                    "movie_search_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": [
                            "lowercase",
                            "asciifolding",
                            "english_stop",
                            "english_stemmer"
                        ]
                    },
                    "edge_ngram_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": [
                            "lowercase",
                            "edge_ngram_filter"
                        ]
                    }
                },
                "filter": {
                    "english_stop": {
                        "type": "stop",
                        "stopwords": "_english_"
                    },
                    "english_stemmer": {
                        "type": "stemmer",
                        "language": "english"
                    },
                    "edge_ngram_filter": {
                        "type": "edge_ngram",
                        "min_gram": 2,
                        "max_gram": 15
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "id": {"type": "integer"},
                "title": {
                    "type": "text",
                    "analyzer": "movie_search_analyzer",
                    "fields": {
                        "keyword": {"type": "keyword"},
                        "edge_ngram": {
                            "type": "text",
                            "analyzer": "edge_ngram_analyzer",
                            "search_analyzer": "movie_search_analyzer"
                        }
                    }
                },
                "year": {"type": "integer"},
                "rating": {"type": "float"},
                "genre": {
                    "type": "text",
                    "analyzer": "movie_search_analyzer",
                    "fields": {
                        "keyword": {"type": "keyword"}
                    }
                },
                "director": {
                    "type": "text",
                    "analyzer": "movie_search_analyzer",
                    "fields": {
                        "keyword": {"type": "keyword"}
                    }
                },
                "description": {
                    "type": "text",
                    "analyzer": "movie_search_analyzer"
                },
                "poster_filename": {"type": "keyword"}
            }
        }
    }
    
    
    es.indices.create(index=index_name, body=settings)
    print(f"Created index: {index_name}")
    
    es.close()

def index_all_movies():
    es = get_es_client()
    
    movies = get_all_movies()
    

    print(f"Indexing {len(movies)} movies...")
    

    for i, movie in enumerate(movies, 1):
        doc = {
            'id': movie['id'],
            'title': movie['title'],
            'year': movie['year'],
            'rating': float(movie['rating']),
            'genre': movie['genre'],
            'director': movie['director'],
            'description': movie['description'],
            'poster_filename': movie['poster_filename']
        }
        
        es.index(index='movies', id=movie['id'], document=doc)
        print(f"  {i}.{movie['title']}")
    
    
    es.indices.refresh(index='movies')
    
    es.close()
    print(f"\nIndexed {len(movies)} movies!")



def search_movies_es(query, size=20):
    es = get_es_client()
    
    query_length = len(query.strip())
    
    # Build strategies based on query length
    should_clauses = []
    
    # Strategy 1: Exact phrase match (always)
    should_clauses.extend([
        {
            "match_phrase": {
                "title": {
                    "query": query,
                    "boost": 10
                }
            }
        },
        {
            "match_phrase": {
                "description": {
                    "query": query,
                    "boost": 5
                }
            }
        }
    ])
    
    # Strategy 2: Multi-match with controlled fuzziness
    if query_length >= 4:
        # Only use fuzziness for queries 4+ chars
        should_clauses.append({
            "multi_match": {
                "query": query,
                "fields": [
                    "title^8",
                    "description^4",
                    "director^3",
                    "genre^2"
                ],
                "type": "best_fields",
                "operator": "or",
                "fuzziness": "AUTO"
            }
        })
    else:
        # For short queries - exact matching only
        should_clauses.append({
            "multi_match": {
                "query": query,
                "fields": [
                    "title^8",
                    "director^3",
                    "genre^2"
                ],
                "type": "best_fields",
                "operator": "and"  # all terms must match
            }
        })
    
    # Strategy 3: Edge ngram (only for 3+ chars)
    if query_length >= 3:
        should_clauses.append({
            "match": {
                "title.edge_ngram": {
                    "query": query,
                    "boost": 6
                }
            }
        })
    
    # Strategy 4: Wildcard (only for 4+ chars)
    if query_length >= 4:
        should_clauses.append({
            "wildcard": {
                "title.keyword": {
                    "value": f"*{query.lower()}*",
                    "boost": 3,
                    "case_insensitive": True
                }
            }
        })
    
    search_query = {
        "query": {
            "bool": {
                "should": should_clauses,
                "minimum_should_match": 1
            }
        },
        "min_score": 1.0,  # filter weak matches
        "size": size,
        "sort": [
            {"_score": {"order": "desc"}},
            {"rating": {"order": "desc"}}
        ]
    }
    
    response = es.search(index='movies', body=search_query)
    
    results = []
    for hit in response['hits']['hits']:
        movie = hit['_source']
        movie['score'] = hit['_score']
        results.append(movie)
    
    es.close()
    
    return results




def get_movies_count_es():
    """Get total movies count in ES"""
    es = get_es_client()
    count = es.count(index='movies')['count']
    es.close()
    return count
