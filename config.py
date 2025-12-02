import os


class Config:
    
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'postgres.service-checker.svc.cluster.local')
    POSTGRES_PORT = int(os.getenv('POSTGRES_PORT', '5432'))
    POSTGRES_DB = os.getenv('POSTGRES_DB', 'postgres')
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
    
    
    REDIS_HOST = os.getenv('REDIS_HOST', 'redis.service-checker.svc.cluster.local')
    REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))
    

    RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq.service-checker.svc.cluster.local')
    RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', '5672'))
    RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'guest')
    RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'guest')
    
    
    ELASTICSEARCH_HOST = os.getenv('ELASTICSEARCH_HOST', 'elasticsearch.service-checker.svc.cluster.local')
    ELASTICSEARCH_PORT = int(os.getenv('ELASTICSEARCH_PORT', '9200'))
    
    
    MINIO_HOST = os.getenv('MINIO_HOST', 'minio.service-checker.svc.cluster.local')
    MINIO_PORT = int(os.getenv('MINIO_PORT', '9000'))
    MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY', 'minioadmin')
    MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY', 'minioadmin')
    
    
    CONSUL_HOST = os.getenv('CONSUL_HOST', 'consul.service-checker.svc.cluster.local')
    CONSUL_PORT = int(os.getenv('CONSUL_PORT', '8500'))
    
    
    PROMETHEUS_HOST = os.getenv('PROMETHEUS_HOST', 'prometheus.service-checker.svc.cluster.local')
    PROMETHEUS_PORT = int(os.getenv('PROMETHEUS_PORT', '9090'))
    
    
    NGINX_HOST = os.getenv('NGINX_HOST', 'ingress-nginx-controller.ingress-nginx.svc.cluster.local')
    NGINX_PORT = int(os.getenv('NGINX_PORT', '80'))
    
    
    GRAFANA_HOST = os.getenv('GRAFANA_HOST', 'grafana.service-checker.svc.cluster.local')
    GRAFANA_PORT = int(os.getenv('GRAFANA_PORT', '3000'))
    
    
    LOKI_HOST = os.getenv('LOKI_HOST', 'loki.service-checker.svc.cluster.local')
    LOKI_PORT = int(os.getenv('LOKI_PORT', '3100'))
    

    TMDB_API_KEY = os.getenv('TMDB_API_KEY', '')
    

    HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    PORT = int(os.getenv('FLASK_PORT', '5000'))
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'