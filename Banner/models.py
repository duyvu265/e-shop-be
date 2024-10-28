from django.db import models

# Create your models here.
class Banner(models.Model):
    title = models.CharField(max_length=255)  
    image = models.URLField() 
    status = models.BooleanField(default=True)  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.title
