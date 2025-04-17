from django.contrib import admin
from .models import Role, User, Product, Category, Sale, Payment, Bill, PayMethod

admin.site.register(Role)
admin.site.register(User)
admin.site.register(Sale)
admin.site.register(Bill)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Payment)
admin.site.register(PayMethod)


