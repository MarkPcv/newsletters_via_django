from django import forms

from newsletters.models import Client, Newsletter, Content

FREQUENCY = {
    ('daily', 'Daily'),
    ('weekly', 'Weekly'),
    ('monthly', 'Monthly'),
}

STATUS = {
    ('created', 'Created'),
    ('started', 'Started'),
    ('finished', 'Finished'),
}


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Create dropdown list for frequency field
            if field_name == 'frequency':
                field.widget=forms.Select(choices=FREQUENCY)
            # Create dropdown list for status field
            if field_name == 'status':
                field.widget = forms.Select(choices=STATUS)
            field.widget.attrs['class'] = 'form-control'



class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'


class NewsletterForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = '__all__'


class ContentForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Content
        exclude = ('client',)