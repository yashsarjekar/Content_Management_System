from django.contrib import admin
from .models import User,Author,Admin,Content
# Register your models here.
class UserLabel(admin.ModelAdmin):
    list_display = ['email','full_name','country']
class ContentLabel(admin.ModelAdmin):
    list_display = ['id','title','categories']
admin.site.register(User,UserLabel)
admin.site.register(Author,UserLabel)
admin.site.register(Admin,UserLabel)
admin.site.register(Content,ContentLabel)