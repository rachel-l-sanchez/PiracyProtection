from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.contrib.auth.hashers import (
    PBKDF2PasswordHasher, SHA1PasswordHasher,
)
import uuid
from django.urls import reverse


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, username = None):
        """
        Creates and saves a User with the given fields.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username = self.normalize_username(username)
        )
        user.username = username
        user.password = password
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.admin = True
        user.save(using=self._db)
        return user



class Customer(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email Address',
        max_length=255,
        unique=False,
        null = False
    )
    ip_address = models.GenericIPAddressField(null = False)
    id = models.CharField(max_length=100, primary_key = True)
    username = models.CharField(null = False, max_length = 100, default = 'myusername')
    serial_key = models.UUIDField(
        editable=False,
        default=uuid.uuid4,
        unique = True,
        primary_key = False
    )

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'username'

    objects = UserManager()
    
    def get_full_username(self):
        # The user is identified by their username
        return self.username

    def __str__(self):
        return self.serial_key
    
    def __unicode__(self):
        return self.serial_key

    def get_absolute_url(self):
        return reverse("users:homepage", kwargs={"serial_key": self.serial_key})
    
    @property
    def is_admin(self):
        return self.admin
    
    def has_module_perms(self, app_label):
        # Simplest possible answer: Yes, always
        return True
   

class File(models.Model):
    sourceFile = models.FileField(upload_to ='uploads/', null=True)
    title = models.TextField(null = False)
    description = models.TextField(null = False)
    stripe_file_id = models.CharField(max_length = 100, default ="defaultID")

    def __str__(self):
        return self.title 
    
    def save(self, *args, **kwargs):
        try:
            this = File.objects.get(id=self.id)
            if this.sourceFile != self.sourceFile:
                this.sourceFile.delete()
        except: pass
        super(File, self).save(*args, **kwargs)

class CustomLogin(models.Model):
    customer = models.OneToOneField(Customer,
     on_delete = models.CASCADE
    )
    file  = models.OneToOneField(
     File,
    on_delete = models.CASCADE, 
    related_name="File")


class Price(models.Model):
    product = models.ForeignKey(File, on_delete=models.CASCADE)
    stripe_price_id = models.CharField(max_length=100)
    price = models.IntegerField(default=0)  # cents
    
    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)

class PaymentHistory(models.Model):
    PENDING = "P"
    COMPLETED = "C"
    FAILED = "F"

    STATUS_CHOICES = (
        (PENDING, ("pending")),
        (COMPLETED, ("completed")),
        (FAILED, ("failed")),
    )

    email = models.EmailField(unique = True)
    product = models.ForeignKey(File, on_delete = models.CASCADE)
    payment_status = models.CharField(
        max_length = 1, choices = STATUS_CHOICES, default=PENDING
    )
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.product.title