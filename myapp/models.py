from django.db import models

class Cafe(models.Model):

    id = models.IntegerField(primary_key=True)
    product_name = models.CharField(max_length=20)
    product_price = models.IntegerField()


    

    


    
