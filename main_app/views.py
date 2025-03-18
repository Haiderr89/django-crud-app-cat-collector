# This is the controller page

# main_app/views.py
from django.shortcuts import render, redirect

from .models import Cat, Toy

from .forms import FeedingForm


# Add UdpateView & DeleteView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.views.generic import ListView, DetailView # add these 

# Import HttpResponse to send text-based responses
# from django.http import HttpResponse

# ====================================================
# Create your views here.

# is like an object
# class Cat:
#     def __init__(self, name, breed, description, age):
#         self.name = name
#         self.breed = breed
#         self.description = description
#         self.age = age

# # Create a list of Cat instances
# cats = [
#     Cat('Lolo', 'tabby', 'Kinda rude.', 3),
#     Cat('Sachi', 'tortoiseshell', 'Looks like a turtle.', 0),
#     Cat('Fancy', 'bombay', 'Happy fluff ball.', 4),
#     Cat('Bonk', 'selkirk rex', 'Meows loudly.', 6)
# ]

# Define the home view function
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def cat_index(request):
    cats = Cat.objects.all()
    # Render the cats/index.html template with the cats data. the {'cats': cats} let you pass it to the next page to use it.
    return render(request, 'cats/index.html', {'cats': cats})

def cat_detail(request, cat_id):
    cat = Cat.objects.get(id=cat_id)

    # Only get the toys the cat does not have
    toys_cat_doesnt_have = Toy.objects.exclude(id__in = cat.toys.all().values_list('id'))

    feeding_form = FeedingForm()
    return render(request, 'cats/detail.html', {
        'cat': cat,
        'feeding_form': feeding_form,
        'toys': toys_cat_doesnt_have  # send those toys
    })

class CatCreate(CreateView):
    model = Cat
    fields = ['name', 'breed', 'description', 'age']

class CatUpdate(UpdateView):
    model = Cat
    # Let's disallow the renaming of a cat by excluding the name field!
    fields = ['breed', 'description', 'age']

class CatDelete(DeleteView):
    model = Cat
    success_url = '/cats/'

def add_feeding(request, cat_id):
    # create a ModelForm instance using the data in request.POST
    form = FeedingForm(request.POST)
    # validate the form
    if form.is_valid():
        # don't save the form to the db until it
        # has the cat_id assigned
        new_feeding = form.save(commit=False)
        new_feeding.cat_id = cat_id
        new_feeding.save()
    return redirect('cat-detail', cat_id=cat_id)

class ToyCreate(CreateView):
    model = Toy
    fields = '__all__'

class ToyList(ListView):
    model = Toy

class ToyDetail(DetailView):
    model = Toy

class ToyUpdate(UpdateView):
    model = Toy
    fields = ['name', 'color']

class ToyDelete(DeleteView):
    model = Toy
    success_url = '/toys/'

def associate_toy(request, cat_id, toy_id):
    # Note that you can pass a toy's id instead of the whole object
    Cat.objects.get(id=cat_id).toys.add(toy_id)
    return redirect('cat-detail', cat_id=cat_id)

