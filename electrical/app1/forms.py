from django import forms
from django.forms import ModelForm
from app1.models import *
import datetime
class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()
class CustomActionForm(forms.Form):
    action = forms.CharField(widget=forms.HiddenInput,initial='delete_selected',label='Delete Selected')
    select_across = forms.BooleanField(label='',required=False,initial=0,widget=forms.HiddenInput({'class': 'select-across'}),                                    )
class MailForm(forms.Form):
    subject = forms.CharField(
        max_length=255
        )
    message = forms.CharField(widget=forms.Textarea)
    attachment = forms.FileField()
        
    def clean_subject(self):
        if self.cleaned_data["subject"]=="" or self.cleaned_data["subject"]==None:
            raise forms.ValidationError("My text goes here")    
        return self.cleaned_data["subject"]

    def clean_message(self):
        if self.cleaned_data["message"]=="" or self.cleaned_data["message"]==None:
            raise forms.ValidationError("My text goes here")    
        return self.cleaned_data["message"]
        
