from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
import datetime


from .models import Book, Member, Transaction
from .serializers import BookSerializer, MemberSerializer, TransactionSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    @action(detail=True, methods=['post'])
    def issue_book(self, request, pk=None):
        transaction = self.get_object()
        serializer = TransactionSerializer(transaction, data=request.data, partial=True)
        if serializer.is_valid():
            if transaction.return_date:
                return Response({"detail": "This book has already been returned."},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer.save(return_date=None)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        transaction = self.get_object()
        serializer = TransactionSerializer(transaction, data=request.data, partial=True)
        if serializer.is_valid():
            if not transaction.return_date:
                return Response({"detail": "This book has not been issued yet."},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer.save(return_date=request.data.get('return_date'))
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def import_books(request):
    num_books = request.data.get('num_books')
    title = request.data.get('title', '')

    # Construct the URL for the Frappe API
    url = f"https://frappe.io/api/method/frappe-library?title={title}"

    # Make a GET request to the Frappe API
    response = requests.get(url)
    data = response.json()

    # Process the data and create book records in your database
    imported_count = 0
    for book_data in data['message']:
        # publication_date = datetime.datetime.strptime(book_data['publication_date'], '%m/%d/%Y').date()
        book, created = Book.objects.get_or_create(
            title=book_data['title'],
            defaults={
                'authors': book_data['authors'],
                'average_rating': book_data['average_rating'],
                'isbn': book_data['isbn'],
                'isbn13': book_data['isbn13'],
                'language_code': book_data['language_code'],
                'ratings_count': book_data['ratings_count'],
                'text_reviews_count': book_data['text_reviews_count'],
                # 'publication_date': publication_date,
                'publisher': book_data['publisher'],
                # Add other fields here
                'stock': num_books
            }
        )
        if created:
            imported_count += 1

    return Response({"message": f"Imported {imported_count} books"})



@api_view(['POST'])
def issue_book(request):
    serializer = TransactionSerializer(data=request.data)
    if serializer.is_valid():
        transaction = serializer.save(return_date=None)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def return_book(request):
    transaction_id = request.data.get('transaction_id')
    return_date = request.data.get('return_date')
    
    try:
        transaction = Transaction.objects.get(id=transaction_id)
    except Transaction.DoesNotExist:
        return Response({"detail": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = TransactionSerializer(transaction, data={'return_date': return_date}, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)