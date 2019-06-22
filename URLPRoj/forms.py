from django import forms


class CheckURL(forms.Form):

    url = forms.URLField(label='Enter URL', label_suffix=': ',
                         widget=forms.URLInput(attrs=
                                               {
                                                   'class': 'btn btn-default'
                                               }
                         )
                         )
