
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError, TransportError
from config import Config


def check_elasticsearch():

    try:
        es_url = f"http://{Config.ELASTICSEARCH_HOST}:{Config.ELASTICSEARCH_PORT}"
        es = Elasticsearch([es_url], request_timeout=10)
        
        # Ping
        if not es.ping():
            return {
                'status': 'unhealthy',
                'service': 'elasticsearch',
                'message': 'Elasticsearch ping failed'
            }
        
        
        info = es.info()
        
        
        health = es.cluster.health()
        
        
        stats = es.cluster.stats()
        
        
        nodes_info = es.nodes.info()
        nodes_count = len(nodes_info['nodes'])
        
        
        indices = es.cat.indices(format='json')
        total_indices = len(indices)
        
        
        total_docs = sum(int(idx.get('docs.count', 0) or 0) for idx in indices)
        
        # Movies index specific stats
        movies_stats = None
        try:
            movies_idx = es.cat.indices(index='movies', format='json')
            if movies_idx:
                movies_stats = {
                    'documents': int(movies_idx[0].get('docs.count', 0) or 0),
                    'size': movies_idx[0].get('store.size', 'N/A'),
                    'health': movies_idx[0].get('health', 'N/A')
                }
        except:
            movies_stats = None
        
        # Search performance (safe access)
        search_stats = stats.get('indices', {}).get('search', {})
        query_total = search_stats.get('query_total', 0)
        query_time = search_stats.get('query_time_in_millis', 0)
        avg_query_time = round(query_time / query_total, 2) if query_total > 0 else 0
        
        es.close()
        
        return {
            'status': 'healthy',
            'service': 'elasticsearch',
            'message': 'Successfully connected to Elasticsearch',
            'details': {
                'connection': {
                    'host': Config.ELASTICSEARCH_HOST,
                    'port': Config.ELASTICSEARCH_PORT,
                    'cluster_name': info.get('cluster_name', 'N/A')
                },
                'version': {
                    'number': info.get('version', {}).get('number', 'N/A'),
                    'lucene_version': info.get('version', {}).get('lucene_version', 'N/A')
                },
                'cluster_health': {
                    'status': health.get('status', 'N/A'),
                    'nodes': health.get('number_of_nodes', 0),
                    'data_nodes': health.get('number_of_data_nodes', 0),
                    'active_shards': health.get('active_shards', 0),
                    'relocating_shards': health.get('relocating_shards', 0),
                    'unassigned_shards': health.get('unassigned_shards', 0)
                },
                'indices': {
                    'total_indices': total_indices,
                    'total_documents': total_docs
                },
                'movies_index': movies_stats,
                'performance': {
                    'total_searches': query_total,
                    'search_time_ms': query_time,
                    'avg_search_time_ms': avg_query_time
                }
            }
        }
        
    except ConnectionError as e:
        return {
            'status': 'unhealthy',
            'service': 'elasticsearch',
            'message': f'Connection error: {str(e)}'
        }
    except TransportError as e:
        return {
            'status': 'unhealthy',
            'service': 'elasticsearch',
            'message': f'Transport error: {str(e)}'
        }
    except Exception as e:
        return {
            'status': 'unhealthy',
            'service': 'elasticsearch',
            'message': f'Unexpected error: {str(e)}'
        }
