from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class GuestEconomyRoot(MemStruct):

	"""
	JWE2: 128 bytes
	#GuestEconomy = {
	#    some parameters might be missing
	#    TargetTicketPrice = 180,
	#a    TargetProfit = 500000,
	#a    TargetDinosaurPrestige = 5000,
	#    TargetSpeciesVariety = 5,
	#    DinosaurPrestigePower = 0.65,
	#    TargetVisitors = 1000,
	#    VisitorArrivalRate = 750,
	#    VisitorDepartureRate = 1000,
	#    IncomeTaxMinIncome = 0,
	#    IncomeTaxMaxIncome = 0,
	#    IncomeTaxMinProportion = 0,
	#    IncomeTaxMaxProportion = 0,
	#    IncomeTaxCurvePower = 1,
	#    TicketPriceVisitorProportionPower = 0.75,
	#    TicketPriceFullVisitorProportion = 1.5,
	
	#    TicketPriceMinimumPriceFraction = 0.4,
	#    VisitorDeathsDecayRate = 2,
	#    VisitorDeathsLimit = 8,
	#    DangerExposureSafeDecayRate = 4,
	#    DangerExposureUnnecessaryShelterPunishment = 1.5,
	#    DangerExposureStormExposurePunishment = 6,
	#    DangerExposureDinosaurExposurePunishment = 8,
	#    DangerExposureDinosaurDangerRadius = 200,
	#    DangerExposureLimit = 8,
	
	#    TransportRatingDisabled = 0
	#},
	# I f I f I 27f
	"""

	__name__ = GuestEconomyRoot

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.target_profit = 0
		self.u_00 = 0.0
		self.target_dinosaur_prestige = 0
		self.dinosaur_prestige_power = 0.0
		self.u_01 = 0
		self.u_02 = 0.0
		self.u_03 = 0.0
		self.u_04 = 0.0
		self.visitor_arrival_rate = 0.0
		self.visitor_departure_rate = 0.0
		self.u_05 = 0.0
		self.u_06 = 0.0
		self.u_07 = 0.0
		self.u_08 = 0.0
		self.u_09 = 0.0
		self.u_10 = 0.0
		self.u_11 = 0.0
		self.ticket_price_visitor_proportion_power = 0.0
		self.ticket_price_full_visitor_proportion = 0.0
		self.ticket_price_minimum_price_fraction = 0.0
		self.visitor_deaths_decay_rate = 0.0
		self.visitor_deaths_limit = 0.0
		self.danger_exposure_safe_decay_rate = 0.0
		self.danger_exposure_unnecessary_shelter_punishment = 0.0
		self.danger_exposure_storm_exposure_punishment = 0.0
		self.danger_exposure_dinosaur_exposure_punishment = 0.0
		self.danger_exposure_dinosaur_danger_radius = 0.0
		self.danger_exposure_limit = 0.0
		self.transport_rating_disabled = 0
		self.u_12 = 0
		self.u_13 = 0
		self.u_14 = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.target_profit = 0
		self.u_00 = 0.0
		self.target_dinosaur_prestige = 0
		self.dinosaur_prestige_power = 0.0
		self.u_01 = 0
		self.u_02 = 0.0
		self.u_03 = 0.0
		self.u_04 = 0.0
		self.visitor_arrival_rate = 0.0
		self.visitor_departure_rate = 0.0
		self.u_05 = 0.0
		self.u_06 = 0.0
		self.u_07 = 0.0
		self.u_08 = 0.0
		self.u_09 = 0.0
		self.u_10 = 0.0
		self.u_11 = 0.0
		self.ticket_price_visitor_proportion_power = 0.0
		self.ticket_price_full_visitor_proportion = 0.0
		self.ticket_price_minimum_price_fraction = 0.0
		self.visitor_deaths_decay_rate = 0.0
		self.visitor_deaths_limit = 0.0
		self.danger_exposure_safe_decay_rate = 0.0
		self.danger_exposure_unnecessary_shelter_punishment = 0.0
		self.danger_exposure_storm_exposure_punishment = 0.0
		self.danger_exposure_dinosaur_exposure_punishment = 0.0
		self.danger_exposure_dinosaur_danger_radius = 0.0
		self.danger_exposure_limit = 0.0
		self.transport_rating_disabled = 0
		self.u_12 = 0
		self.u_13 = 0
		self.u_14 = 0

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.target_profit = Uint.from_stream(stream, instance.context, 0, None)
		instance.u_00 = Float.from_stream(stream, instance.context, 0, None)
		instance.target_dinosaur_prestige = Uint.from_stream(stream, instance.context, 0, None)
		instance.dinosaur_prestige_power = Float.from_stream(stream, instance.context, 0, None)
		instance.u_01 = Uint.from_stream(stream, instance.context, 0, None)
		instance.u_02 = Float.from_stream(stream, instance.context, 0, None)
		instance.u_03 = Float.from_stream(stream, instance.context, 0, None)
		instance.u_04 = Float.from_stream(stream, instance.context, 0, None)
		instance.visitor_arrival_rate = Float.from_stream(stream, instance.context, 0, None)
		instance.visitor_departure_rate = Float.from_stream(stream, instance.context, 0, None)
		instance.u_05 = Float.from_stream(stream, instance.context, 0, None)
		instance.u_06 = Float.from_stream(stream, instance.context, 0, None)
		instance.u_07 = Float.from_stream(stream, instance.context, 0, None)
		instance.u_08 = Float.from_stream(stream, instance.context, 0, None)
		instance.u_09 = Float.from_stream(stream, instance.context, 0, None)
		instance.u_10 = Float.from_stream(stream, instance.context, 0, None)
		instance.u_11 = Float.from_stream(stream, instance.context, 0, None)
		instance.ticket_price_visitor_proportion_power = Float.from_stream(stream, instance.context, 0, None)
		instance.ticket_price_full_visitor_proportion = Float.from_stream(stream, instance.context, 0, None)
		instance.ticket_price_minimum_price_fraction = Float.from_stream(stream, instance.context, 0, None)
		instance.visitor_deaths_decay_rate = Float.from_stream(stream, instance.context, 0, None)
		instance.visitor_deaths_limit = Float.from_stream(stream, instance.context, 0, None)
		instance.danger_exposure_safe_decay_rate = Float.from_stream(stream, instance.context, 0, None)
		instance.danger_exposure_unnecessary_shelter_punishment = Float.from_stream(stream, instance.context, 0, None)
		instance.danger_exposure_storm_exposure_punishment = Float.from_stream(stream, instance.context, 0, None)
		instance.danger_exposure_dinosaur_exposure_punishment = Float.from_stream(stream, instance.context, 0, None)
		instance.danger_exposure_dinosaur_danger_radius = Float.from_stream(stream, instance.context, 0, None)
		instance.danger_exposure_limit = Float.from_stream(stream, instance.context, 0, None)
		instance.transport_rating_disabled = Uint.from_stream(stream, instance.context, 0, None)
		instance.u_12 = Uint.from_stream(stream, instance.context, 0, None)
		instance.u_13 = Uint.from_stream(stream, instance.context, 0, None)
		instance.u_14 = Uint.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint.to_stream(stream, instance.target_profit)
		Float.to_stream(stream, instance.u_00)
		Uint.to_stream(stream, instance.target_dinosaur_prestige)
		Float.to_stream(stream, instance.dinosaur_prestige_power)
		Uint.to_stream(stream, instance.u_01)
		Float.to_stream(stream, instance.u_02)
		Float.to_stream(stream, instance.u_03)
		Float.to_stream(stream, instance.u_04)
		Float.to_stream(stream, instance.visitor_arrival_rate)
		Float.to_stream(stream, instance.visitor_departure_rate)
		Float.to_stream(stream, instance.u_05)
		Float.to_stream(stream, instance.u_06)
		Float.to_stream(stream, instance.u_07)
		Float.to_stream(stream, instance.u_08)
		Float.to_stream(stream, instance.u_09)
		Float.to_stream(stream, instance.u_10)
		Float.to_stream(stream, instance.u_11)
		Float.to_stream(stream, instance.ticket_price_visitor_proportion_power)
		Float.to_stream(stream, instance.ticket_price_full_visitor_proportion)
		Float.to_stream(stream, instance.ticket_price_minimum_price_fraction)
		Float.to_stream(stream, instance.visitor_deaths_decay_rate)
		Float.to_stream(stream, instance.visitor_deaths_limit)
		Float.to_stream(stream, instance.danger_exposure_safe_decay_rate)
		Float.to_stream(stream, instance.danger_exposure_unnecessary_shelter_punishment)
		Float.to_stream(stream, instance.danger_exposure_storm_exposure_punishment)
		Float.to_stream(stream, instance.danger_exposure_dinosaur_exposure_punishment)
		Float.to_stream(stream, instance.danger_exposure_dinosaur_danger_radius)
		Float.to_stream(stream, instance.danger_exposure_limit)
		Uint.to_stream(stream, instance.transport_rating_disabled)
		Uint.to_stream(stream, instance.u_12)
		Uint.to_stream(stream, instance.u_13)
		Uint.to_stream(stream, instance.u_14)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'target_profit', Uint, (0, None), (False, None)
		yield 'u_00', Float, (0, None), (False, None)
		yield 'target_dinosaur_prestige', Uint, (0, None), (False, None)
		yield 'dinosaur_prestige_power', Float, (0, None), (False, None)
		yield 'u_01', Uint, (0, None), (False, None)
		yield 'u_02', Float, (0, None), (False, None)
		yield 'u_03', Float, (0, None), (False, None)
		yield 'u_04', Float, (0, None), (False, None)
		yield 'visitor_arrival_rate', Float, (0, None), (False, None)
		yield 'visitor_departure_rate', Float, (0, None), (False, None)
		yield 'u_05', Float, (0, None), (False, None)
		yield 'u_06', Float, (0, None), (False, None)
		yield 'u_07', Float, (0, None), (False, None)
		yield 'u_08', Float, (0, None), (False, None)
		yield 'u_09', Float, (0, None), (False, None)
		yield 'u_10', Float, (0, None), (False, None)
		yield 'u_11', Float, (0, None), (False, None)
		yield 'ticket_price_visitor_proportion_power', Float, (0, None), (False, None)
		yield 'ticket_price_full_visitor_proportion', Float, (0, None), (False, None)
		yield 'ticket_price_minimum_price_fraction', Float, (0, None), (False, None)
		yield 'visitor_deaths_decay_rate', Float, (0, None), (False, None)
		yield 'visitor_deaths_limit', Float, (0, None), (False, None)
		yield 'danger_exposure_safe_decay_rate', Float, (0, None), (False, None)
		yield 'danger_exposure_unnecessary_shelter_punishment', Float, (0, None), (False, None)
		yield 'danger_exposure_storm_exposure_punishment', Float, (0, None), (False, None)
		yield 'danger_exposure_dinosaur_exposure_punishment', Float, (0, None), (False, None)
		yield 'danger_exposure_dinosaur_danger_radius', Float, (0, None), (False, None)
		yield 'danger_exposure_limit', Float, (0, None), (False, None)
		yield 'transport_rating_disabled', Uint, (0, None), (False, None)
		yield 'u_12', Uint, (0, None), (False, None)
		yield 'u_13', Uint, (0, None), (False, None)
		yield 'u_14', Uint, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'GuestEconomyRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* target_profit = {self.fmt_member(self.target_profit, indent+1)}'
		s += f'\n	* u_00 = {self.fmt_member(self.u_00, indent+1)}'
		s += f'\n	* target_dinosaur_prestige = {self.fmt_member(self.target_dinosaur_prestige, indent+1)}'
		s += f'\n	* dinosaur_prestige_power = {self.fmt_member(self.dinosaur_prestige_power, indent+1)}'
		s += f'\n	* u_01 = {self.fmt_member(self.u_01, indent+1)}'
		s += f'\n	* u_02 = {self.fmt_member(self.u_02, indent+1)}'
		s += f'\n	* u_03 = {self.fmt_member(self.u_03, indent+1)}'
		s += f'\n	* u_04 = {self.fmt_member(self.u_04, indent+1)}'
		s += f'\n	* visitor_arrival_rate = {self.fmt_member(self.visitor_arrival_rate, indent+1)}'
		s += f'\n	* visitor_departure_rate = {self.fmt_member(self.visitor_departure_rate, indent+1)}'
		s += f'\n	* u_05 = {self.fmt_member(self.u_05, indent+1)}'
		s += f'\n	* u_06 = {self.fmt_member(self.u_06, indent+1)}'
		s += f'\n	* u_07 = {self.fmt_member(self.u_07, indent+1)}'
		s += f'\n	* u_08 = {self.fmt_member(self.u_08, indent+1)}'
		s += f'\n	* u_09 = {self.fmt_member(self.u_09, indent+1)}'
		s += f'\n	* u_10 = {self.fmt_member(self.u_10, indent+1)}'
		s += f'\n	* u_11 = {self.fmt_member(self.u_11, indent+1)}'
		s += f'\n	* ticket_price_visitor_proportion_power = {self.fmt_member(self.ticket_price_visitor_proportion_power, indent+1)}'
		s += f'\n	* ticket_price_full_visitor_proportion = {self.fmt_member(self.ticket_price_full_visitor_proportion, indent+1)}'
		s += f'\n	* ticket_price_minimum_price_fraction = {self.fmt_member(self.ticket_price_minimum_price_fraction, indent+1)}'
		s += f'\n	* visitor_deaths_decay_rate = {self.fmt_member(self.visitor_deaths_decay_rate, indent+1)}'
		s += f'\n	* visitor_deaths_limit = {self.fmt_member(self.visitor_deaths_limit, indent+1)}'
		s += f'\n	* danger_exposure_safe_decay_rate = {self.fmt_member(self.danger_exposure_safe_decay_rate, indent+1)}'
		s += f'\n	* danger_exposure_unnecessary_shelter_punishment = {self.fmt_member(self.danger_exposure_unnecessary_shelter_punishment, indent+1)}'
		s += f'\n	* danger_exposure_storm_exposure_punishment = {self.fmt_member(self.danger_exposure_storm_exposure_punishment, indent+1)}'
		s += f'\n	* danger_exposure_dinosaur_exposure_punishment = {self.fmt_member(self.danger_exposure_dinosaur_exposure_punishment, indent+1)}'
		s += f'\n	* danger_exposure_dinosaur_danger_radius = {self.fmt_member(self.danger_exposure_dinosaur_danger_radius, indent+1)}'
		s += f'\n	* danger_exposure_limit = {self.fmt_member(self.danger_exposure_limit, indent+1)}'
		s += f'\n	* transport_rating_disabled = {self.fmt_member(self.transport_rating_disabled, indent+1)}'
		s += f'\n	* u_12 = {self.fmt_member(self.u_12, indent+1)}'
		s += f'\n	* u_13 = {self.fmt_member(self.u_13, indent+1)}'
		s += f'\n	* u_14 = {self.fmt_member(self.u_14, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
