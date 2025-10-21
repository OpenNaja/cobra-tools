from generated.formats.campaigndata.structs.MissionData import MissionData
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class CampaignDataRoot(MemStruct):
    campaign_name: Pointer[str]
    campaign_description: Pointer[str]
    campaign_unknown: int
    chapter_list: ArrayPointer[MissionData]
    chapter_count: int
    chapter_unknown: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
