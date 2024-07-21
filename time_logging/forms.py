from django import forms
from .models import TimeLog


class EnterForm(forms.Form):
    faculties = [
        ('情報', '情報'),
        ('アニメ・マンガ', 'アニメ・マンガ'),
        ('事業創造', '事業創造'),
        ('その他', 'その他'),
    ]
    faculty = forms.ChoiceField(
        label='学部',
        choices=faculties,
        initial='情報',
        widget=forms.RadioSelect(attrs={'class':'input-radio'}),
        required=True,
    )

    attributes = [
        ('学生', '学生'),
        ('教員', '教員'),
        ('職員', '職員'),
        ('その他', 'その他'),
    ]
    attribute = forms.ChoiceField(
        label='所属',
        choices=attributes,
        initial='学生',
        widget=forms.RadioSelect(attrs={'class':'input-radio'}),
        required=True,
    )

    student_number = forms.CharField(
        label='学籍番号',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': '20232024（数字八桁）'}),
        min_length=8,
        max_length=8,
        strip=True,
        
        )
    
    name = forms.CharField(
        label='氏名',
        required=False,
        #help_text= '学生は任意',
        widget=forms.TextInput(attrs={'placeholder': '開志専太'}),
        min_length=1,
        max_length=48,
        strip=True,
        
        )
    
class AddForm(EnterForm):
    
    enter =  forms.DateTimeField(
        label='入室時間',
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        required=True,
        
        )

    
    exit = forms.DateTimeField(
        label='退室時間',
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        required=True,
        
        )
    

