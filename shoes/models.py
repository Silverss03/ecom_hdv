from django.db import models

# Create your models here.
class Shoe(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    size = models.TextField()
    image = models.ImageField(upload_to='shoes_images/', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "shoe"
        app_label = "shoes"
        managed = True