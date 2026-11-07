"""Writes recipes/baihong.json: Wild Oriole's trails in black and white on every weapon, and grey blades.

usage: python tools/make_recipe.py <Bladesmith's catalog JSON>
The catalog is Bladesmith's bladesmith/data/prebuilt.json: every player weapon with its trail tags.
"""
import json
import sys
from pathlib import Path

LIGHT = "NS_LuanYing_BladeTrail_401_P1"   # light attacks and the rest
HEAVY = "NS_LuanYing_BladeTrail_401_P2"   # heavy and charged attacks
KEEP = ("Kick", "Blink")                  # kicks and the dodge keep their own look
GREY = {"to": "#8a8a8a", "all": True, "mesh": True}  # the whole weapon; "mesh" because some blades ignore the override
NO_BLADE = ("XieShan",)                   # its blade is an effect, there is no material to recolor


def trail_for(tag: str) -> str | None:
    if tag.startswith(KEEP):
        return None
    return HEAVY if {"B", "C"} & set(tag.split(".")) else LIGHT


def recipe(catalog: list[dict]) -> dict:
    weapons = []
    for w in catalog:
        entry = {"base": w["key"], "trail_color": "presets/baihong.json",
                 "trails": {t["tag"]: trail_for(t["tag"]) for t in w["trails"] if trail_for(t["tag"])}}
        if not w["key"].startswith(NO_BLADE):
            entry["blade_color"] = GREY
        weapons.append(entry)
    # small z: a mod that changes a weapon's look wins on that weapon
    return {"pak_name": "zzz_zBaihong_P", "weapons": weapons}


if __name__ == "__main__":
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    catalog = data["catalog"] if isinstance(data, dict) else data
    out = Path(__file__).resolve().parents[1] / "recipes" / "baihong.json"
    r = recipe(catalog)
    out.write_text(json.dumps(r, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(out.name, len(r["weapons"]), "weapons")
