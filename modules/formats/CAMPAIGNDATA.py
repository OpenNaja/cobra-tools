from generated.formats.campaigndata.structs.CampaignDataRoot import CampaignDataRoot
from modules.formats.BaseFormat import MemStructLoader


class CampaignDataLoader(MemStructLoader):
    target_class = CampaignDataRoot
    extension = ".campaigndata"
