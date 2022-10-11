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

	__name__ = 'GuestEconomyRoot'

	_import_key = 'guesteconomy.compounds.GuestEconomyRoot'

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

	_attribute_list = MemStruct._attribute_list + [
		('target_profit', Uint, (0, None), (False, None), None),
		('u_00', Float, (0, None), (False, None), None),
		('target_dinosaur_prestige', Uint, (0, None), (False, None), None),
		('dinosaur_prestige_power', Float, (0, None), (False, None), None),
		('u_01', Uint, (0, None), (False, None), None),
		('u_02', Float, (0, None), (False, None), None),
		('u_03', Float, (0, None), (False, None), None),
		('u_04', Float, (0, None), (False, None), None),
		('visitor_arrival_rate', Float, (0, None), (False, None), None),
		('visitor_departure_rate', Float, (0, None), (False, None), None),
		('u_05', Float, (0, None), (False, None), None),
		('u_06', Float, (0, None), (False, None), None),
		('u_07', Float, (0, None), (False, None), None),
		('u_08', Float, (0, None), (False, None), None),
		('u_09', Float, (0, None), (False, None), None),
		('u_10', Float, (0, None), (False, None), None),
		('u_11', Float, (0, None), (False, None), None),
		('ticket_price_visitor_proportion_power', Float, (0, None), (False, None), None),
		('ticket_price_full_visitor_proportion', Float, (0, None), (False, None), None),
		('ticket_price_minimum_price_fraction', Float, (0, None), (False, None), None),
		('visitor_deaths_decay_rate', Float, (0, None), (False, None), None),
		('visitor_deaths_limit', Float, (0, None), (False, None), None),
		('danger_exposure_safe_decay_rate', Float, (0, None), (False, None), None),
		('danger_exposure_unnecessary_shelter_punishment', Float, (0, None), (False, None), None),
		('danger_exposure_storm_exposure_punishment', Float, (0, None), (False, None), None),
		('danger_exposure_dinosaur_exposure_punishment', Float, (0, None), (False, None), None),
		('danger_exposure_dinosaur_danger_radius', Float, (0, None), (False, None), None),
		('danger_exposure_limit', Float, (0, None), (False, None), None),
		('transport_rating_disabled', Uint, (0, None), (False, None), None),
		('u_12', Uint, (0, None), (False, None), None),
		('u_13', Uint, (0, None), (False, None), None),
		('u_14', Uint, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
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
