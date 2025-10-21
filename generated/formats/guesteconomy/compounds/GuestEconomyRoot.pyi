from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class GuestEconomyRoot(MemStruct):
    target_profit: int
    u_00: float
    target_dinosaur_prestige: int
    dinosaur_prestige_power: float
    u_01: int
    u_02: float
    u_03: float
    u_04: float
    visitor_arrival_rate: float
    visitor_departure_rate: float
    u_05: float
    u_06: float
    u_07: float
    u_08: float
    u_09: float
    u_10: float
    u_11: float
    ticket_price_visitor_proportion_power: float
    ticket_price_full_visitor_proportion: float
    ticket_price_minimum_price_fraction: float
    visitor_deaths_decay_rate: float
    visitor_deaths_limit: float
    danger_exposure_safe_decay_rate: float
    danger_exposure_unnecessary_shelter_punishment: float
    danger_exposure_storm_exposure_punishment: float
    danger_exposure_dinosaur_exposure_punishment: float
    danger_exposure_dinosaur_danger_radius: float
    danger_exposure_limit: float
    transport_rating_disabled: int
    u_12: int
    u_13: int
    u_14: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
