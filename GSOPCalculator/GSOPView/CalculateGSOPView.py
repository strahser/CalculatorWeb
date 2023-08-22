import pandas as pd
import streamlit as st

from EnergyCompare.Utility.MakeGrid import make_grid
from GSOPCalculator.GSOPModel.CityLabels import CityLabels
from GSOPCalculator.Static.GSOPNamesStatic import GSOPNamesStatic

class CalculateGSOPView:
    def __init__(self):
        self.all_city:list[str] = None
        self.all_regions:list[str]  = None
        self.unique_city = None

    def create_view(self, df: pd.DataFrame):
        self.choose_city_select_option = st.radio(
            CityLabels.choose_city.value,
            [CityLabels.all_city.value, CityLabels.region_city.value],
            horizontal=True,
        )

        grid = make_grid(4, (2, 2, 8))
        if self.choose_city_select_option == CityLabels.all_city.value:
            grid[0][0].write(CityLabels.choose_city.value)
            self.selected_city = grid[0][1].selectbox(
                CityLabels.choose_city.value,
                options=self.all_city,
                key="all city",
                label_visibility="collapsed",
            )
            self.selected_region = None
        else:
            self._select_city(df, grid)

    def _select_city(self, df: pd.DataFrame, grid):
        grid[0][0].write(CityLabels.choose_region.value)
        self.selected_region = grid[0][1].selectbox(
            CityLabels.choose_region.value,
            options=self.all_regions,
            label_visibility="collapsed",
        )
        unique_city = df[df[GSOPNamesStatic.region] == self.selected_region]
        unique_city = unique_city[GSOPNamesStatic.city].unique()
        grid[1][0].write(CityLabels.choose_city.value)
        self.selected_city = grid[1][1].selectbox(
            CityLabels.choose_city.value,
            options=unique_city,
            key="region city",
            label_visibility="collapsed",
        )
