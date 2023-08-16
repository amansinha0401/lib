from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, MemberViewSet, TransactionViewSet, issue_book, return_book
from .views import import_books

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'members', MemberViewSet)
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    # ... your existing URLs if any
    path('', include(router.urls)),
    path('import-books/', import_books, name='import-books'),
   path('issue-book/', issue_book, name='issue-book'),
    path('return-book/', return_book, name='return-book'),
]
