from django import forms
from django.forms import ModelForm
from app1.models import *
import datetime
class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()
class CustomActionForm(forms.Form):
    action = forms.CharField(widget=forms.HiddenInput,
                             initial='delete_selected',
                             label='Delete Selected'
                             )
    select_across = forms.BooleanField(
                                       label='',
                                       required=False,
                                       initial=0,
                                       widget=forms.HiddenInput({'class': 'select-across'}),
                                       )
# class MultiImageUploadForm(ModelForm):
#     """ This form is only used to handle the uploads """

#     class Meta:
#         fields = "__all__"
#         model = image

#     def __init__(self, *args, **kwargs):
#         super(MultiImageUploadForm, self).__init__(*args, **kwargs)
#         self.fields['created_at'].initial = datetime.datetime.now()