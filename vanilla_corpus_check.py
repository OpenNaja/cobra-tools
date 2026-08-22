"""Guard against the format model drifting when a reader or schema is edited.

A round trip through cobra proves the reader and writer agree with each other. It does
not prove either matches the format - mirror-image errors survive it intact. This checks
something external instead: does a fixed set of SHIPPED, UNMODIFIED game files still
parse the way it did before the change?

    python vanilla_corpus_check.py --update     # record the baseline (do this on a known-good tree)
    python vanilla_corpus_check.py              # verify nothing drifted

A changed signature is not automatically a bug - `CompressedHeaderReader` legitimately
changed it when 11/12 Indoraptor bundles became 12/12, because that change was anchored
to ACL's documented tag 0xAC11DB01. The rule is that a changed signature REQUIRES AN
EXTERNAL CITATION: a spec, a shipped Frontier asset, or the game itself. "The tests pass
now" is not a citation, and that is exactly the failure this file exists to catch.

Corpus paths live in vanilla_corpus.json next to this file, so the list can grow without
touching the code. Keep every entry a pristine vanilla file - a modified one silently
turns the baseline into a record of the modification.
"""
import argparse
import hashlib
import json
import logging
import os
import sys
import traceback

REPO = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.join(REPO, "vanilla_corpus.json")

logging.disable(logging.CRITICAL)
logging.success = lambda *a, **k: None  # cobra installs this at CLI startup


def digest(parts):
    return hashlib.sha256("\n".join(str(p) for p in parts).encode("utf-8")).hexdigest()[:20]


def sig_ovl(path, game):
    """Names, archive layout, pool counts and buffer sizes - the structural skeleton."""
    from generated.formats.ovl import OvlFile
    from utils.config import Config
    ovl = OvlFile()
    cfg = Config(REPO)
    cfg.load()
    ovl.cfg = cfg
    ovl.game = game
    ovl.load_hash_table()
    ovl.load(path)
    parts = [f"files={len(ovl.loaders)}", f"archives={len(ovl.archives)}"]
    for name in sorted(ovl.loaders):
        loader = ovl.loaders[name]
        entries = []
        for arch, entry in sorted(getattr(loader, "data_entries", {}).items()):
            entries.append(f"{arch}:{[len(b) for b in entry.buffer_datas]}")
        parts.append(f"{name}|{';'.join(entries)}")
    for archive in ovl.archives:
        parts.append(f"arc {archive.name} pools={len(archive.content.pools)}")
    return digest(parts)


def sig_manis(path, game):
    """Clip count, dtypes, frame/bone counts and the channel maps."""
    from generated.formats.manis import ManisFile
    manis = ManisFile()
    manis.load(path)
    parts = [f"version={manis.version}", f"mani_version={manis.context.mani_version}",
             f"clips={len(manis.mani_infos)}"]
    for mi in manis.mani_infos:
        keys = getattr(mi, "keys", None)
        maps = "none"
        if keys is not None:
            maps = "|".join(",".join(str(int(x)) for x in getattr(keys, attr))
                            for attr in ("pos_channel_to_bone", "ori_channel_to_bone",
                                         "scl_channel_to_bone"))
        parts.append(f"{mi.name} dtype={int(mi.dtype)} frames={mi.frame_count} "
                     f"pos={mi.pos_bone_count} ori={mi.ori_bone_count} "
                     f"scl={mi.scl_bone_count} flo={mi.float_count} maps={maps}")
    return digest(parts)


def sig_fgm(path, game):
    """Shader, texture and attribute inventory - the canary for shared XML machinery."""
    from generated.formats.fgm.structs.FgmHeader import FgmHeader
    from modules.formats.FGM import FgmContext
    ctx = FgmContext()
    ctx.version = 0
    hdr = FgmHeader.from_xml_file(path, ctx)
    def unwrap(field):
        return field.data if hasattr(field, "data") else field
    tex, att = unwrap(hdr.textures), unwrap(hdr.attributes)
    parts = [f"shader={hdr.shader_name}",
             f"textures={0 if tex is None else len(tex)}",
             f"attributes={0 if att is None else len(att)}"]
    for group, label in ((tex, "tex"), (att, "att")):
        if group is None:
            continue
        for item in group:
            parts.append(f"{label} {getattr(item, 'name', '?')}")
    return digest(parts)


SIGNERS = {"ovl": sig_ovl, "manis": sig_manis, "fgm": sig_fgm}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--update", action="store_true",
                    help="record the current signatures as the baseline")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    if not os.path.isfile(CORPUS):
        sys.exit(f"no corpus file at {CORPUS}")
    with open(CORPUS, encoding="utf-8") as fh:
        corpus = json.load(fh)

    sys.path.insert(0, REPO)
    drift, missing, failed, ok = [], [], [], 0

    for entry in corpus["entries"]:
        path, kind = entry["path"], entry["kind"]
        if not os.path.isfile(path):
            missing.append(path)
            continue
        try:
            got = SIGNERS[kind](path, entry.get("game", corpus.get("game")))
        except Exception as error:
            failed.append((path, f"{type(error).__name__}: {error}"))
            if args.verbose:
                traceback.print_exc()
            continue
        if args.update:
            entry["signature"] = got
            ok += 1
        elif entry.get("signature") != got:
            drift.append((path, entry.get("signature"), got))
        else:
            ok += 1

    if args.update:
        with open(CORPUS, "w", encoding="utf-8") as fh:
            json.dump(corpus, fh, indent=2)
        print(f"baseline recorded for {ok} files")
        if missing:
            print(f"skipped {len(missing)} missing files")
        for path, why in failed:
            print(f"  FAILED {os.path.basename(path)}: {why}")
        return 0

    print(f"matched : {ok}")
    print(f"drifted : {len(drift)}")
    print(f"missing : {len(missing)}")
    print(f"failed  : {len(failed)}")
    for path, was, now in drift:
        print(f"\n  DRIFT {path}\n     baseline {was}\n     now      {now}")
    for path, why in failed:
        print(f"\n  FAILED {os.path.basename(path)}: {why}")
    if drift or failed:
        print("\nA vanilla file now parses differently than it did.")
        print("This needs an EXTERNAL citation - a spec, a shipped asset, or the game.")
        print("Passing tests is not a citation. See FORMAT_RESEARCH_RULES.md.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
