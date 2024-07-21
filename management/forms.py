from django import forms


class DownloadForm(forms.Form):

    year = forms.IntegerField(
        label='年',
        required=True,
        widget=forms.NumberInput,
        min_value=2023,
        max_value=2100,
        disabled=False,
    )

    month = forms.IntegerField(
        label='月',
        required=True,
        widget=forms.NumberInput,
        min_value=1,
        max_value=12,
        disabled=False,
    )

