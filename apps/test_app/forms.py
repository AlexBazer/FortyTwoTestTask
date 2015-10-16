from django.forms import ModelForm

from test_app.models import CustomUser


class CustomUserForm(ModelForm):
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
