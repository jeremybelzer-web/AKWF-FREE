# Core Curiosity Engine — App Building Roadmap

> **This is the APP BUILDING roadmap** (product heart, UX, web week + Max for Live pivot, build order).  
> It is **NOT** the manuals roadmap. Manuals are reference input only — see [`MANUALS-PATTERN-INDEX.md`](./MANUALS-PATTERN-INDEX.md).

**Repo note:** These planning docs were drafted in the `AKWF-FREE` agent workspace. The live web app historically lives under Jeremy’s Curiositor / CrossPollinate / `pmw` project. Claude Fable should port or continue these files in the correct app repo if that is not this one.

---

## 1. Vision (heart-first)

Curiositor is **not** “another full DAW clone.”

The product heart is:

1. **Inspiration → curiosities → automation** — pull *building-block* behaviors from an inspiration song (or whole song), optionally remap key/BPM, and redraw selected curiosity automation into the user’s song.
2. **Song Sketch 2–class form editing** — edit *any* curiosity at any zoom granularity across 1..N tracks (not just arrangement copy).
3. **Node leadership** — a selected node / line (2 nodes) / group leads follower curiosity lanes.
4. **Stacked Session matrices** — Ableton-like clip grid reinterpreted as a swipeable stack: Cover (all curiosities summed) + one matrix per split curiosity.
5. **Arrangement ↔ Inspiration swipe** (web/bigger host) — user’s multi-track in front; inspiration song behind/left; Record draws selected curiosity automation into the user song.

Everything else (transport, tracks, clips/shelf, magnify/device lane, minimal synth/sampler/FX) exists only to host that heart.

---

## 2. Document split (do not merge)

| Document | Purpose | Path |
|----------|---------|------|
| **App building roadmap** | What we build | `Song Prism Atlas/roadmap/CORE-CURIOSITY-ENGINE-ROADMAP.md` |
| **Manuals pattern index** | Patterns adapted/rejected from Ableton/FL/etc. manuals | `Song Prism Atlas/roadmap/MANUALS-PATTERN-INDEX.md` |
| **Handoff** | Status + next agent instructions | `Song Prism Atlas/HANDOFF-CLAUDE-FABLE.md` |

Manuals under `manuals/` (when populated) are **reference only**. Never copy copyrighted manual prose into these docs—summarize adapted patterns in our own words.

---

## 3. One-week web push + day-7 pivot gate

**Clock starts:** from Jeremy’s decision date (week of this handoff).

### Week-now track (bigger / web host)
Spend **exactly one more week** trying to demo the heart in the web host (slim multi-track + curiosity core—not full DAW parity).

### Day-7 pivot gate (Jeremy’s call)
If progress is insufficient for Jeremy’s taste → **from that point onward: all-in on Ableton Live Max for Live only**, same product heart, stripped UI.

**Suggested testable gate criteria (edit with Jeremy):**

- [ ] Inspiration song can be loaded (clip or longer region / whole song path stubbed)
- [ ] Key/BPM import popup A/B works
- [ ] At least **one** curiosity type generates/redraws automation into the user song on Record (e.g. rate of chord change or modulations)
- [ ] At least **one** Sketch-style form editor surface OR stacked matrix swipe prototype is visible
- [ ] Node or lane selection can mark a leader → at least one follower lane reacts (even if crude)
- [ ] Project save/load survives a refresh for the demo set

If fewer than Jeremy’s minimum bar (he decides) → pivot to M4L.

---

## 4. Dual-track plan (same heart)

### Track W — Web MVP host (this week)
Smallest host that can demo:

- Multi-track grid + transport
- Essence Shelf / idea parking (existing concept)
- Magnify / per-track detail + automation lanes
- Inspiration import + A/B key-BPM popup
- Curiosity selection → Record redraw
- Stacked matrix swipe **or** Sketch form surface (whichever ships first as vertical slice)

**Freeze:** full scenes parity, full arrangement “print,” 3rd-party plugins, Wanderer/Orbits-scale theory UIs, dual-skin chrome debt.

### Track M — Max for Live (always designed in parallel; exclusive after failed gate)
Stripped plug-in product:

- Expanded **Chord Changes–class** engine (whole-song optional; multi-key; not 2-bar-only; not one-key-only)
- **Song Sketch 2–class** form editor for curiosities (not arrangement-only; any curiosity; 1..N tracks as Live API allows)
- **Curiosity automation lanes** + node/line/group leadership
- Stacked curiosity matrices **as far as M4L windows allow**
- Same import key/BPM A/B behavior

Shared schema (portable): curiosity taxonomy, lane IDs, node graph, inspiration→user transform params, templates/snapshots—so pivot is not a full rewrite.

---

## 5. Curiosity taxonomy v0

### Form curiosities
1. Song form (sections)
2. Melodic form
3. Melody rise-and-fall line form
4. Rhythm form
5. Melody phrasing form (starts/stops in section(s); silences between notes; silences between phrases/sections)
6. Rate-of-chord-change rhythm form
7. Chord-strike form (e.g. 3,3,3,4…)
8. Syncopation: chord strikes ↔ rate of chord change
9. Syncopation: chord strikes ↔ rate of chord change ↔ percussion
10. Form of when that syncopation set changes to the next set
11. *(extensible slots)*

### Suites
- **Curiosity suite** = set of curiosities **and/or** curiosities *about relationships between* curiosities.

### User-defined
- Users can add curiosities and suites.

### Legal product posture (summary for builders)
- Prefer user-owned / licensed / PD inspiration sources for ingest.
- Prefer ephemeral extract → transform → combine → keep **new** artifact; avoid public vaults of named hit phrase kits.
- Teach idea vs expression; don’t market “download this chart hook.”
- Details: see conversation handoff; get counsel before shipping mining features.

---

## 6. Core UX specs

### 6.1 Stacked Session curiosity matrices + swipe
- **Cover (front):** all curiosities summed (= whole clip/track as in Live).
- **Behind:** one Session-style matrix per curiosity (Rhythm of Melody, Rise/Fall, Chord Strike Form, Rate of Chord Change, Melodic Form, …).
- Swipe **right** on top name bar → matrix behind.
- Swipe **left** → previous; on Cover swipe left → wrap (back becomes front).

### 6.2 Arrangement ↔ Inspiration swipe (web)
- Center: user multi-track.
- Swipe right → Inspiration song behind/left (editable).
- Record: selected curiosity automation lanes generate/redraw user song from inspiration.

### 6.3 Import key / BPM popup
- **A (default):** set inspiration key+BPM → match user song.
- **B:** set user song key+BPM → match inspiration.

### 6.4 Node / line / group leadership
- Select node | line (2 nodes) | group in a curiosity lane → **leader**.
- Leader triggers automation in one or more **follower** curiosity lanes across tracks.

### 6.5 Song Sketch–style multi-granularity form editor
- Edit any curiosity at any zoom across 1..N tracks.
- Exceeds arrangement template copy.

### 6.6 Chord Changes–class engine (exceed)
| Chord Changes-like | We exceed |
|--------------------|-----------|
| Short loop source | Optional **whole song** |
| Often one-key workflow | **Multi-key**; remap via A/B popup |
| Chord progression exploration | + full curiosity taxonomy + automation redraw |
| — | Node leadership across lanes |

---

## 7. Keep vs exceed — reference products

| Surface | Keep (pattern) | Exceed |
|---------|----------------|--------|
| Chord Changes | Live clip sync, progression graph feel, real-time audition | Whole song; multi-key; curiosity types beyond chords; automation lanes |
| Song Sketch 2 | Template/form sketch UX, section thinking | Any curiosity; any granularity; multi-track; not arrangement-only |
| Ableton Session | Clip matrix launching | Stacked curiosity matrices + swipe |
| Ableton Arrangement | Multi-track timeline | Dual stack with Inspiration behind + curiosity Record |

---

## 8. M4L scope on pivot

**In:**
- Chord Changes–class + Sketch-style curiosity form editor + curiosity automation lanes
- Whole-song optional inspiration; multi-key; A/B key-BPM
- Node/line/group leadership
- Matrices/windows as feasible in M4L

**Out (unless trivial):**
- Full web DAW chrome parity
- 3rd-party plugin hosting
- Massive theory-corpus UIs

---

## 9. Build order (demoable vertical slices)

1. Host skeleton: tracks + transport + save/load  
2. Automation lane + Record stub on one track  
3. Inspiration import + A/B key-BPM popup  
4. One curiosity (e.g. rate of chord change **or** modulations) inspiration → redraw  
5. Node or lane leader → one follower  
6. Stacked matrix swipe **or** Sketch form surface  
7. Second curiosity type + suite relationship stub  
8. M4L shell wrapping same schema (parallel)

---

## 10. Ruthless out-of-scope (until heart demos)

- Full Ableton/FL feature parity  
- VST/third-party plugins  
- Dual-skin / “everything in its own window” chrome debt  
- Wanderer Decision Trees / Orbits-scale planetary UIs  
- Backend stem split as launch blocker  
- Unlicensed public “hit curiosity vault”

---

## 11. Open questions for Jeremy

1. Exact day-7 gate minimum (which checkboxes are must-pass)?  
2. First curiosity to ship: modulations, rate-of-chord-change, or chord-strike form?  
3. Web host = slim `pmw` cut, or greenfield M4L-first schema with tiny web shell?  
4. Essence Shelf = cover matrix parking lot, or separate?  
5. Inspiration ingest: MIDI-only for v0, or audio→MIDI path?

---

## 12. Links

- Manuals pattern index: [`MANUALS-PATTERN-INDEX.md`](./MANUALS-PATTERN-INDEX.md)  
- Handoff: [`../HANDOFF-CLAUDE-FABLE.md`](../HANDOFF-CLAUDE-FABLE.md)  
- Home folder: `Song Prism Atlas/`
