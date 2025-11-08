from typing import Union
from generated.base_struct import BaseStruct
from generated.formats.bnk.enums.HircType import HircType
from generated.formats.bnk.structs.BlendContainer import BlendContainer
from generated.formats.bnk.structs.Event import Event
from generated.formats.bnk.structs.EventAction import EventAction
from generated.formats.bnk.structs.MusicSegment import MusicSegment
from generated.formats.bnk.structs.MusicSwitch import MusicSwitch
from generated.formats.bnk.structs.MusicTrack import MusicTrack
from generated.formats.bnk.structs.RanSeqContainer import RanSeqContainer
from generated.formats.bnk.structs.Sound import Sound
from generated.formats.bnk.structs.SwitchContainer import SwitchContainer
from generated.formats.bnk.structs.TypeOther import TypeOther


class HircPointer(BaseStruct):
    id: HircType
    length: int
    data: Union[BlendContainer, Event, EventAction, MusicSegment, MusicSwitch, MusicTrack, RanSeqContainer, Sound, SwitchContainer, TypeOther]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
