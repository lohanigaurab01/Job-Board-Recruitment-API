from django.contrib import admin
from .models import Company

class CompanyAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)

admin.site.register(Company, CompanyAdmin)
