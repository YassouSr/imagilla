import requests
from PIL import Image

from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from .form import SearchForm
from .search  import ReverseSearch

# Basic view function that retuns index.html
def HomeView(request):
    ALLOWED_EXT = ["image/png", "image/jpeg", "image/jpg"]
    form = SearchForm()
    if request.method == 'POST':
        form = SearchForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['urlField']:
                url = form.cleaned_data['urlField']
                try:
                    res = requests.get(url)
                    if res.status_code == 404:
                        return HttpResponseRedirect(reverse('errorview', args=["non-existent-url", url]))
                    if not res.headers["content-type"] in ALLOWED_EXT:
                        if  not res.headers["content-type"].startswith('image'):
                            return HttpResponseRedirect(reverse('errorview', args=["img-url-error", url]))
                        else:
                            return HttpResponseRedirect(reverse('errorview', args=["img-ext-error", res.headers["content-type"].split('/')[1]]))   
                    
                    return SearchView(request, 'url-search', url)
                except:
                    return HttpResponseRedirect((reverse('errorview', args=["non-existent-url", url])))  
            else:
                file = request.FILES['upload_field']
                if not file.content_type in ALLOWED_EXT:
                    return HttpResponseRedirect(reverse('errorview', args=["img-ext-error", file.content_type.split('/')[1]]))
                else:
                    image = Image.open(file)
                    return SearchView(request, 'image-search', image)
        else:
            form = SearchForm()
            
    return render(request, 'backend/index.html', {"form": form})

# View function that returns search results (search.html)
def SearchView(request, typeSearch, data):
    if typeSearch == 'url-search':
        model = ReverseSearch()
        query = model.prepare_image_through_url(data)
        label, results = model.search_sisters(query)
    
    if typeSearch == 'image-search':
        model = ReverseSearch()
        query = model.prepare_image(data)
        label, results = model.search_sisters(query)

    context = {
        "query_label": label,
        "results": results
    }
    
    return render(request, 'backend/search.html', context)

# View function for errors (error.html)
def ErrorView(request, errorType, errorText):
    context = { 
            "errorType": errorType,
            "errorText": errorText,
        }

    return render(request, 'backend/error.html', context)
