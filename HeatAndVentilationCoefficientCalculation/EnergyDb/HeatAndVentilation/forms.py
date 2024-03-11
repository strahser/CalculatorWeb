from django import forms
import calculation
from django.forms import CheckboxInput

from HeatAndVentilation.models.BaseStructure import BaseStructure
from HeatAndVentilation.models.Building import Building
from HeatAndVentilation.models.Room import Room
from HeatAndVentilation.models.Structure import Structure
from HeatAndVentilation.models.StructureLayer import StructureLayer
from HeatAndVentilationCoefficientCalculation.StaticData.StructureTypeData import StructureTypeData


class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = "form-group row"


class BuildingSelectedForm(forms.Form):
    qs = Building.objects.all()
    selected_building = forms.ModelChoiceField(
        label="Выберите здание",
        queryset=qs,
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-control'}, ),
    )
    create_report = forms.BooleanField(required=False,
                                            initial=False,
                                            label='создать отчет?')


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = "__all__"


class StructureForm(forms.ModelForm):
    width = forms.DecimalField(label='Ширина', initial=1, help_text='введите для расчета площади автоматически')
    length = forms.DecimalField(label='Длина', initial=1, help_text='введите для расчета площади автоматически')
    quantity = forms.DecimalField(label='Колличество конструкций', initial=1,
                                  help_text='введите для расчета площади автоматически')
    area = forms.DecimalField(
        widget=calculation.FormulaInput('width*length*quantity'), label='Площадь Конструкции',
        help_text='введите площадь, или расчитайте автоматически'  # <- using single math expression
    )
    structure_type = forms.ChoiceField(choices=[(val.name, val.value) for val in StructureTypeData],
                                       label="Типовая Конструкция",
                                       )

    class Meta:
        model = Structure
        fields = ['name', 'orientation', 'room', 'structure_type',
                  'base_structures', 'short_name', 'area', 'width', 'length', 'quantity']
        widgets = {
            'base_structures': forms.Select(
                attrs={'class': 'form-control', 'readonly': True, }
            ),
        }


class BaseStructureForm(forms.ModelForm):
    class Meta:
        model = BaseStructure
        fields = "__all__"


class StructureLayerForm(forms.ModelForm):
    class Meta:
        fields = "__all__"
        model = StructureLayer
        widgets = {
            'base_structure': forms.Select(
                attrs={'class': 'form-control', 'readonly': True}
            )
        }
