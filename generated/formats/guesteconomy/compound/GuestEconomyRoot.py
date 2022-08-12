from generated.formats.base.basic import fmt_member
from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.ovl_base.compound.MemStruct import MemStruct


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

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.target_profit = 0
		self.u_00 = 0
		self.target_dinosaur_prestige = 0
		self.dinosaur_prestige_power = 0
		self.u_01 = 0
		self.u_02 = 0
		self.u_03 = 0
		self.u_04 = 0
		self.visitor_arrival_rate = 0
		self.visitor_departure_rate = 0
		self.u_05 = 0
		self.u_06 = 0
		self.u_07 = 0
		self.u_08 = 0
		self.u_09 = 0
		self.u_10 = 0
		self.u_11 = 0
		self.ticket_price_visitor_proportion_power = 0
		self.ticket_price_full_visitor_proportion = 0
		self.ticket_price_minimum_price_fraction = 0
		self.visitor_deaths_decay_rate = 0
		self.visitor_deaths_limit = 0
		self.danger_exposure_safe_decay_rate = 0
		self.danger_exposure_unnecessary_shelter_punishment = 0
		self.danger_exposure_storm_exposure_punishment = 0
		self.danger_exposure_dinosaur_exposure_punishment = 0
		self.danger_exposure_dinosaur_danger_radius = 0
		self.danger_exposure_limit = 0
		self.transport_rating_disabled = 0
		self.u_12 = 0
		self.u_13 = 0
		self.u_14 = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		print(f'set_defaults {self.__class__.__name__}')
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

	def read(self, stream):
		self.io_start = stream.tell()
		self.read_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		self.write_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.target_profit = stream.read_uint()
		instance.u_00 = stream.read_float()
		instance.target_dinosaur_prestige = stream.read_uint()
		instance.dinosaur_prestige_power = stream.read_float()
		instance.u_01 = stream.read_uint()
		instance.u_02 = stream.read_float()
		instance.u_03 = stream.read_float()
		instance.u_04 = stream.read_float()
		instance.visitor_arrival_rate = stream.read_float()
		instance.visitor_departure_rate = stream.read_float()
		instance.u_05 = stream.read_float()
		instance.u_06 = stream.read_float()
		instance.u_07 = stream.read_float()
		instance.u_08 = stream.read_float()
		instance.u_09 = stream.read_float()
		instance.u_10 = stream.read_float()
		instance.u_11 = stream.read_float()
		instance.ticket_price_visitor_proportion_power = stream.read_float()
		instance.ticket_price_full_visitor_proportion = stream.read_float()
		instance.ticket_price_minimum_price_fraction = stream.read_float()
		instance.visitor_deaths_decay_rate = stream.read_float()
		instance.visitor_deaths_limit = stream.read_float()
		instance.danger_exposure_safe_decay_rate = stream.read_float()
		instance.danger_exposure_unnecessary_shelter_punishment = stream.read_float()
		instance.danger_exposure_storm_exposure_punishment = stream.read_float()
		instance.danger_exposure_dinosaur_exposure_punishment = stream.read_float()
		instance.danger_exposure_dinosaur_danger_radius = stream.read_float()
		instance.danger_exposure_limit = stream.read_float()
		instance.transport_rating_disabled = stream.read_uint()
		instance.u_12 = stream.read_uint()
		instance.u_13 = stream.read_uint()
		instance.u_14 = stream.read_uint()

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint(instance.target_profit)
		stream.write_float(instance.u_00)
		stream.write_uint(instance.target_dinosaur_prestige)
		stream.write_float(instance.dinosaur_prestige_power)
		stream.write_uint(instance.u_01)
		stream.write_float(instance.u_02)
		stream.write_float(instance.u_03)
		stream.write_float(instance.u_04)
		stream.write_float(instance.visitor_arrival_rate)
		stream.write_float(instance.visitor_departure_rate)
		stream.write_float(instance.u_05)
		stream.write_float(instance.u_06)
		stream.write_float(instance.u_07)
		stream.write_float(instance.u_08)
		stream.write_float(instance.u_09)
		stream.write_float(instance.u_10)
		stream.write_float(instance.u_11)
		stream.write_float(instance.ticket_price_visitor_proportion_power)
		stream.write_float(instance.ticket_price_full_visitor_proportion)
		stream.write_float(instance.ticket_price_minimum_price_fraction)
		stream.write_float(instance.visitor_deaths_decay_rate)
		stream.write_float(instance.visitor_deaths_limit)
		stream.write_float(instance.danger_exposure_safe_decay_rate)
		stream.write_float(instance.danger_exposure_unnecessary_shelter_punishment)
		stream.write_float(instance.danger_exposure_storm_exposure_punishment)
		stream.write_float(instance.danger_exposure_dinosaur_exposure_punishment)
		stream.write_float(instance.danger_exposure_dinosaur_danger_radius)
		stream.write_float(instance.danger_exposure_limit)
		stream.write_uint(instance.transport_rating_disabled)
		stream.write_uint(instance.u_12)
		stream.write_uint(instance.u_13)
		stream.write_uint(instance.u_14)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('target_profit', Uint, (0, None))
		yield ('u_00', Float, (0, None))
		yield ('target_dinosaur_prestige', Uint, (0, None))
		yield ('dinosaur_prestige_power', Float, (0, None))
		yield ('u_01', Uint, (0, None))
		yield ('u_02', Float, (0, None))
		yield ('u_03', Float, (0, None))
		yield ('u_04', Float, (0, None))
		yield ('visitor_arrival_rate', Float, (0, None))
		yield ('visitor_departure_rate', Float, (0, None))
		yield ('u_05', Float, (0, None))
		yield ('u_06', Float, (0, None))
		yield ('u_07', Float, (0, None))
		yield ('u_08', Float, (0, None))
		yield ('u_09', Float, (0, None))
		yield ('u_10', Float, (0, None))
		yield ('u_11', Float, (0, None))
		yield ('ticket_price_visitor_proportion_power', Float, (0, None))
		yield ('ticket_price_full_visitor_proportion', Float, (0, None))
		yield ('ticket_price_minimum_price_fraction', Float, (0, None))
		yield ('visitor_deaths_decay_rate', Float, (0, None))
		yield ('visitor_deaths_limit', Float, (0, None))
		yield ('danger_exposure_safe_decay_rate', Float, (0, None))
		yield ('danger_exposure_unnecessary_shelter_punishment', Float, (0, None))
		yield ('danger_exposure_storm_exposure_punishment', Float, (0, None))
		yield ('danger_exposure_dinosaur_exposure_punishment', Float, (0, None))
		yield ('danger_exposure_dinosaur_danger_radius', Float, (0, None))
		yield ('danger_exposure_limit', Float, (0, None))
		yield ('transport_rating_disabled', Uint, (0, None))
		yield ('u_12', Uint, (0, None))
		yield ('u_13', Uint, (0, None))
		yield ('u_14', Uint, (0, None))

	def get_info_str(self, indent=0):
		return f'GuestEconomyRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* target_profit = {fmt_member(self.target_profit, indent+1)}'
		s += f'\n	* u_00 = {fmt_member(self.u_00, indent+1)}'
		s += f'\n	* target_dinosaur_prestige = {fmt_member(self.target_dinosaur_prestige, indent+1)}'
		s += f'\n	* dinosaur_prestige_power = {fmt_member(self.dinosaur_prestige_power, indent+1)}'
		s += f'\n	* u_01 = {fmt_member(self.u_01, indent+1)}'
		s += f'\n	* u_02 = {fmt_member(self.u_02, indent+1)}'
		s += f'\n	* u_03 = {fmt_member(self.u_03, indent+1)}'
		s += f'\n	* u_04 = {fmt_member(self.u_04, indent+1)}'
		s += f'\n	* visitor_arrival_rate = {fmt_member(self.visitor_arrival_rate, indent+1)}'
		s += f'\n	* visitor_departure_rate = {fmt_member(self.visitor_departure_rate, indent+1)}'
		s += f'\n	* u_05 = {fmt_member(self.u_05, indent+1)}'
		s += f'\n	* u_06 = {fmt_member(self.u_06, indent+1)}'
		s += f'\n	* u_07 = {fmt_member(self.u_07, indent+1)}'
		s += f'\n	* u_08 = {fmt_member(self.u_08, indent+1)}'
		s += f'\n	* u_09 = {fmt_member(self.u_09, indent+1)}'
		s += f'\n	* u_10 = {fmt_member(self.u_10, indent+1)}'
		s += f'\n	* u_11 = {fmt_member(self.u_11, indent+1)}'
		s += f'\n	* ticket_price_visitor_proportion_power = {fmt_member(self.ticket_price_visitor_proportion_power, indent+1)}'
		s += f'\n	* ticket_price_full_visitor_proportion = {fmt_member(self.ticket_price_full_visitor_proportion, indent+1)}'
		s += f'\n	* ticket_price_minimum_price_fraction = {fmt_member(self.ticket_price_minimum_price_fraction, indent+1)}'
		s += f'\n	* visitor_deaths_decay_rate = {fmt_member(self.visitor_deaths_decay_rate, indent+1)}'
		s += f'\n	* visitor_deaths_limit = {fmt_member(self.visitor_deaths_limit, indent+1)}'
		s += f'\n	* danger_exposure_safe_decay_rate = {fmt_member(self.danger_exposure_safe_decay_rate, indent+1)}'
		s += f'\n	* danger_exposure_unnecessary_shelter_punishment = {fmt_member(self.danger_exposure_unnecessary_shelter_punishment, indent+1)}'
		s += f'\n	* danger_exposure_storm_exposure_punishment = {fmt_member(self.danger_exposure_storm_exposure_punishment, indent+1)}'
		s += f'\n	* danger_exposure_dinosaur_exposure_punishment = {fmt_member(self.danger_exposure_dinosaur_exposure_punishment, indent+1)}'
		s += f'\n	* danger_exposure_dinosaur_danger_radius = {fmt_member(self.danger_exposure_dinosaur_danger_radius, indent+1)}'
		s += f'\n	* danger_exposure_limit = {fmt_member(self.danger_exposure_limit, indent+1)}'
		s += f'\n	* transport_rating_disabled = {fmt_member(self.transport_rating_disabled, indent+1)}'
		s += f'\n	* u_12 = {fmt_member(self.u_12, indent+1)}'
		s += f'\n	* u_13 = {fmt_member(self.u_13, indent+1)}'
		s += f'\n	* u_14 = {fmt_member(self.u_14, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
