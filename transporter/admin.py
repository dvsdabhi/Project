from django.contrib import admin

from transporter.models import Transporter

# Register your models here.
@admin.register(Transporter)
class UserAdmin(admin.ModelAdmin):

    list_display = ['username','email']