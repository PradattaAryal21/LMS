import os
import pika
import json
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "healthcaretestkutumba@gmail.com"
EMAIL_HOST_PASSWORD = "yhyn apnz fjlx ktzw"
DEFAULT_FROM_EMAIL = "pradattaaryal11@gmail.com"

RABBITMQ_URL = os.getenv(
    "RABBITMQ_URL",
    "amqp://guest:guest@localhost:5672/"
)

PREFETCH_COUNT = 10
MAX_RETRIES = 5
INITIAL_RETRY_DELAY = 5

def send_email_smtp(to_email, subject, message_text):
    try:
        msg = MIMEMultipart()
        msg['From'] = DEFAULT_FROM_EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message_text, 'plain'))
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        text = msg.as_string()
        server.sendmail(DEFAULT_FROM_EMAIL, to_email, text)
        server.quit()
        return True
    except Exception:
        return False

def callback(ch, method, properties, body):
    try:
        email_data = json.loads(body)
        email = email_data.get("email")
        subject = email_data.get("subject")
        message = email_data.get("message")
        if email and subject and message:
            success = send_email_smtp(email, subject, message)
            if success:
                ch.basic_ack(delivery_tag=method.delivery_tag)
            else:
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)
    except json.JSONDecodeError:
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception:
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

def establish_connection():
    retry_count = 0
    retry_delay = INITIAL_RETRY_DELAY
    while retry_count < MAX_RETRIES:
        try:
            params = pika.URLParameters(RABBITMQ_URL)
            params.heartbeat = 600
            connection = pika.BlockingConnection(params)
            channel = connection.channel()
            channel.queue_declare(queue='transaction_email_queue', durable=True)
            channel.basic_qos(prefetch_count=PREFETCH_COUNT)
            return connection, channel
        except pika.exceptions.AMQPConnectionError:
            retry_count += 1
            if retry_count < MAX_RETRIES:
                time.sleep(retry_delay)
                retry_delay *= 2
            else:
                return None, None
        except Exception:
            retry_count += 1
            if retry_count < MAX_RETRIES:
                time.sleep(retry_delay)
                retry_delay *= 2
            else:
                return None, None

def start_worker():
    while True:
        try:
            connection, channel = establish_connection()
            if not connection or not channel:
                time.sleep(60)
                continue
            channel.basic_consume(
                queue='transaction_email_queue', 
                on_message_callback=callback,
                auto_ack=False
            )
            channel.start_consuming()
        except pika.exceptions.ConnectionClosedByBroker:
            break
        except pika.exceptions.AMQPChannelError:
            break
        except pika.exceptions.AMQPConnectionError:
            time.sleep(5)
        except KeyboardInterrupt:
            if connection and connection.is_open:
                connection.close()
            break
        except Exception:
            if connection and connection.is_open:
                connection.close()
            time.sleep(5)

if __name__ == '__main__':
    start_worker()