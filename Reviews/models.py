from django.db import models
from django.utils.translation import gettext_lazy as _
from Products.models import Product
from SiteUser.models import SiteUser

class Review(models.Model):
    class RatingChoices(models.IntegerChoices):
        ONE_STAR = 1, _('1 Star')
        TWO_STARS = 2, _('2 Stars')
        THREE_STARS = 3, _('3 Stars')
        FOUR_STARS = 4, _('4 Stars')
        FIVE_STARS = 5, _('5 Stars')

    user = models.ForeignKey(SiteUser, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(choices=RatingChoices.choices)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image_url = models.URLField(blank=True, null=True)
    class Meta:
        unique_together = ('user', 'product')  
        ordering = ['-created_at']  

    def __str__(self):
        return f"Review by {self.user} for {self.product} - {self.rating} Stars"
