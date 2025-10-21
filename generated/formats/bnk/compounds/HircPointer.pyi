from typing import Union
from generated.base_struct import BaseStruct
from generated.formats.bnk.compounds.Event import Event
from generated.formats.bnk.compounds.EventAction import EventAction
from generated.formats.bnk.compounds.MusicSegment import MusicSegment
from generated.formats.bnk.compounds.MusicSwitch import MusicSwitch
from generated.formats.bnk.compounds.MusicTrack import MusicTrack
from generated.formats.bnk.compounds.RanSeqContainer import RanSeqContainer
from generated.formats.bnk.compounds.Sound import Sound
from generated.formats.bnk.compounds.SwitchContainer import SwitchContainer
from generated.formats.bnk.compounds.TypeOther import TypeOther
from generated.formats.bnk.enums.HircType import HircType


class HircPointer(BaseStruct):
    id: HircType
    length: int
    data: Union[Event, EventAction, MusicSegment, MusicSwitch, MusicTrack, RanSeqContainer, Sound, SwitchContainer, TypeOther]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
