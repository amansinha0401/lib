from django.db import models
import datetime
from django.core.validators import MaxValueValidator

# Create your models here. Database Model (Database kaisa dikhega))

class Book(models.Model):
    title = models.CharField(max_length=200, default="")
    authors = models.CharField(max_length=200, default="")
    average_rating = models.CharField(max_length=200, default="")
    isbn = models.CharField(max_length=20, default="")
    isbn13 = models.CharField(max_length=20, default="")
    language_code = models.CharField(max_length=10, default="")
    num_pages = models.PositiveIntegerField(default=0.0)
    ratings_count = models.PositiveIntegerField(default=0.0)
    text_reviews_count = models.PositiveIntegerField(default=0.0)
    # publication_date = models.DateField(default=datetime.date.today)
    publisher = models.CharField(max_length=200, default="")
    # ... other fields
    stock = models.PositiveIntegerField(default=0.0)

class Member(models.Model):
    name = models.CharField(max_length=100)
    amountdue = models.DecimalField(max_digits=6, decimal_places=2, default=0.0, validators=[MaxValueValidator(500)])
    books_issued = models.ManyToManyField(Book, through='Transaction')
    # ... other fields

class Transaction(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    book_name = models.CharField(max_length=200, default="", editable=False)  # Make it not editable
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    issue_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    # ... other fields

    def issue_book(self, book, member, issue_date):
        self.book = book
        self.book_name = book.title  # Set book name based on book's title
        self.member = member
        self.issue_date = issue_date
        self.return_date = None
        self.save()

    def return_book(self, return_date):
        self.return_date = return_date
        self.save()

    def calculate_overdue_charges(self):
        if self.return_date and self.return_date > self.issue_date:
            due_date = self.issue_date + datetime.timedelta(days=10)
            if self.return_date > due_date:
                days_overdue = (self.return_date - due_date).days
                return max(0, days_overdue * 10)
        return 0
