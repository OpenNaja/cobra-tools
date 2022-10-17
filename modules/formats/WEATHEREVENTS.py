from generated.formats.weatherevents.compounds.WeatherEventsRoot import WeatherEventsRoot
from modules.formats.BaseFormat import MemStructLoader

class WeatherEventssLoader(MemStructLoader):
	target_class = WeatherEventsRoot
	extension = ".weatherevents"
