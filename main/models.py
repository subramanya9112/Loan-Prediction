from django.db import models


class ContactUs(models.Model):
    name = models.CharField(max_length=200)
    email1 = models.EmailField()
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name
