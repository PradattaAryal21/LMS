import logging
from venv import logger
from .repositories import TransactionRepository
logger = logging.getLogger('Transaction')  # Use the logger you defined in the LOGGING configuration

class TransactionService:
    def __init__(self):
        self.repository = TransactionRepository()

    def get_all_Transactions(self):
        try:
            logger.info(f"Fetching transactions.")
            transactions = self.repository.get_all()  # Fetch all transactions from the repository
            logger.info(f"Fetched {len(transactions)} transactions.")  # Log the fetched transaction count
            return transactions
        except Exception as e:
            logger.error(f"Error fetching transactions: {str(e)}")
            raise Exception("Testing error in list method")
    def get_Transaction_by_id(self, transaction_id):
        
        return self.repository.get_by_id(transaction_id)

    def create_Transaction(self, data):
        return self.repository.create(data)

    def update_Transaction(self, transaction_id, data):
        return self.repository.update(transaction_id, data)

    def delete_Transaction(self, transaction_id):
        return self.repository.delete(transaction_id)
