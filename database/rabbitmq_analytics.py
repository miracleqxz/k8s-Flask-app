
import pika
import json
from config import Config
from datetime import datetime


def get_rabbitmq_connection():
    credentials = pika.PlainCredentials(
        Config.RABBITMQ_USER,
        Config.RABBITMQ_PASSWORD
    )
    
    parameters = pika.ConnectionParameters(
        host=Config.RABBITMQ_HOST,
        port=Config.RABBITMQ_PORT,
        credentials=credentials,
        connection_attempts=3,
        retry_delay=2
    )
    
    return pika.BlockingConnection(parameters)


def publish_search_event(query, results_count, cached=False):
    try:
        connection = get_rabbitmq_connection()
        channel = connection.channel()
        
        # Declare queue
        queue_name = 'search_analytics'
        channel.queue_declare(queue=queue_name, durable=True)
        
        # Create event
        event = {
            'query': query,
            'results_count': results_count,
            'cached': cached,
            'timestamp': datetime.now().isoformat()
        }
        
        # Publish message
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=json.dumps(event),
            properties=pika.BasicProperties(
                delivery_mode=2  # Make message persistent
            )
        )
        
        connection.close()
        
    except Exception as e:
        print(f"RabbitMQ publish error: {e}")


def get_queue_stats():
    """Get queue statistics"""
    try:
        connection = get_rabbitmq_connection()
        channel = connection.channel()
        
        queue_name = 'search_analytics'
        queue = channel.queue_declare(queue=queue_name, passive=True)
        
        stats = {
            'queue_name': queue_name,
            'messages': queue.method.message_count,
            'consumers': queue.method.consumer_count
        }
        
        connection.close()
        return stats
        
    except Exception as e:
        print(f"RabbitMQ stats error: {e}")
        return None
