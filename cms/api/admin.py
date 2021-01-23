from django.contrib import admin
from .models import User,Author,Admin,Content,AuthorBlacklistToken,AdminBlacklistToken
# Register your models here.
class UserLabel(admin.ModelAdmin):
    list_display = ['email','full_name','country']
class ContentLabel(admin.ModelAdmin):
    list_display = ['id','title','categories']
class AuthorBlacklistTokenLabel(admin.ModelAdmin):
    list_display = ['token','user','timestamp']
class AdminBlacklistTokenLabel(admin.ModelAdmin):
    list_display = ['token','user','timestamp']
admin.site.register(User,UserLabel)
admin.site.register(Author,UserLabel)
admin.site.register(Admin,UserLabel)
admin.site.register(Content,ContentLabel)
admin.site.register(AuthorBlacklistToken,AuthorBlacklistTokenLabel)
admin.site.register(AdminBlacklistToken,AdminBlacklistTokenLabel)