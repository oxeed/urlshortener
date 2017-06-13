from django import forms

from .validators import validate_dot_com, validate_url


class SumbitUrlForm(forms.Form):
    url = forms.CharField(label='',
                          validators=[validate_url],
                          widget= forms.TextInput(
                              attrs={
                                  'placeholder': 'Long URL',
                                  'class': 'form-control',

                              }
                          )
                          )

    def clean_url(self):
        url = self.cleaned_data['url']
        if 'http' in url:
            return url
        return 'http://' + url
