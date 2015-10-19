from django.forms import DateInput, MultiWidget, HiddenInput
from django.utils.safestring import mark_safe


class DateSelectorWidget(MultiWidget):
    def __init__(self, attrs=None, _format='D MMMM YYYY'):
        _widgets = (
            DateInput(attrs=attrs),
            HiddenInput(attrs=attrs),
        )
        self.format = _format
        super(DateSelectorWidget, self).__init__(_widgets, attrs)

    def decompress(self, value):
        """
            Populate only hidden widgets
        """
        return [None, value]

    def value_from_datadict(self, data, files, name):
        """
            Return hidden value
        """
        return data.get(name + '_1')

    def render(self, name, value, attrs=None):
        """
            Render super and then add Kalendae initialization
            And format logic
        """
        data_widget_html = super(DateSelectorWidget, self).render(
            name, value, attrs
        )
        return mark_safe(data_widget_html + """
        <script>
            var birthday_hidden = document.getElementById('{{hidden_id}}');
            var birthday = new Kalendae.Input('{{input_id}}', {
                format:'{{format}}',
                weekStart: 1,
                subscribe: {
                   'change': function (date) {
                        // Change hidden_date value by selected value
                        birthday_hidden.value = date.format('YYYY-MM-DD')
                   }
               }
            });
            birthday.input.addEventListener('keyup', function(e){
                e.preventDefault();
            })
            var hidden_date;
            if (birthday_hidden.value.length > 0){
                hidden_date = Kalendae.moment(
                    birthday_hidden.value,
                    'YYYY-MM-DD'
                );
            }
            // Disable onkeypress
            //(lives field editable, but only through calendar)
            birthday.input.onkeypress = \
            birthday.input.onkeydown = \
            birthday.input.onkeyup = function(e){
               e.preventDefault();
               return false;
            }
            //Init date by hidden_date
            birthday.setSelected(hidden_date.format(birthday.settings.format))
            </script>
        """.replace('{{input_id}}', attrs['id']+'_0').
            replace('{{hidden_id}}', attrs['id']+'_1').
            replace('{{format}}', self.format))

    class Media:
        css = {
            'all': ('css/kalendae.css', 'css/kalendae-theme.css')
        }
        js = ('js/kalendae.standalone.js',)
