from rest_framework import serializers
from .models import Transaction
from django.utils import timezone
from datetime import datetime

class TransactionSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    librarian_name = serializers.CharField(source='user.user_name', read_only=True)
    book_name = serializers.CharField(source='book.Title', read_only=True)

    class Meta:
        model = Transaction
        fields = ['transaction_id', 'student', 'user', 'book', 'transaction_type', 'date', 'student_name', 'librarian_name', 'book_name']
        read_only_fields = ['student_name', 'librarian_name', 'book_name']

    def to_internal_value(self, data):
        # Handle the 'date' field before the default validation
        if 'date' in data:
            if data['date'] is None:
                # Set to current date and time if null
                data['date'] = timezone.now()
            elif isinstance(data['date'], str):
                try:
                    # Parse the date in the format "%Y/%m/%d"
                    parsed_date = datetime.strptime(data['date'], "%Y/%m/%d")
                    data['date'] = timezone.make_aware(parsed_date)
                except ValueError:
                    raise serializers.ValidationError({"date": "Invalid date format. Use YYYY/MM/DD."})
        
        return super().to_internal_value(data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['date'] = instance.date.strftime("%Y/%m/%d")
        return representation