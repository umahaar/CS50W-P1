import random
from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import util

# View for the /wiki/TITLE
def entry(request, title): 
    print(f"Request for title: {title}")
    # Fetch the content of the encyclopedia entry
    entry_content = util.get_entry(title)

    if entry_content is None:
        print("Entry not found")
        # If entry does not exist, render an error page
        return render(request, "encyclopedia/error.html", {
            "message": "The requested page was not found."
        })
    else:
        print("Entry found")
        return render(request, "encyclopedia/entry.html",{
            "title": title,
            "content": entry_content
        })
    
# View for the Index page

def index(request):
    entries = util.list_entries() # Here I am getting the list that is being returned by list_enteries() utility funtion in util.py
    return render(request, "encyclopedia/index.html", { # Whole list is sent to index.html to handle it
        "entries": entries
    })

# View for Search

def search(request):
    query = request.GET.get('q', '') #'q' gives the whole query parameter,incase of empty string we will head to else: block
    if query:
        matches = util.search_entries(query)
        exact_match = next((entry for entry in matches if entry.lower() == query.lower()), None) # For the exact match
        if exact_match:
            # Exact match found, redirect to the entry page
            return redirect('entry', exact_match)
        else: # For the partial match
            # Partial matches found, render the search results page
            return render(request, "encyclopedia/search_results.html", {
                "query": query,
                "matches": matches
            })
    else:
        # In case no query is provided, redirect to the index page
        return redirect('index')


# View for New_Page

def new_page(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        if not title or not content:
            return render(request, "encyclopedia/new_page.html", {
                "error": "Title and content are required."
            })

        if util.get_entry(title):
            return render(request, "encyclopedia/new_page.html", {
                "error": "An entry with this title already exists."
            })

        util.save_entry(title, content)
        return redirect("entry", title=title)

    return render(request, "encyclopedia/new_page.html")

# View for Editing and  saving it again:


def edit_page(request, title):
    if request.method == "POST":
        content = request.POST.get("content")
        if not content:
            return render(request, "encyclopedia/edit_page.html", {
                "title": title,
                "error": "Content is required.",
                "content": util.get_entry(title)
            })
        util.save_entry(title, content)
        return redirect("entry", title=title)
    
    return render(request, "encyclopedia/edit_page.html", {
        "title": title,
        "content": util.get_entry(title)
    })

# View for  Random function:

def random_page(request):
    entries = util.list_entries()
    if entries:
        random_entry = random.choice(entries)
        return redirect('entry', title=random_entry)
    else:
        return render(request, "encyclopedia/error.html", {
            "message": "No entries available."
        })
    
