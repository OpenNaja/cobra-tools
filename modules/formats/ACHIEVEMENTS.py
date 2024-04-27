from generated.formats.achievements.compounds.AchievementsRoot import AchievementsRoot
from modules.formats.BaseFormat import MemStructLoader


class AchievementsLoader(MemStructLoader):
	target_class = AchievementsRoot
	extension = ".achievements"
