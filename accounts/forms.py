from django import forms
from .models import Report

class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6)

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['report_date', 'amount', 'bank_number', 'ifsc_code', 'description']
        widgets = {
            'report_date': forms.DateInput(attrs={'type': 'date'}),
            'amount': forms.NumberInput(attrs={'step': '0.01'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }