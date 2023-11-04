from django import forms
from .models import Category, Difficulty, Question


class FilterForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="All Categories",
                                      required=False,
                                      to_field_name="name")
    difficulty = forms.ModelChoiceField(queryset=Difficulty.objects.all(), empty_label="All Difficulties",
                                        required=False, to_field_name="level")

    def __init__(self, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)
        self.fields['category'].label_from_instance = lambda obj: obj.name
        self.fields['difficulty'].label_from_instance = lambda obj: obj.level
