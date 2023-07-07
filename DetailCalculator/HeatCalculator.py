class HeatCalculator:

	def _calculate_heating_yer_consumption(self):
		"""
        Расход тепловой энергии на отопление и вентиляцию здания за отопительный
        период Q_от^год, кВт·ч/год, следует определять по формуле
        """
		self.Qот = 0.024 * self.ГСОП * self.Vот * self.q_р_от
		return self.Qот

	def _calculate_heating_yer_consumption_local(self):
		"""
        Опеределяем Удельный годовой расход тепловой энергии на отопление и вентиляцию МКД, кВт∙ч/м2:
        """
		self.qot = round(self.Qот / (self.Aкв + self.Aпнж), 2)

	def _calculate_hort_water_yer_consumption(self):
		"""
        Удельный годовой расход тепловой энергии на горячее водоснабжение МКД, кВт∙ч/м2:
        """

		self.q_gv = round(self.Qgv / (self.Aкв + self.Aпнж))

	def _calculate_hort_water_day_consumption(self):
		"""
        Определяем среднесуточный расход горячей воды для квартир МКД за сутки, м3/сут:
        """
		self.Vgv_g = round(85 * self.Nж * 0.001 * ((self.zot + self.alpha * (355 - self.zot)) / 365), 2)
		
	def get_q_base():
		V_от = 1000
		GSOP = 2000
		q_gsop = 4.74 / (0.00013 * GSOP + 0.61)
		v_base = V_от / (V_от ** (1 / 3))
		k_ob_tr = q_gsop * v_base