#!/usr/bin/env python3
"""Build the three E1 GO (8) organ sound packs from AKWF-format cycles.

Each pack is a folder of 600-sample, 16-bit, 44.1 kHz mono WAV cycles
(the AKWF contract), plus an SFZ instrument and a JSON manifest.

Pack identities:
  organ-drawbar  — Hammond-style 9-drawbar registrations
  organ-pipe     — flue / principal / flute / mixture ranks
  organ-combo    — transistor / Farfisa-Vox voicings

Source: additive synthesis at the AKWF cycle length, plus the closest
matching AKWF_eorgan waves copied in as from-akwf variants.
"""

from __future__ import annotations

import json
import math
import shutil
import struct
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EORGAN = ROOT / "AKWF" / "AKWF_eorgan"
OUT = ROOT / "sound-packs"

CYCLE = 600
RATE = 44100
# 44100/600 = 73.5 Hz ≈ MIDI 38 (D2 = 73.416 Hz)
PITCH_KEYCENTER = 38
MAX_AMP = 0.89


def sine_partials(amps: dict[int, float]) -> list[float]:
    """amps: harmonic number (1=fundamental) -> linear amplitude."""
    samples = []
    for n in range(CYCLE):
        phase = 2.0 * math.pi * n / CYCLE
        s = 0.0
        for h, a in amps.items():
            if a:
                s += a * math.sin(phase * h)
        samples.append(s)
    return normalize(samples)


def normalize(samples: list[float], peak: float = MAX_AMP) -> list[float]:
    m = max(abs(x) for x in samples) or 1.0
    return [peak * x / m for x in samples]


def write_wav(path: Path, samples: list[float]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    ints = [max(-32767, min(32767, int(round(x * 32767.0)))) for x in samples]
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(struct.pack(f"<{len(ints)}h", *ints))


def read_wav(path: Path) -> list[float]:
    with wave.open(str(path), "rb") as w:
        raw = w.readframes(w.getnframes())
        ints = struct.unpack(f"<{w.getnframes()}h", raw)
    return [s / 32768.0 for s in ints]


def spectrum(samples: list[float], harmonics: int = 16) -> list[float]:
    mag = []
    n = len(samples)
    for h in range(1, harmonics + 1):
        re = 0.0
        im = 0.0
        for i, x in enumerate(samples):
            ph = 2.0 * math.pi * h * i / n
            re += x * math.cos(ph)
            im += x * math.sin(ph)
        mag.append(math.hypot(re, im) / n)
    return mag


def spec_distance(a: list[float], b: list[float]) -> float:
    return sum((x - y) ** 2 for x, y in zip(a, b))


def drawbar_amps(drawbars: str) -> dict[int, float]:
    """9 Hammond drawbars 16' 5⅓' 8' 4' 2⅔' 2' 1⅗' 1⅓' 1' → harmonics."""
    if len(drawbars) != 9 or any(c not in "012345678" for c in drawbars):
        raise ValueError(f"bad drawbars: {drawbars}")
    harmonics = (1, 3, 2, 4, 6, 8, 10, 12, 16)
    amps: dict[int, float] = {}
    for h, ch in zip(harmonics, drawbars):
        level = int(ch)
        if level:
            amps[h] = amps.get(h, 0.0) + level / 8.0
    return amps


DRAWBAR_REGS = [
    ("foundation_16", "800000000", "16' foundation"),
    ("jimmy_smith", "888000000", "Jimmy Smith jazz"),
    ("classic_rock", "888800000", "Classic rock"),
    ("blues", "888880000", "Blues"),
    ("full_upper", "888888000", "Full upper (no high mixture)"),
    ("jazz_sizzle", "888000008", "Jazz with 1' sizzle"),
    ("amazing_grace", "808000000", "Amazing Grace"),
    ("church", "840000000", "Soft church"),
    ("chorus_flute", "008800000", "8'+4' flute chorus"),
    ("whistle", "000080000", "2' whistle"),
    ("full_organ", "888888888", "Full nine drawbars"),
    ("two_drawbars", "880000000", "16'+5⅓' growl"),
]


PIPE_RANKS = [
    (
        "principal_8",
        "Open diapason 8'",
        {1: 1.0, 2: 0.35, 3: 0.22, 4: 0.12, 5: 0.08, 6: 0.05, 7: 0.03},
    ),
    (
        "octave_4",
        "Principal 4'",
        {2: 1.0, 4: 0.28, 6: 0.12, 8: 0.06},
    ),
    (
        "super_octave_2",
        "Fifteenth 2'",
        {4: 1.0, 8: 0.22, 12: 0.08},
    ),
    (
        "flute_8",
        "Stopped flute 8' (even harmonics)",
        {1: 1.0, 2: 0.08, 3: 0.45, 5: 0.18, 7: 0.07},
    ),
    (
        "flute_4",
        "Flute 4'",
        {2: 1.0, 4: 0.12, 6: 0.35, 10: 0.1},
    ),
    (
        "nazard_223",
        "Nazard 2⅔'",
        {3: 1.0, 6: 0.2, 9: 0.08},
    ),
    (
        "mixture",
        "Bright mixture",
        {4: 0.35, 6: 0.55, 8: 0.8, 10: 0.65, 12: 0.5, 16: 0.35},
    ),
    (
        "bourdon_16",
        "Pedal bourdon 16'+8'",
        {1: 1.0, 2: 0.55, 3: 0.12, 4: 0.08},
    ),
    (
        "diapason_chorus",
        "8'+4'+2' principal chorus",
        {1: 1.0, 2: 0.7, 3: 0.18, 4: 0.45, 5: 0.08, 6: 0.12, 8: 0.22},
    ),
    (
        "flute_chorus",
        "8'+4' flute chorus",
        {1: 1.0, 2: 0.65, 3: 0.4, 5: 0.16, 6: 0.2, 7: 0.06},
    ),
    (
        "gedackt",
        "Soft gedackt",
        {1: 1.0, 3: 0.28, 5: 0.09},
    ),
    (
        "full_swell",
        "Full swell (flue + mixture)",
        {1: 0.9, 2: 0.55, 3: 0.35, 4: 0.4, 5: 0.18, 6: 0.3, 8: 0.35, 10: 0.2, 12: 0.15},
    ),
]


def pulse(duty: float) -> list[float]:
    samples = [1.0 if (n / CYCLE) % 1.0 < duty else -1.0 for n in range(CYCLE)]
    # mild Gibbs-free edge via 8-harmonic band-limit
    amps: dict[int, float] = {}
    for h in range(1, 17):
        amps[h] = (2.0 / (h * math.pi)) * math.sin(h * math.pi * duty)
    return sine_partials(amps)


def saw_lite() -> list[float]:
    return sine_partials({h: 1.0 / h for h in range(1, 13)})


def square_lite() -> list[float]:
    return sine_partials({h: 1.0 / h for h in range(1, 16, 2)})


COMBO_VOICES = [
    ("combo_8", "Transistor 8' (band-limited square)", square_lite),
    ("combo_4", "Transistor 4'", lambda: sine_partials({h: 1.0 / h for h in range(2, 17, 2)})),
    ("combo_16_8", "16'+8' combo", lambda: sine_partials({1: 0.85, **{h: 0.7 / h for h in range(1, 15, 2)}})),
    ("farfisa_bright", "Farfisa-like 16+8+4+2", lambda: sine_partials({1: 0.7, 2: 0.9, 3: 0.35, 4: 0.7, 5: 0.2, 6: 0.25, 8: 0.45, 10: 0.15})),
    ("vox_nasal", "Vox-like nasal", lambda: sine_partials({1: 0.4, 2: 0.55, 3: 1.0, 4: 0.35, 5: 0.7, 6: 0.25, 7: 0.4, 9: 0.2})),
    ("pulse_25", "25% pulse", lambda: pulse(0.25)),
    ("pulse_12", "12% thin pulse", lambda: pulse(0.125)),
    ("saw_combo", "Soft saw combo", saw_lite),
    ("combo_chorus", "8'+4'+2' transistor chorus", lambda: sine_partials({1: 0.8, 2: 0.85, 3: 0.25, 4: 0.6, 6: 0.2, 8: 0.4})),
    ("combo_reed", "Reedy combo", lambda: sine_partials({1: 0.6, 2: 0.3, 3: 0.85, 4: 0.2, 5: 0.55, 6: 0.15, 7: 0.35, 9: 0.18})),
    ("spinet", "Spinet (thin 8'+4')", lambda: sine_partials({1: 0.55, 2: 1.0, 3: 0.12, 4: 0.45, 8: 0.18})),
    ("combo_full", "Full combo", lambda: sine_partials({1: 0.9, 2: 0.8, 3: 0.5, 4: 0.65, 5: 0.3, 6: 0.25, 8: 0.4, 10: 0.15, 12: 0.1})),
]


def load_eorgan_library() -> list[tuple[str, list[float], list[float]]]:
    lib = []
    for path in sorted(EORGAN.glob("AKWF_eorgan_*.wav")):
        samples = read_wav(path)
        if len(samples) != CYCLE:
            continue
        lib.append((path.name, samples, spectrum(samples)))
    if not lib:
        raise SystemExit(f"No AKWF_eorgan waves in {EORGAN}")
    return lib


def closest_eorgan(samples: list[float], library, used: set[str]) -> tuple[str, list[float]]:
    target = spectrum(samples)
    ranked = sorted(library, key=lambda item: spec_distance(target, item[2]))
    for name, wav, _ in ranked:
        if name not in used:
            used.add(name)
            return name, wav
    name, wav, _ = ranked[0]
    return name, wav


def write_sfz(path: Path, waves: list[dict]) -> None:
    # C0–B0 (MIDI 12–23) keyswitch the 12 registrations; play from C1 up.
    sw_lo, sw_hi = 12, 12 + len(waves) - 1
    lines = [
        "// AKWF organ sound pack — looped single-cycle (CC0)",
        "<control>",
        "default_path=waves/",
        "",
        "<global>",
        "loop_mode=loop_continuous",
        "loop_start=0",
        f"loop_end={CYCLE - 1}",
        f"pitch_keycenter={PITCH_KEYCENTER}",
        f"sw_lokey={sw_lo}",
        f"sw_hikey={sw_hi}",
        f"sw_default={sw_lo}",
        "lokey=24",
        "hikey=127",
        "",
    ]
    for i, wave_info in enumerate(waves):
        lines += [
            "<region>",
            f"sample={wave_info['file']}",
            f"sw_last={sw_lo + i}",
            f"sw_label={wave_info['name']}",
            "",
        ]
    path.write_text("\n".join(lines), encoding="utf-8")


def write_pack(
    pack_id: str,
    title: str,
    blurb: str,
    entries: list[tuple[str, str, list[float]]],
    library,
) -> dict:
    pack_dir = OUT / pack_id
    wave_dir = pack_dir / "waves"
    if pack_dir.exists():
        shutil.rmtree(pack_dir)
    wave_dir.mkdir(parents=True)

    used: set[str] = set()
    waves = []
    for stem, label, samples in entries:
        dest = wave_dir / f"{stem}.wav"
        write_wav(dest, samples)
        src_name, _src_samples = closest_eorgan(samples, library, used)
        src_dest = wave_dir / f"{stem}__akwf_{Path(src_name).stem}.wav"
        shutil.copy2(EORGAN / src_name, src_dest)
        waves.append(
            {
                "id": stem,
                "name": label,
                "file": dest.name,
                "akwfSource": src_name,
                "akwfFile": src_dest.name,
            }
        )

    manifest = {
        "id": pack_id,
        "name": title,
        "blurb": blurb,
        "format": "akwf-cycle",
        "cycleSamples": CYCLE,
        "sampleRate": RATE,
        "bitDepth": 16,
        "channels": 1,
        "pitchKeycenter": PITCH_KEYCENTER,
        "cycleHz": RATE / CYCLE,
        "license": "CC0-1.0",
        "task": "E1 GO (8)",
        "waves": waves,
    }
    (pack_dir / f"{pack_id}.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    write_sfz(pack_dir / f"{pack_id}.sfz", waves)
    (pack_dir / "README.md").write_text(
        f"# {title}\n\n{blurb}\n\n"
        f"- Format: {CYCLE} samples, 16-bit, {RATE} Hz, mono (AKWF cycle)\n"
        f"- Pitch keycenter: MIDI {PITCH_KEYCENTER} (cycle ≈ {RATE / CYCLE:.1f} Hz)\n"
        f"- License: CC0-1.0 (same as AKWF)\n"
        f"- Instrument: `{pack_id}.sfz` (looped cycle; C0–B0 keyswitches)\n"
        f"- Manifest: `{pack_id}.json`\n\n"
        "Each registration has a synthesized cycle and the closest "
        "`AKWF_eorgan` wave (`*__akwf_*`).\n",
        encoding="utf-8",
    )
    return manifest


def verify_pack(pack_id: str, expected: int) -> None:
    pack_dir = OUT / pack_id
    wavs = list((pack_dir / "waves").glob("*.wav"))
    if len(wavs) != expected:
        raise SystemExit(f"{pack_id}: expected {expected} wavs, got {len(wavs)}")
    for path in wavs:
        with wave.open(str(path), "rb") as w:
            if (
                w.getnchannels() != 1
                or w.getsampwidth() != 2
                or w.getframerate() != RATE
                or w.getnframes() != CYCLE
            ):
                raise SystemExit(f"{path} is not an AKWF cycle")
        samples = read_wav(path)
        peak = max(abs(x) for x in samples)
        # Synthesized cycles stay under 0.89; AKWF sources may already be full-scale.
        if "__akwf_" in path.name:
            if peak < 0.05:
                raise SystemExit(f"{path} peak {peak:.3f} is silent")
        elif peak < 0.2 or peak > 0.95:
            raise SystemExit(f"{path} peak {peak:.3f} out of range")
    if not (pack_dir / f"{pack_id}.sfz").exists():
        raise SystemExit(f"{pack_id}: missing sfz")
    json.loads((pack_dir / f"{pack_id}.json").read_text())


def main() -> None:
    library = load_eorgan_library()

    drawbar_entries = [
        (stem, f"{label} ({reg})", sine_partials(drawbar_amps(reg)))
        for stem, reg, label in DRAWBAR_REGS
    ]
    pipe_entries = [
        (stem, label, sine_partials(amps)) for stem, label, amps in PIPE_RANKS
    ]
    combo_entries = [(stem, label, factory()) for stem, label, factory in COMBO_VOICES]

    packs = [
        write_pack(
            "organ-drawbar",
            "Drawbar Organ",
            "Hammond-style 9-drawbar registrations as AKWF single-cycle waves.",
            drawbar_entries,
            library,
        ),
        write_pack(
            "organ-pipe",
            "Pipe Organ",
            "Flue ranks: principal, flute, nazard, mixture, pedal bourdon.",
            pipe_entries,
            library,
        ),
        write_pack(
            "organ-combo",
            "Combo Organ",
            "Transistor combo voicings (Farfisa / Vox / spinet families).",
            combo_entries,
            library,
        ),
    ]

    index = {
        "task": "E1 GO (8)",
        "packs": [
            {
                "id": p["id"],
                "name": p["name"],
                "waves": len(p["waves"]),
                "path": f"sound-packs/{p['id']}/",
            }
            for p in packs
        ],
    }
    (OUT / "index.json").write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
    (OUT / "README.md").write_text(
        "# Organ sound packs (E1 GO (8))\n\n"
        "Three playable organ packs in the AKWF cycle format "
        "(600 samples, 16-bit, 44.1 kHz, mono).\n\n"
        "| Pack | Folder | Waves |\n"
        "| --- | --- | --- |\n"
        + "\n".join(
            f"| {p['name']} | `{p['id']}/` | {len(p['waves'])} registrations "
            f"(+ closest AKWF_eorgan) |"
            for p in packs
        )
        + "\n\n"
        "Load `*.sfz` in any SFZ sampler, or the JSON cycles in a web/PMW oscillator. "
        "License is CC0-1.0.\n",
        encoding="utf-8",
    )

    for pack_id, entries in (
        ("organ-drawbar", drawbar_entries),
        ("organ-pipe", pipe_entries),
        ("organ-combo", combo_entries),
    ):
        verify_pack(pack_id, expected=len(entries) * 2)

    print("Built", ", ".join(p["id"] for p in packs))


if __name__ == "__main__":
    main()
