import re


def bitflag(bit: str) -> str:
    if bit is not None:
        return "0x%08X" % (1 << int(bit))

    return bit


def escape_backslashes(text: str) -> str:
    if text is not None:
        return text.replace('\\', '\\\\')

    return text


def hex_string(number: str) -> str:
    if number is not None:
        return "0x%08X" % int(number, base=0)

    return number


def enum_name(text: str) -> str:
    # This could maybe use an upper(), but maybe we should leave the enum names as they are
    if text is not None:
        return re.sub('[^a-zA-Z0-9_]', '_', text)

    return text


def field_name(text: str) -> str:
    if text is not None:
        return re.sub('[^a-zA-Z0-9_]', '_', text).lower()

    return text


def to_basic_type(type: str) -> str:
    # Temporary, these would likely be patched via a preprocessor
    if type is not None:
        if type == 'ulittle32':
            return 'basic.ulittle32'
        if type == 'int':
            return 'basic.int'
        if type == 'uint':
            return 'basic.uint'
        if type == 'uint64':
            return 'basic.int64'
        if type == 'uint':
            return 'basic.uint64'
        if type == 'byte':
            return 'basic.byte'
        if type == 'char':
            return 'basic.char'
        if type == 'short':
            return 'basic.short'
        if type == 'ushort':
            return 'basic.ushort'
        if type == 'float':
            return 'basic.float'
        if type == 'BlockTypeIndex':
            return 'basic.BlockTypeIndex'
        if type == 'StringIndex':
            return 'basic.StringIndex'
        if type == 'StringOffset':
            return 'basic.StringOffset'
        if type == 'FileVersion':
            return 'basic.FileVersion'
        if type == 'NiFixedString':
            return 'basic.NiFixedString'
        if type == 'Ref':
            return 'basic.Ref'
        if type == 'Ptr':
            return 'basic.Ptr'

    return type
