from django.core.mail import send_mail
from django.conf import settings
from Student.models import Student
from Transaction.models import Transaction
import logging

logger = logging.getLogger(__name__)

def send_transaction_email(user_id, transaction_id):
    try:
        # Fetch transaction details
        transaction = Transaction.objects.get(transaction_id=transaction_id)
        student = Student.objects.get(student_id=transaction.student.student_id)

        subject = "Transaction Completed Successfully"
        message = f"Hello {student.name},\n\nYour transaction has been successfully completed.\n\n"
        message += f"Transaction ID: {transaction.transaction_id}\n"
        message += f"Book: {transaction.book_name}\n"
        message += f"Transaction Type: {transaction.get_transaction_type_display()}\n"
        message += f"Date: {transaction.date.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        message += "Thank you for using our library system.\n\nBest Regards,\nLibrary Team"

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [student.email],
            fail_silently=False,
        )
        
        logger.info(f"Transaction email sent to {student.email} for transaction ID {transaction_id}")
    except Student.DoesNotExist:
        logger.error(f"Student not found for user_id {user_id}")
    except Transaction.DoesNotExist:
        logger.error(f"Transaction not found with transaction_id {transaction_id}")
    except Exception as e:
        logger.error(f"Error sending email: {e}")
