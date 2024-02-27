import pandas as pd
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django_pandas.io import read_frame
from django.db import models
from django.template.loader import render_to_string


def button_link(url: str, name: str = "изменить", cls='info'):
    return f'<a href="{url}"class="btn btn-{cls} mr-5"   role="button">{name}</a>'


def df_html(df: pd.DataFrame, table_id="zero_config") -> str:
    """Обертка со стилями для экспорта дата фрейм в html"""
    return df.to_html(index=False, classes="table table-striped table-bordered ", border=1, render_links=True,
                      justify='center', escape=False, table_id=table_id)


def renamed_dict(model_type: models.Model) -> dict[str, str]:
    """переименовываем столбцы модели django согласно заданному verbose name """
    names = [f.name for f in model_type._meta.get_fields()]
    res_dict = {}
    for val in names:
        try:
            res_dict[val] = model_type._meta.get_field(val).verbose_name
        except:
            pass
    return res_dict


def create_table_from_model(model_name: models.Model, qs=None, table_id="zero_config") -> str:
    """создаем таблицу на основе модели django (выбираем все записи если qs не задан) через библиотеку
    django_pandas read_frame добавляем столбец с пустой ссылкой на id модели
    задаем id для data table рендера
    """
    qs = qs if qs else model_name.objects.all()
    res_dict = renamed_dict(model_name)
    table1 = (
        read_frame(qs, datetime_index=False)
        .rename(res_dict, axis="columns")
    )
    id_data = table1['ID']
    table1["button"] = f"<a href=''>{id_data}</a>"
    return df_html(table1)


def create_fields_list_for_render(model_name: models.Model, qs=None):
    fields_ = [f.name for f in model_name._meta.get_fields()]
    data = []
    for value in qs:
        temp_list = []
        for fild in fields_:
            temp = getattr(value, fild)
            temp_list.append(temp)
        data.append(temp_list)
    names = renamed_dict(model_name).values()
    return dict(data=data, names=names)


def render_modal_window(pk: int, title: str, modal_body: str, button_name='Детали'):
    context = dict(pk=pk, title=title, modal_body=modal_body, button_name=button_name)
    return f"""
    	<button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal{pk}">
        {button_name}
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