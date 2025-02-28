import os
import django
import pika
import json
import logging
#from  .emil import send_transaction_email

# Set up Django
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LMS.settings")
#django.setup()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Use environment variable for RabbitMQ URL
RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqps://defhsify:omnBvSPMX35gPEvr2LscqyuB1FFSbdU2@cougar.rmq.cloudamqp.com/defhsify")

def callback(ch, method, properties, body):
    try:
        message = json.loads(body)
        user_id = message.get('user_id')
        transaction_id = message.get('transaction_id')

        if user_id and transaction_id:
#           send_transaction_email(user_id, transaction_id)
            logger.info(f"Email sent for transaction {transaction_id}")
        else:
            logger.warning("Invalid message format received")

        # Acknowledge the message
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logger.error(f"Error processing message: {e}")

def start_worker():
    try:
        # Establish RabbitMQ connection
        params = pika.URLParameters(RABBITMQ_URL)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()

        # Declare the queue (ensure it exists)
        channel.queue_declare(queue='transaction_email_queue', durable=True)

        # Set up message consumption
        channel.basic_consume(queue='transaction_email_queue', on_message_callback=callback)

        logger.info("Email worker started, waiting for messages...")
        channel.start_consuming()
    except pika.exceptions.AMQPConnectionError as e:
        logger.error(f"Failed to connect to RabbitMQ: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        if 'connection' in locals() and connection.is_open:
            connection.close()

if __name__ == '__main__':
    start_worker()