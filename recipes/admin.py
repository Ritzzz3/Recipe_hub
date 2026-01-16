from django.contrib import admin

# Register your models here.
from .models import*

admin.site.register(Category)
# admin.site.register(Recipes)

@admin.action(description='approve')
def approve_recipes(ModelAdmin,request, queryset):
    queryset.update(approved=True)
       

@admin.register(Recipes)
class Admin_recipe(admin.ModelAdmin):
    list_display=['id','title','created_at']
    search_fields = ['title', 'discription','ingredients']
    list_filter = ['created_at','approved']
    list_display_links = ['title']
    actions = [approve_recipes]
    readonly_fields = ['title','slug']
    fieldsets = (('recipe_info',{'fields':['title','discription','slug']}),
                 ('preparetion_info',{'fields':['ingredients','instructions']}),
                 ('category',{'fields':['category']}),
                 ('image',{'fields':['image']}),
                 ('approve',{'fields':['approved']})

                )

    
