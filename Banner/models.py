from django.db import models

# Create your models here.
class Banner(models.Model):
    title = models.CharField(max_length=255)  
    image = models.URLField() 
    status = models.BooleanField(default=True)  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True) 
    start_date = models.DateTimeField()  
    end_date = models.DateTimeField()   
    description= models.CharField(max_length=255)  

    def __str__(self):
        return self.title
