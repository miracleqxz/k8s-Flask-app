"""Application configuration"""
import os
from dotenv import load_dotenv

# Load environment-specific .env file
env = os.getenv('ENV', 'local')
env_file = f'.env.{env}'

if os.path.exists(env_file):
    load_dotenv(env_file)
    print(f"env: {env}")
else:
    print(f"env: {env} (using system environment variables)")


class Config:
    
    
    POSTGRES_HOST = os.getenv('APP_POSTGRES_HOST', os.getenv('POSTGRES_HOST', 'localhost'))
    POSTGRES_PORT = int(os.getenv('APP_POSTGRES_PORT', os.getenv('POSTGRES_PORT', '5432')))
    POSTGRES_DB = os.getenv('APP_POSTGRES_DB', os.getenv('POSTGRES_DB', 'postgres'))
    POSTGRES_USER = os.getenv('APP_POSTGRES_USER', os.getenv('POSTGRES_USER', 'postgres'))
    POSTGRES_PASSWORD = os.getenv('APP_POSTGRES_PASSWORD', os.getenv('POSTGRES_PASSWORD', 'postgres'))
    
    
    REDIS_HOST = os.getenv('APP_REDIS_HOST', os.getenv('REDIS_HOST', 'localhost'))
    REDIS_PORT = int(os.getenv('APP_REDIS_PORT', os.getenv('REDIS_PORT', '6379')))
    
    
    RABBITMQ_HOST = os.getenv('APP_RABBITMQ_HOST', os.getenv('RABBITMQ_HOST', 'localhost'))
    RABBITMQ_PORT = int(os.getenv('APP_RABBITMQ_PORT', os.getenv('RABBITMQ_PORT', '5672')))
    RABBITMQ_USER = os.getenv('APP_RABBITMQ_USER', os.getenv('RABBITMQ_USER', 'guest'))
    RABBITMQ_PASSWORD = os.getenv('APP_RABBITMQ_PASSWORD', os.getenv('RABBITMQ_PASSWORD', 'guest'))
    
    
    ELASTICSEARCH_HOST = os.getenv('APP_ELASTICSEARCH_HOST', os.getenv('ELASTICSEARCH_HOST', 'localhost'))
    ELASTICSEARCH_PORT = int(os.getenv('APP_ELASTICSEARCH_PORT', os.getenv('ELASTICSEARCH_PORT', '9200')))
    
    
    MINIO_HOST = os.getenv('APP_MINIO_HOST', os.getenv('MINIO_HOST', 'localhost'))
    MINIO_PORT = int(os.getenv('APP_MINIO_PORT', os.getenv('MINIO_PORT', '9000')))
    MINIO_ACCESS_KEY = os.getenv('APP_MINIO_ACCESS_KEY', os.getenv('MINIO_ACCESS_KEY', 'minioadmin'))
    MINIO_SECRET_KEY = os.getenv('APP_MINIO_SECRET_KEY', os.getenv('MINIO_SECRET_KEY', 'minioadmin'))
    
    
    CONSUL_HOST = os.getenv('APP_CONSUL_HOST', os.getenv('CONSUL_HOST', 'localhost'))
    CONSUL_PORT = int(os.getenv('APP_CONSUL_PORT', os.getenv('CONSUL_PORT', '8500')))
    
    
    PROMETHEUS_HOST = os.getenv('APP_PROMETHEUS_HOST', os.getenv('PROMETHEUS_HOST', 'localhost'))
    PROMETHEUS_PORT = int(os.getenv('APP_PROMETHEUS_PORT', os.getenv('PROMETHEUS_PORT', '9090')))
    
    
    TMDB_API_KEY = os.getenv('TMDB_API_KEY', '')
