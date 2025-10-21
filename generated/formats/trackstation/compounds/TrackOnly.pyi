from generated.formats.trackstation.compounds.CommonChunk import CommonChunk


class TrackOnly(CommonChunk):
    zero_2: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
