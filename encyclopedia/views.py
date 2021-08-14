from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from markdown2 import Markdown
from random import choice
import re

from . import util

class EntryForm(forms.Form):
    title = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.Textarea)

def entry_handler(request,template_name, body):
    form = EntryForm(body)
    if form.is_valid():
        title = form.cleaned_data['title']
        content = form.cleaned_data['content']
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("entry", kwargs={"entry_name":title}))
    return render(request,template_name,{
        "title":body['title'],
        "content":body['content'],
        "form":form
    })

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry_name):
    markdowner = Markdown()
    file_content = util.get_entry(entry_name)
    if not file_content:
        response = render(request, "encyclopedia/404.html")
        response.status_code = 404
        return response
    return render(request, "encyclopedia/entry.html", {
        "entry_name": entry_name,
        "file_content": markdowner.convert(file_content)
    })

def random(request):
    title = choice(util.list_entries())
    return HttpResponseRedirect(reverse("entry", kwargs={"entry_name":title}))

def create(request):
    if request.method == "POST":
        return entry_handler(request, "encyclopedia/new.html",request.POST)
    return render(request, "encyclopedia/new.html", {
        "title":"",
        "content":"Enter your content for entry here.",
        "form":EntryForm()
    })

def search(request):
    search_string = request.GET['q'].strip()
    all_entries = util.list_entries()
    if search_string in all_entries:
        return HttpResponseRedirect(reverse("entry", kwargs={"entry_name":search_string}))
    filtered_entries = [entry for entry in all_entries if re.search(search_string,entry, re.IGNORECASE)]
    if len(filtered_entries) ==1:
        return HttpResponseRedirect(reverse("entry", kwargs={"entry_name":filtered_entries[0]}))
    return render(request, "encyclopedia/search.html", {
        "entries": filtered_entries
    })

def edit(request, entry_name):
    if request.method=="POST":
        body = {}
        body['content'] = request.POST['content']
        body['title'] = entry_name
        return entry_handler(request, "encyclopedia/edit.html",body)
    file_content = util.get_entry(entry_name)
    if not file_content:
        response = render(request, "encyclopedia/404.html")
        response.status_code = 404
        return response
    return render(request, "encyclopedia/edit.html", {
        "title":entry_name,
        "content":file_content,
        "form":EntryForm()
    })