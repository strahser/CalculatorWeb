from django import forms

from HeatAndVentilation.models.Room import Room
from HeatAndVentilation.models.Structure import Structure
from HeatAndVentilation.models.StructureLayer import StructureLayer
import calculation

from HeatAndVentilationCoefficientCalculation.StaticData.StructureTypeData import StructureTypeData
from .fields import GroupedModelChoiceField
from .models.BaseStructure import BaseStructure


class BaseForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields.values():
			field.widget.attrs['class'] = "form-group row"


class BuildingForm(forms.ModelForm):
	class Meta:
		model = Room
		fields = "__all__"


class StructureForm(forms.ModelForm):
	quantity = forms.DecimalField(label='количество')
	price = forms.DecimalField(label='цена')
	area = forms.DecimalField(
		widget=calculation.FormulaInput('quantity*price'), label='Площадь'  # <- using single math expression
	)
	structure_type = forms.ChoiceField(choices=[(val.name, val.value) for val in StructureTypeData],label="Типовая Конструкция")

	class Meta:
		model = Structure
		fields = ['name', 'orientation', 'room', 'structure_type', 'base_structures', 'short_name', 'area', 'quantity',
		          'price', ]
		widgets = {
			'base_structures': forms.Select(
				attrs={'class': 'form-control', 'readonly': True}
			)
		}


class StructureLayerForm(forms.ModelForm):
	class Meta:
		fields = "__all__"
		model = StructureLayer
		widgets = {
			'base_structure': forms.Select(
				attrs={'class': 'form-control', 'readonly': True}
			)
		}
