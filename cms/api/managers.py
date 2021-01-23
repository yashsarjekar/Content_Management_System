from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
###### User Manager ######
class UserManager(BaseUserManager):
    def create_user(self, email, password,full_name,phone,pincode,address="",city="",state="",country=""):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,full_name=full_name,phone=phone,address=address,
        city=city,state=state,country=country,pincode=pincode)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password,full_name,phone,pincode):
        """
        Create and save a SuperUser with the given email and password.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, password,full_name,phone,pincode)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

##### AuthorManager #######
class AuthorManager(BaseUserManager):
    def create_user(self, email, password,full_name,phone,pincode,address="",city="",state="",country=""):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,full_name=full_name,phone=phone,address=address,
        city=city,state=state,country=country,pincode=pincode)
        user.set_password(password)
        user.save()
        return user

###### Admin Manager #########        
class AdminManager(BaseUserManager):
    def create_user(self, email, password,full_name,phone,pincode,address="",city="",state="",country=""):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,full_name=full_name,phone=phone,address=address,
        city=city,state=state,country=country,pincode=pincode)
        user.set_password(password)
        user.save()
        return user