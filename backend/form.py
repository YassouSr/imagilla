from django import forms
from  .validator import validate_urlField

class SearchForm(forms.Form):
    urlField = forms.URLField(max_length=1000, 
                              required=False, 
                              validators=[validate_urlField]
                            )
    
    upload_field = forms.ImageField(required=False)
    
    urlField.widget.attrs.update({'class': 'form-control', 
                                   'autofocus':'true',
                                   'autocomplete':'off',
                                   'spellcheck':'false',
                                   'autocorrect':'off',
                                   'placeholder':'Enter a URL or Upload an image'
                                })
    
