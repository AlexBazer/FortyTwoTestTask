from django.forms import ModelForm, DateField, ImageField

from test_app.models import CustomUser
from test_app.widgets import DateSelectorWidget, TumbnailImage


class CustomUserForm(ModelForm):
    birthday = DateField(widget=DateSelectorWidget())
    # photo = ImageField(widget=TumbnailImage())
    
    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)

        form_control_fields = [
            'first_name',
            'last_name',
            'jabber_id',
            'skype_id',
            'biography',
            'other_contacts',
            'birthday'
        ]
        for field in form_control_fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'birthday',
            'jabber_id',
            'skype_id',
            'biography',
            'other_contacts',
            'photo',
        ]
