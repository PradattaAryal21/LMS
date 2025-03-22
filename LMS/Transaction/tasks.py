# Transaction/tasks.py

import logging
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from Transaction.models import Transaction

logger = logging.getLogger(__name__)

@shared_task
def send_transaction_email(transaction_id):
    try:
        # Fetch transaction details
        transaction = Transaction.objects.select_related("student").get(transaction_id=transaction_id)
        student = transaction.student

        # Prepare email data
        subject = "Transaction Completed Successfully"
        message = f"""
        Hello {student.name},

        Your transaction has beenxxxxxxxxxxxxxxxxxxxxxxx successfully completed.

        Transaction ID: {transaction.transaction_id}
        Book: {transaction.book_name}
        Transaction Type: {transaction.get_transaction_type_display()}
        Date: {transaction.date.strftime('%Y-%m-%d %H:%M:%S')}

        Thank you for using our library system.

        Best Regards,
        Library Team
        """

        # Send email
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [student.email],
            fail_silently=False,
        )

        logger.info(f"Email sent successfully for transaction {transaction_id}")
    except Transaction.DoesNotExist:
        logger.error(f"Transaction not found with transaction_id {transaction_id}")
    except Exception as e:
        logger.error(f"Error sending email: {e}")