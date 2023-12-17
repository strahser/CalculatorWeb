from pytexit import py2tex
import streamlit as st
from dataclasses import dataclass, field


@dataclass()
class Formula:
	formula_name: str
	formula_value: float
	formula_abstract: str
	formula_val_calculation: str

	def render(self):
		st.write(f"Определяем {self.formula_name} по формуле")
		st.write(self.formula_name, "=", py2tex(self.formula_abstract))
		st.write(self.formula_name, "=", py2tex(self.formula_val_calculation + "==" + str(self.formula_value)))

# region render
# gsop_formula = Formula("GSOP", GSOP, f'(t_in- t_ot)*z_ot', f'({t_in}- {t_ot})*{z_ot}')
# r_norm_wall = Formula("R_wall_norm", R_wall_norm, "0.00035*GSOP+1.4", f"0.00035*{GSOP}+1.4")
# gsop_formula.render()
# r_norm_wall.render()
# endregion
