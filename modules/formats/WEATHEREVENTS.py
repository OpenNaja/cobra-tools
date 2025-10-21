from generated.formats.weatherevents.structs.WeatherEventsRoot import WeatherEventsRoot
from modules.formats.BaseFormat import MemStructLoader

class WeatherEventssLoader(MemStructLoader):
	target_class = WeatherEventsRoot
	extension = ".weatherevents"
