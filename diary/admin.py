from django.contrib import admin

# Register your models here.
from .models import Diary, Category

admin.site.register(Diary)
admin.site.register(Category)
