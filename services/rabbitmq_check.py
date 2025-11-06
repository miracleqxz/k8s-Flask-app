
import pika
from config import Config


def check_rabbitmq():
    try:
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
        
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        
        # Test queue
        queue_name = 'health_check_queue'
        channel.queue_declare(queue=queue_name, durable=False)
        
        # Send test message
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body='Health check'
        )
        
        # Get queue info
        queue_info = channel.queue_declare(queue=queue_name, passive=True)
        message_count = queue_info.method.message_count
        
        # Get all queues
        import requests
        try:
            api_url = f"http://{Config.RABBITMQ_HOST}:15672/api/queues"
            auth = (Config.RABBITMQ_USER, Config.RABBITMQ_PASSWORD)
            queues_response = requests.get(api_url, auth=auth, timeout=3)
            all_queues = len(queues_response.json()) if queues_response.status_code == 200 else 'N/A'
            
            
            conn_url = f"http://{Config.RABBITMQ_HOST}:15672/api/connections"
            conn_response = requests.get(conn_url, auth=auth, timeout=3)
            total_connections = len(conn_response.json()) if conn_response.status_code == 200 else 'N/A'
            
            
            chan_url = f"http://{Config.RABBITMQ_HOST}:15672/api/channels"
            chan_response = requests.get(chan_url, auth=auth, timeout=3)
            total_channels = len(chan_response.json()) if chan_response.status_code == 200 else 'N/A'
        except:
            all_queues = 'N/A'
            total_connections = 'N/A'
            total_channels = 'N/A'
        
        connection.close()
        
        return {
            'status': 'healthy',
            'service': 'rabbitmq',
            'message': 'Successfully connected to RabbitMQ',
            'details': {
                'connection': {
                    'host': Config.RABBITMQ_HOST,
                    'port': Config.RABBITMQ_PORT,
                    'total_connections': total_connections,
                    'total_channels': total_channels
                },
                'queues': {
                    'total_queues': all_queues,
                    'test_queue': queue_name,
                    'messages_in_test_queue': message_count
                },
                'test_result': {
                    'message_published': True,
                    'queue_accessible': True
                }
            }
        }
        
    except pika.exceptions.AMQPConnectionError as e:
        return {
            'status': 'unhealthy',
            'service': 'rabbitmq',
            'message': f'Connection error: {str(e)}'
        }
    except Exception as e:
        return {
            'status': 'unhealthy',
            'service': 'rabbitmq',
            'message': f'Unexpected error: {str(e)}'
        }
