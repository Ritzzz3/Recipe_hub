from django.db import models
from django.utils.text import slugify

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=50)
    image=models.ImageField(upload_to='category_image/', blank=True, null=True)#black or null true means without image its support
    slug=models.SlugField(unique=True,blank=True,max_length=120)

    def save(self ,*args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.name)
        super(Category,self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Recipes(models.Model):
    title = models.CharField(max_length=50)
    discription = models.TextField() 
    ingredients = models.TextField()
    instructions = models.TextField()  
    image = models.ImageField(upload_to='recipe_image/',blank=True,null=True) 
    category = models.ForeignKey(Category, on_delete=models.SET_NULL , null=True, blank=True)
    slug=models.SlugField(unique=True,blank=True,null=True)

    # on delete means when category was deleted then recipes category become null
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def save(self,*arg,**kwarg):
        if not self.slug:
            self.slug=slugify(self.title)
        return super().save(*arg,**kwarg)

    def __str__(self):
        return self.title

class Feedback(models.Model):
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE ,related_name='feed_back' )
    name = models.CharField(max_length=50)
    rating = models.PositiveSmallIntegerField()#small positive integer for 1 to 5
    feedback = models.TextField()









