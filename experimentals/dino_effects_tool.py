#!/usr/bin/env python3
"""
Dinosaur Material Effects decoder (JWE3)

Reads a `.dinosaurmaterialeffects` XML exported by cobra-tools and prints it as
the flat 66-slot material parameter block the shader actually consumes, with the
identified parameter names attached.

Why this exists
- The struct fields are named `a`..`i` / `vec_0..5` / `floats_1..5` because the
  layout was reverse-engineered without the names. The real names live in the
  reflection string pool of `Effects_Final_Win64_SM60.arc` as 52
  `pDinosaurMaterialEffects_*` entries.
- Critically, **the order fields appear in the exported XML is not the slot
  order**. The `Uint` fields are interleaved between the vector/float arrays.
  Reading the XML top-to-bottom gives the wrong slot indices, which is the usual
  reason a slot mapping fails to line up.

This script derives the true order from `DinoEffectsHeader._get_attribute_list()`
so it stays correct if the struct is ever regenerated.

Read-only by default. `--set` rewrites a single slot in place, which is enough to
sweep one parameter at a time when deriving the unconfirmed slots.

Usage
  python dino_effects_tool.py <file.dinosaurmaterialeffects>
  python dino_effects_tool.py <file> --set 36=4280164978
  python dino_effects_tool.py <file> --set 0=int:1        # int-typed float slot
  python dino_effects_tool.py <file> --colour 36=0,120,40,255

Status of the mapping
  PINNED    slots 0-5 (camo), 24 (Damage_DecayModifierIsEnabled),
            and the six colour slots 20/21/27/36/43/64.
  UNPINNED  the remaining ~44 wound/decay/scar slots. The reflection pool order
            does not cleanly satisfy the colour-adjacency constraints, so
            declaration order is not simply file order. Do not assert a specific
            wound slot without re-deriving it.

Note the per-animal *amount* of damage/decay/scar/wither is not in this file at
all -- it is a runtime API on the dinosaurs world API
(`SetDinosaurDamage/Decay/Scar/Wither`, 0..1). This file only styles how those
effects look.
"""
from __future__ import annotations

import argparse
import os
import re
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generated.formats.dinosaurmaterialvariants.structs.DinoEffectsHeader import DinoEffectsHeader

# Slots confirmed against the shader reflection pool and cross-checked on
# multiple species files. Everything absent here is deliberately unnamed.
PINNED_NAMES = {
    0: "Camo_IsEnabled (int)",
    1: "Camo_InfluenceDistance",
    2: "Camo_LuminanceBoostThreshold",
    3: "Camo_DiffuseScaler",
    4: "Camo_SpecularScaler",
    5: "Camo_MaxWeight",
    24: "Damage_DecayModifierIsEnabled (int)",
}

# Packed RGBA8, little-endian: struct.pack("<I", u) then read bytes as R,G,B,A.
# Reading these as ARGB gives nonsense -- that is how the six were identified.
COLOUR_SLOTS = (20, 21, 27, 36, 43, 64)


def slot_layout():
    """Yield (xml_field, element_count) in true file order, skipping pointers."""
    for entry in DinoEffectsHeader._get_attribute_list():
        name, dtype = entry[0], entry[1]
        type_name = getattr(dtype, "__name__", str(dtype))
        if type_name == "Pointer":  # fgm_name, not a parameter slot
            continue
        if type_name == "Vector3f":
            yield name, 3
        elif type_name == "Array":
            shape = entry[2][2]
            yield name, int(shape[0])
        else:
            yield name, 1


def parse(path):
    text = open(path, encoding="utf-8").read()
    values = {}
    for m in re.finditer(r'<(vec_\d)\s+x="([^"]+)"\s+y="([^"]+)"\s+z="([^"]+)"\s*/?>', text):
        values[m.group(1)] = [float(m.group(i)) for i in (2, 3, 4)]
    for m in re.finditer(r"<(floats_\d)>([^<]*)</\1>", text):
        values[m.group(1)] = [float(x) for x in m.group(2).split()]
    header = re.search(r"<DinoEffectsHeader([^>]*)>", text).group(1)
    for key in list("abcdefghi") + ["float"]:
        m = re.search(r'\b%s="([^"]+)"' % key, header)
        if m:
            values[key] = [float(m.group(1)) if key == "float" else int(m.group(1))]
    return text, values


def as_int_bits(value):
    """A denormal in a float slot is a mistyped int -- return it, else None."""
    if isinstance(value, float) and 0 < abs(value) < 1e-30:
        return struct.unpack("<I", struct.pack("<f", value))[0]
    return None


def enumerate_slots(values):
    slot = 0
    for field, count in slot_layout():
        got = values.get(field, [0] * count)
        for index in range(count):
            label = field if count == 1 else "%s[%d]" % (field, index)
            yield slot, field, index, label, got[index] if index < len(got) else 0
            slot += 1


def report(path):
    _, values = parse(path)
    print("%-4s  %-13s %22s  %s" % ("slot", "field", "value", "note"))
    print("-" * 80)
    for slot, _field, _i, label, value in enumerate_slots(values):
        note = PINNED_NAMES.get(slot, "")
        if slot in COLOUR_SLOTS:
            r, g, b, a = struct.pack("<I", int(value))
            note = "COLOUR rgba(%d,%d,%d,%d)" % (r, g, b, a)
        bits = as_int_bits(value)
        if bits is not None:
            note += "  <- int %d" % bits
        print("%-4d  %-13s %22s  %s" % (slot, label, value, note))


def locate(values, target):
    for slot, field, index, label, value in enumerate_slots(values):
        if slot == target:
            return field, index, label, value
    raise SystemExit("slot %d out of range (0-65)" % target)


def write_slot(path, target, raw):
    text, values = parse(path)
    field, index, label, old = locate(values, target)

    if raw.startswith("int:"):  # store an int's bit pattern in a float slot
        new = struct.unpack("<f", struct.pack("<I", int(raw[4:])))[0]
    else:
        new = float(raw) if "." in raw or "e" in raw.lower() else int(raw)

    if field in ("a", "b", "c", "d", "e", "f", "g", "h", "i"):
        pattern = r'(\b%s=")[^"]*(")' % field
        text = re.sub(pattern, lambda m: m.group(1) + str(int(new)) + m.group(2), text, count=1)
    elif field == "float":
        text = re.sub(r'(\bfloat=")[^"]*(")', lambda m: m.group(1) + repr(float(new)) + m.group(2), text, count=1)
    elif field.startswith("vec_"):
        axis = "xyz"[index]
        pattern = r'(<%s\b[^>]*?\b%s=")[^"]*(")' % (field, axis)
        text = re.sub(pattern, lambda m: m.group(1) + repr(float(new)) + m.group(2), text, count=1)
    else:
        nums = list(values[field])
        nums[index] = float(new)
        body = " ".join(repr(n) for n in nums)
        text = re.sub(r"(<%s>)[^<]*(</%s>)" % (field, field),
                      lambda m: m.group(1) + body + m.group(2), text, count=1)

    open(path, "w", encoding="utf-8").write(text)
    print("slot %d (%s): %s -> %s" % (target, label, old, new))


def main():
    ap = argparse.ArgumentParser(description="Decode/patch a .dinosaurmaterialeffects file.")
    ap.add_argument("file")
    ap.add_argument("--set", metavar="SLOT=VALUE", action="append", default=[],
                    help="Write a slot. Use int:N to store an int bit pattern in a float slot.")
    ap.add_argument("--colour", metavar="SLOT=R,G,B,A", action="append", default=[],
                    help="Write a packed RGBA8 colour slot.")
    args = ap.parse_args()

    for item in args.colour:
        slot, _, rgba = item.partition("=")
        r, g, b, a = (int(x) for x in rgba.split(","))
        write_slot(args.file, int(slot), str(struct.unpack("<I", bytes((r, g, b, a)))[0]))
    for item in args.set:
        slot, _, value = item.partition("=")
        write_slot(args.file, int(slot), value)

    report(args.file)


if __name__ == "__main__":
    main()
