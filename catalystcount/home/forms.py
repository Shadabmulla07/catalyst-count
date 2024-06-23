from django import forms  
class excelForm(forms.Form):    
    file      = forms.FileField() # for creating file input  