from django.db import models
from Student.models import Student
from Auth.models import User
from Book.models import Book

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('borrow', 'Borrow'),
        ('return', 'Return'),
    ]

    transaction_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="transactions")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")  # Librarian
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="transactions")
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    date = models.DateTimeField()

    student_name = models.CharField(max_length=255)
    librarian_name = models.CharField(max_length=255)
    book_name = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        """Automatically populate student_name, librarian_name, and book_name before saving."""
        self.student_name = self.student.name
        self.librarian_name = self.user.user_name
        self.book_name = self.book.Title
        super().save(*args, **kwargs)

    def __str__(self):
            return"__all__"