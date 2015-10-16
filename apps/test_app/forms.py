from django.forms import ModelForm

from test_app.models import CustomUser


class CustomUserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)

        form_control_fields = [
            'first_name',
            'last_name',
            'jabber_id',
            'skype_id',
            'biography',
            'other_contacts',
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
