from django import forms
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
