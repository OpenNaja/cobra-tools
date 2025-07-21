from generated.formats.achievements.compounds.AchievementsRoot import AchievementsRoot
from modules.formats.BaseFormat import MimeVersionedLoader


class AchievementsLoader(MimeVersionedLoader):
	target_class = AchievementsRoot
	extension = ".achievements"
