from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django_pandas.io import read_frame
from django.db import models


def renamed_dict(model_type: models.Model) -> dict[str, str]:
	names = [f.name for f in model_type._meta.get_fields()]
	res_dict = {}
	for val in names:
		try:
			res_dict[val] = model_type._meta.get_field(val).verbose_name
		except:
			pass
	return res_dict


def create_table_from_model(model_name: models.Model, qs=None):
	qs = qs if qs else model_name.objects.all()
	res_dict = renamed_dict(model_name)
	table1 = (
		read_frame(qs, datetime_index=False)
		.rename(res_dict, axis="columns")
	)
	id_data = table1['ID']
	table1["button"] = f"<a href=''>{id_data}</a>"
	return table1.to_html(
		classes="table table-striped table-bordered",
		table_id="zero_config",
		index=False,
		escape=False
	)


def create_filds_list_for_render(model_name: models.Model, qs=None):
	filds_ = [f.name for f in model_name._meta.get_fields()]
	data = []
	for value in qs:
		temp_list = []
		for fild in filds_:
			temp = getattr(value, fild)
			temp_list.append(temp)
		data.append(temp_list)
	names = renamed_dict(model_name).values()
	return dict(data=data, names=names)


def render_modal_window(pk: int, title: str, modal_body: str):
	return f"""
	<button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal{pk}">
	  Показать Детали
	</button>
	<!-- Modal -->
	<div class="modal fade" id="exampleModal{pk}" tabindex="-1" aria-labelledby="exampleModal{pk}" aria-hidden="true">
	  <div class="modal-dialog modal-xl">
	    <div class="modal-content">
	      <div class="modal-header">
	        <h5 class="modal-title" id="exampleModalLabel"> {title} </h5>
	        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
	      </div>
	      <div class="modal-body">
	          {modal_body}
	      </div>
	      <div class="modal-footer">
	        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" id="close">Close</button>
	      </div>
	    </div>
	  </div>
	</div>
			"""