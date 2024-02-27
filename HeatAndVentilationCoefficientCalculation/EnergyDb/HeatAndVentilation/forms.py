from django import forms

from HeatAndVentilation.models.Room import Room


class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = "form-group row"


class BuildingForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = "__all__"
