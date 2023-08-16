from django.contrib import admin
from .models import Book, Member, Transaction

admin.site.register(Book)
admin.site.register(Member)
admin.site.register(Transaction)
