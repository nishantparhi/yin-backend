from django.db import models

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=200, help_text="Name of the sender" )
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=200, null=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Contact"

    def __str__(self):
        return self.name + "-" +  self.email