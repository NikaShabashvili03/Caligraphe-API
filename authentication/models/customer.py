from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _


class Customer(AbstractBaseUser):
    firstname = models.CharField(max_length=255, verbose_name=_('Name'))
    lastname = models.CharField(max_length=255, verbose_name=_('Last Name'))
    email = models.EmailField(unique=True, verbose_name=_('Email'))

    last_login = models.DateTimeField(null=True, blank=True, verbose_name=_('Last Login'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname']

    def save(self, *args, **kwargs):
        self.firstname = self.firstname.capitalize()
        self.lastname = self.lastname.capitalize()
        if self.pk is None: 
            self.set_password(self.password) 
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers") 

    def __str__(self):
        return f"{self.firstname} {self.lastname} - {self.email}"