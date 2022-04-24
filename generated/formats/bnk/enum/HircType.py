from source.formats.base.basic import fmt_member
from generated.formats.base.enum import UbyteEnum


class HircType(UbyteEnum):
	NONE = 0
	Settings = 1
	SoundSfxVoice = 2
	EventAction = 3
	Event = 4
	RandomOrSequenceContainer = 5
	SwitchContainer = 6
	ActorMixer = 7
	AudioBus = 8
	BlendContainer = 9
	MusicSegment = 10
	MusicTrack = 11
	MusicSwitchContainer = 12
	MusicPlaylistContainer = 13
	Attenuation = 14
	DialogueEvent = 15
	MotionBus = 16
	MotionFX = 17
	Effect = 18
	AuxiliaryBus = 20
