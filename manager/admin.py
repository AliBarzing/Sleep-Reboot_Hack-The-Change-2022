from django.contrib import admin
from .models import Group, Password , user

# Register your models here.

admin.site.register(Group)
admin.site.register(Password)
admin.site.register(user)