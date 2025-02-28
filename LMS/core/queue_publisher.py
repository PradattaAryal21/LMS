import pika
import json
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Use environment variable for RabbitMQ URL
RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqps://defhsify:omnBvSPMX35gPEvr2LscqyuB1FFSbdU2@cougar.rmq.cloudamqp.com/defhsify")

def publish_transaction_email(user_id, transaction_id):
    try:
        # Establish RabbitMQ connection
        params = pika.URLParameters(RABBITMQ_URL)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()

     
        channel.queue_declare(queue='transaction_email_queue', durable=True)

        # Prepare the message
        message = json.dumps({'user_id': user_id, 'transaction_id': transaction_id})

        # Publish the message
        channel.basic_publish(
            exchange='',
            routing_key='transaction_email_queue',
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent
            )
        )

        logger.info(f"Published email task to queue for user {user_id} and transaction {transaction_id}")
    except Exception as e:
        logger.error(f"Error publishing message to RabbitMQ: {e}")
    finally:
        if 'connection' in locals() and connection.is_open:
            connection.close()

# Example usage
if __name__ == '__main__':
    publish_transaction_email(user_id=123, transaction_id=456)