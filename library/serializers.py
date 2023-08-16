from rest_framework import serializers
from .models import Book, Member, Transaction

# frontend me kya data dikhega uske liye serializers use karte hai

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'  # You can specify specific fields here if needed 
        # Jo bhi field dikhana hai sirf wahi likhna hai ya to __all__ likhna hai
        # fields = ['title', 'author']

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'  # You can specify specific fields here if needed

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'  # You can specify specific fields here if needed

class ImportBooksSerializer(serializers.Serializer):
    num_books = serializers.IntegerField()
    title = serializers.CharField(required=False)