import os
from dotenv import load_dotenv


environment = os.getenv('ENV', 'local')

if environment == 'k8s':
    load_dotenv('.env.k8s')
else:
    load_dotenv('.env.local')

print(f"env: {environment}")

class Config:
    
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', '5000'))
    

    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT = int(os.getenv('POSTGRES_PORT', '5432'))
    POSTGRES_DB = os.getenv('POSTGRES_DB', 'testdb')
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
    

    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))


    RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
    RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', '5672'))
    RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'guest')
    RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'guest')
    

    ELASTICSEARCH_HOST = os.getenv('ELASTICSEARCH_HOST', 'localhost')
    ELASTICSEARCH_PORT = int(os.getenv('ELASTICSEARCH_PORT', '9200'))
    

    MINIO_HOST = os.getenv('MINIO_HOST', 'localhost')
    MINIO_PORT = int(os.getenv('MINIO_PORT', '9000'))
    MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY', 'minioadmin')
    MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY', 'minioadmin')
    
    
    CONSUL_HOST = os.getenv('CONSUL_HOST', 'localhost')
    CONSUL_PORT = int(os.getenv('CONSUL_PORT', '8500'))
    
    
    PROMETHEUS_HOST = os.getenv('PROMETHEUS_HOST', 'localhost')
    PROMETHEUS_PORT = int(os.getenv('PROMETHEUS_PORT', '9090'))
