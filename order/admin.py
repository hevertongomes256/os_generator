from django.contrib import admin
from .models import Order, Checklist, ChecklistItem

# Register your models here.
admin.site.register(Order)
admin.site.register(Checklist)
admin.site.register(ChecklistItem)
