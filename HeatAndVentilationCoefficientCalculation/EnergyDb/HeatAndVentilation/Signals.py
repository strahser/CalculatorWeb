from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from HeatAndVentilation.models.BaseStructure import BaseStructure
from HeatAndVentilation.models.Structure import Structure
from HeatAndVentilation.models.StructureLayer import StructureLayer


@receiver(post_save, sender="HeatAndVentilation.BaseStructure")
def change_R_real(instance, **kwargs):
	qs = Structure.objects.filter(base_structures__id=instance.id).all()
	qs.update(R_real=instance.R_custom, standard_structure_type=instance.standard_structure_type)


# Connect the signal to the signal handler
post_save.connect(change_R_real, sender="HeatAndVentilation.BaseStructure")


@receiver(pre_save, sender="HeatAndVentilation.BaseStructure")
def change_R_real_by_layers(instance, **kwargs):
	layers_qs = StructureLayer.objects.select_related('base_structure').filter(base_structure__id=instance.id).all()
	r_calc = round(
		1 / 23 + sum([val.thickness_layer * 0.001 / val.lambda_structure_layer for val in layers_qs]) + 1 / 8.7, 2)
	qs = BaseStructure.objects.filter(id=instance.id)
	instance.R_custom = r_calc


# Connect the signal to the signal handler
pre_save.connect(change_R_real_by_layers, sender="HeatAndVentilation.BaseStructure")