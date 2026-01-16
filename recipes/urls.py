
from django.urls import path 
from .views import*

urlpatterns = [
    path('',home,name='home'),
    path('addrecipe/',add_recipe,name='addrecipe'),

    path('about/',about,name='about'),
    path('all_category/',all_category,name='all_category'),
    path('all_recipe/',all_recipe,name='all_recipe'),
    path('category_detail/<str:category_slug>/',category_detail,name='category_detail'),
    path('detail_recipe/<str:recipe_slug>/',detail_recipe,name='detail_recipe'),
    path('search/',search,name='search'),
    path('contact/',contact,name='contact'),
]
