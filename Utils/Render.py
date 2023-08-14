import locale
import os
from docxtpl import DocxTemplate
locale.setlocale(locale.LC_ALL, '')
locale.currency(1234567.89, grouping=True)
import datetime
def render_docx(doc: DocxTemplate, short_context: dict, out_folder, suffix=""):
	""" рендер пояснительной записки suffix для имени файла"""
	doc.render(short_context)
	file_name = f"Энергоэффектвиность_{suffix}_{datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')}.docx"
	doc.save(os.path.join(out_folder, file_name))