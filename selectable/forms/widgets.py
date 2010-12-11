from django import forms


__all__ = (
    'AutoCompleteWidget',
)


class AutoCompleteWidget(forms.TextInput):

    def __init__(self, lookup_class, *args, **kwargs):
        self.lookup_class = lookup_class
        super(AutoCompleteWidget, self).__init__(*args, **kwargs)
        # New attrs
        url = lookup_class.url()
        self.attrs['data-selectable-url'] = url

