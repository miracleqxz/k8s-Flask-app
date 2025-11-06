"""RabbitMQ consumer - process search analytics"""
import pika
import json
import time
from database.rabbitmq_analytics import get_rabbitmq_connection
from database.analytics_db import save_search_analytics


def process_search_event(event):
    """Process single search event"""
    try:
        print(f"📊 Processing: {event['query']} "
              f"(results: {event['results_count']}, "
              f"cached: {event['cached']})")
        
        # Save to database
        save_search_analytics(
            event['query'],
            event['results_count'],
            event['cached']
        )
        
        print(f"   ✅ Saved to DB")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")


def callback(ch, method, properties, body):
    """Callback for message processing"""
    try:
        # Parse JSON
        event = json.loads(body)
        
        # Process event
        process_search_event(event)
        
        # Acknowledge message
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
    except Exception as e:
        print(f"Callback error: {e}")
        # Reject message (requeue)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)


def start_worker():
    """Start analytics worker"""
    print("=" * 50)
    print("🐰 RabbitMQ Analytics Worker")
    print("=" * 50)
    print("\nConnecting to RabbitMQ...")
    
    connection = get_rabbitmq_connection()
    channel = connection.channel()
    
    # Declare queue
    queue_name = 'search_analytics'
    channel.queue_declare(queue=queue_name, durable=True)
    
    # Fair dispatch (process one message at a time)
    channel.basic_qos(prefetch_count=1)
    
    # Start consuming
    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback
    )
    
    print(f"✅ Connected!")
    print(f"📥 Listening to queue: {queue_name}")
    print("\nWaiting for messages... (Ctrl+C to stop)\n")
    
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\n\n⏹️  Stopping worker...")
        channel.stop_consuming()
        connection.close()
        print("✅ Worker stopped")


if __name__ == '__main__':
    start_worker()
