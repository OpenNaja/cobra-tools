from generated.formats.achievements.structs.AchievementsRoot import AchievementsRoot
from modules.formats.BaseFormat import MimeVersionedLoader


class AchievementsLoader(MimeVersionedLoader):
	target_class = AchievementsRoot
	extension = ".achievements"
