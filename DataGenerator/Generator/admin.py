from django.contrib import admin
from .models import category


# Register your models here.

class category_admin(admin.ModelAdmin):
    list_display = [x.name for x in category._meta.fields]


admin.site.register(category, category_admin)
