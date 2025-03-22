from rest_framework import viewsets, status
from rest_framework.response import Response
from core.queue_publisher import publish_transaction_email
#from core.emil import send_transaction_email
from .service import TransactionService
from .serializer import TransactionSerializer
from rest_framework.permissions import AllowAny
from core.utils import handle_error
import logging
from core.queue_publisher import publish_transaction_email
logger = logging.getLogger(__name__)

class TransactionViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = TransactionService()
    
    @handle_error
    def list(self, request):
        print(request.data)
        logger.info("Fetching all transactions.")
        transactions = self.service.get_all_Transactions()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
    
    @handle_error
    def retrieve(self, request, pk=None):
        logger.info(f"Fetching transaction with id {pk}.")
        transaction = self.service.get_Transaction_by_id(pk)
        if transaction:
            serializer = TransactionSerializer(transaction)
            return Response(serializer.data)
        return Response({"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)
    
    @handle_error
    def create(self, request):
        print("Request Data:", request.data)   
        logger.info(f"Creating a new transaction with data: {request.data}")
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            transaction = self.service.create_Transaction(serializer.validated_data)
            try:
#               send_transaction_email( transaction.transaction_id)
                publish_transaction_email(transaction.transaction_id)  # ✅ Properly indented
            except Exception as e:
                logger.error(f"Failed to send email: {e}")
            return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @handle_error
    def update(self, request, pk=None):
        logger.info(f"Updating transaction with id {pk} with data: {request.data}")
        serializer = TransactionSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            transaction = self.service.update_Transaction(pk, serializer.validated_data)
            if transaction:
                return Response(TransactionSerializer(transaction).data)
            return Response({"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @handle_error
    def destroy(self, request, pk=None):
        logger.info(f"Deleting transaction with id {pk}.")
        if self.service.delete_Transaction(pk):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)
