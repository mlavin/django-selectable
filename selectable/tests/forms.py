from django import forms

from selectable.forms import fields
from selectable.tests import ThingLookup

class Form1(forms.Form):
    f = fields.AutoCompleteSelectMultipleField(ThingLookup)


