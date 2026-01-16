from django.shortcuts import render, get_object_or_404,redirect
from .models import*
from django.core.mail import send_mail
from django.db.models import Avg, Q
from django.conf import settings
from django.core.paginator import Paginator
from datetime import datetime
from django.contrib import messages


# Create your views here.
def home(request):
    category=Category.objects.all()
    # recipe=Recipes.objects.all()[:6]
    recipes=Recipes.objects.order_by('id').annotate(avg_rating=Avg('feed_back__rating'))[:6]
    # for roundoff the avg rating
    for recipe in recipes:
        if recipe.avg_rating:
            recipe.avg_rating=round(recipe.avg_rating)
        else:
            recipe.avg_rating=0
    
    return render(request,'index.html',context={

        "category":category,
        "recipe":recipes,
        "now":datetime.now()
        } )

def add_recipe(request):
    
    categories=Category.objects.all()

    if request.method=='POST':
        title=request.POST.get('title')
        description=request.POST.get('description')
        ingridients=request.POST.get('ingredients')
        instruction=request.POST.get('instructions')
        category_id=request.POST.get('category')
        category=Category.objects.get(id=category_id) if category_id else None
        
        image=request.FILES.get('image')
        
        recipe = Recipes.objects.create(

            title=title,
            discription=description,
            ingredients=ingridients,
            instructions=instruction,
            category=category,
            image=image,
            approved = True if request.user.is_superuser else False


        )
        
        recipe_id=recipe.id
        if not request.user.is_superuser:
            send_mail(
                subject= 'A new recipe is create',
                message= f'''There is new recipe is add and waiting for your approvement
                recipe id = {recipe_id}, 
                recipe title = {title},
                ''',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['rishikabhawsar431@gmail.com']

            )
            messages.info(request,'''Thank you for sharing recipe,
                          Your recipe is currently under review and 
                          will be approved by the admin shortly''')
      


        return redirect('addrecipe')

    return render(request,'addrecipe.html' ,context={'categories':categories})

def detail_recipe(request, recipe_slug):
    recipe=Recipes.objects.get(slug=recipe_slug)
    ingredient_list=recipe.ingredients.split(',')

    if request.method=="POST":
        name = request.POST.get('name')
        rating = request.POST.get('rating')
        feedback = request.POST.get('feedback')
        # recipe= request.POST.get(id=recipe_id)

        Feedback.objects.create(
            name = name,
            rating = rating,
            feedback = feedback,
            recipe = recipe
        )
        return redirect('detail_recipe', recipe_slug=recipe.slug)

    feedbacks=Feedback.objects.filter(recipe=recipe)


    return render(request,'detail_recipe.html',context={
        'recipe':recipe,
        'ingredient_list':ingredient_list,
        'feedback':feedbacks
        })



def about(request):
    return render(request,'about.html')

def all_category(request):
    category=Category.objects.all()

    return render(request,'all_category.html',context={'category':category})

def all_recipe(request):
    
    recipes=Recipes.objects.annotate(avg_rating=Avg('feed_back__rating')) 
    # for roundoff the avg rating
    for recipe in recipes:
        if recipe.avg_rating:
            recipe.avg_rating=round(recipe.avg_rating)
        else:
            recipe.avg_rating=0
    
    paginator= Paginator(recipes,6)
    page_no=request.GET.get('page')
    page_obj=paginator.get_page(page_no)
    
    return render(request, 'all_recipe.html',context={'page_obj':page_obj})

def category_detail(request ,category_slug):
    category=get_object_or_404(Category,slug=category_slug)
    recipes=Recipes.objects.filter(category=category).annotate(avg_rating=Avg('feed_back__rating')) 
    # for roundoff the avg rating
    for recipe in recipes:
        if recipe.avg_rating:
            recipe.avg_rating=round(recipe.avg_rating)
        else:
            recipe.avg_rating=0
    paginator= Paginator(recipes,6)
    page_no=request.GET.get('page')
    page_obj=paginator.get_page(page_no)


    return render(request,'category_detail.html',context={'page_obj':page_obj,
                                                          'category':category})



def search(request):
    query=request.GET.get('q')
    recipe=[]
    if query:
        recipe=Recipes.objects.filter(
            Q(title__icontains=query)|
            Q(discription__icontains=query)
            ).annotate(avg_rating = Avg('feed_back__rating'))
        
        for r in recipe:
            if r.avg_rating:
                r.avg_rating=round(r.avg_rating)
            else:
                r.avg_rating=0
 
        
    return render(request,'search.html', context={'query':query, 'recipes':recipe})

def contact(request):
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        message=request.POST.get('message')


        send_mail(
            subject=f"contact from {name} ",

            message=f"""{message}
                    myemail={email}
                    """,  

            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["rishikabhawsar431@gmail.com"]

        )
        messages.success(request,'Your message has been send successsfully')
        return redirect("contact")

    return render(request,'contect.html')

