from django.shortcuts import render
from django.http import HttpResponse
from .util import *
import markdown2
import random
from . import util
import os
from django.shortcuts import render,redirect
from django.urls import reverse
from django import forms
from .models import MyModel

class AddNewEntryForm(forms.ModelForm):
    class Meta:
        model = MyModel
        fields = ['title' , 'description']
        widgets = {
            'description': forms.Textarea(attrs={
                'placeholder': 'Enter a detailed description...',
            }),
            'title' : forms.TextInput(attrs={
                'style' : 'line-height: 30px;'
            })
        }


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
})

def search_list(request):
    query = request.GET.get('q','').lower()
    entries =  []
    entry_list = list_entries()
    for entry in entry_list:

        if query in entry.lower() :
            entries.append(entry)

    if len(entries)!=0 : 
        return render(request, "encyclopedia/index.html", {
            "entries": entries
        })
    else :
        return render(request , "encyclopedia/error.html" ,{
            'message' : f'No entry found related to:{query}',
        })

def entry_info(request, entry):
    content = get_entry(entry)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": f"The entry '{entry}' was not found."
        })
    return render(request, "encyclopedia/display.html", {
        'entry_name': entry,
        'text': markdown2.markdown(content),
    })

def random_entry(request):
    entries = util.list_entries()
    title = random.choice(entries)
    return redirect("view" ,entry=title)



def create_new_page(request):
    if request.method=='POST':
        new_entry = AddNewEntryForm(request.POST)
        if new_entry.is_valid():
            new_file_name=new_entry.cleaned_data['title']
            file_content = new_entry.cleaned_data['description']
            all_entries_available = list_entries()
            if new_file_name in all_entries_available:
                return render(request , 'encyclopedia/error.html' , {
                    'message' : f'{new_file_name} already exists',
                })
            else :
                with open(f'entries/{new_file_name}.md' , 'w') as file:
                    file.write(file_content)
                return redirect("view" , entry=new_file_name)

    return render(request , "encyclopedia/create.html" ,{
        'form' : AddNewEntryForm(),
    })

def edit_content(request , entry):
    initial_data = {"description": get_entry(entry) , "title" : entry}
    MyForm = AddNewEntryForm(initial=initial_data)
    if (request.method=='POST'):
        new_entry = AddNewEntryForm(request.POST)
        if new_entry.is_valid():
            with open(f"entries/{entry}.md" , "w") as f:
                f.write(new_entry.cleaned_data['description'])
        return redirect("view" , entry = entry)
        
    return render(request , 'encyclopedia/edit.html' , {
        'form' : MyForm,
        'entry' : entry
    })

def delete_content(request , entry):
    os.remove(f'entries/{entry}.md')
    return redirect("index")