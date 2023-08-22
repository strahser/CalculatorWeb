import locale
import os
from docxtpl import DocxTemplate
locale.setlocale(locale.LC_ALL, '')
locale.currency(1234567.89, grouping=True)
import datetime
def render_docx(template_path:str, short_context: dict, out_folder:str,doc_name:str="Энергоэффектвиность_", suffix=""):
	""" рендер пояснительной записки suffix для имени файла"""
	doc = DocxTemplate(template_path)
	doc.render(short_context)
	file_name = f"{doc_name}{suffix}_{datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')}.docx"
	doc.save(os.path.join(out_folder, file_name))