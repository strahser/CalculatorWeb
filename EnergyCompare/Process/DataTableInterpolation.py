import numpy as np
import pandas as pd
from EnergyCompare.Models.EnergyModels import InterpolateDb, BaseNames


class DataTableInterpolation:
	def __init__(self, input_data_frame: pd.DataFrame):
		"""input_data_frame loaded excel table"""
		self.df = input_data_frame

	def interpolate_df(self, gsop_data: float, levlel_number: int) -> pd.DataFrame:
		"""
		получаем значение интерполяции в зависимости от ГСОП и этажности. Оборачиваем в Data Frame
		 что бы дальше можно было добавить класс энергоэффективности с рассчетными процентами
		 """
		levlel_number = 12 if levlel_number>12 else levlel_number
		new_arr_df = self._transform_df()
		query_filter = new_arr_df[new_arr_df["level"] == levlel_number]
		new_array_df_local = pd.DataFrame(
			{BaseNames.base_name.value: [np.interp(gsop_data, query_filter.gsop, query_filter.q_base_norm)]})
		return new_array_df_local

	@staticmethod
	def bilinear_interpolation(x, y, points):
		'''Interpolate (x,y) from values associated with four points.

		The four points are a list of four triplets:  (x, y, value).
	    The four points can be in any order.  They should form a rectangle.


	        >>> bilinear_interpolation(12, 5.5,
	        ...                        [(10, 4, 100),
	        ...                         (20, 4, 200),
	        ...                         (10, 6, 150),
	        ...                         (20, 6, 300)])
	        165.0
		st.write(bilinear_interpolation(2000, 4, [(2000, 2, 215), (3000, 2, 228), (2000, 4, 206), (3000, 4, 216)]))
		# data_db_ = [(db.gsop, db.level, db.q_base_norm) for db in new_arr]  # for bilinear_interpolation interpolation
	    '''
		# See formula at:  http://en.wikipedia.org/wiki/Bilinear_interpolation

		points = sorted(points)  # order points by x, then by y
		(x1, y1, q11), (_x1, y2, q12), (x2, _y1, q21), (_x2, _y2, q22) = points

		if x1 != _x1 or x2 != _x2 or y1 != _y1 or y2 != _y2:
			raise ValueError('points do not form a rectangle')
		if not x1 <= x <= x2 or not y1 <= y <= y2:
			raise ValueError('(x, y) not within the rectangle')

		return (q11 * (x2 - x) * (y2 - y) +
		        q21 * (x - x1) * (y2 - y) +
		        q12 * (x2 - x) * (y - y1) +
		        q22 * (x - x1) * (y - y1)
		        ) / ((x2 - x1) * (y2 - y1) + 0.0)

	@staticmethod
	def _add_row(df_numpy, col_number):
		new_arr = []
		for en, col in enumerate(df_numpy[:][0]):
			if col_number != 0 and en != 0:
				db_ = InterpolateDb(df_numpy[col_number][0], df_numpy[0][en], df_numpy[col_number][en])
				new_arr.append(db_)
		return new_arr

	@staticmethod
	def _add_column(df_numpy):
		new_arr = []
		for en_row, row in enumerate(enumerate(df_numpy, start=1)):
			row = DataTableInterpolation._add_row(df_numpy, en_row)
			new_arr.extend(row)
		return new_arr

	def _transform_df(self) -> np.array:
		df_n = self.df.to_numpy()
		df_n = np.vstack([self.df.columns, df_n])
		return pd.DataFrame(self._add_column(df_n))
