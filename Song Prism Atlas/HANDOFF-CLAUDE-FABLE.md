# Handoff — Claude Fable

**From:** Composer cloud agent (this run)  
**To:** Claude Fable  
**Date:** 2026-09-13  
**Run:** https://cursor.com/agents/bc-01a07da3-940d-797a-bfba-31f76562da10  
**Branch:** `cursor/curiositor-roadmap-handoff-da10`  
**Repo this agent is attached to:** `github.com/jeremybelzer-web/AKWF-FREE` (Adventure Kid waveforms library — **not** the Curiositor web app)

---

## Status: in-flight work finished for *this* request

Jeremy asked to:
1. Create roadmap docs with a **clear split** (app building vs manuals patterns)
2. Write a handoff for Claude Fable
3. Commit / push

**Done in this PR/branch:**
- [`Song Prism Atlas/roadmap/CORE-CURIOSITY-ENGINE-ROADMAP.md`](./roadmap/CORE-CURIOSITY-ENGINE-ROADMAP.md) — **app building** north star
- [`Song Prism Atlas/roadmap/MANUALS-PATTERN-INDEX.md`](./roadmap/MANUALS-PATTERN-INDEX.md) — manuals **pattern index only**
- [`Song Prism Atlas/HANDOFF-CLAUDE-FABLE.md`](./HANDOFF-CLAUDE-FABLE.md) — this file
- [`manuals/README.md`](../manuals/README.md) — pointer so manuals/ is not mistaken for the product plan

**Location:** all Curiositor planning docs live under **`Song Prism Atlas/`** (not `docs/curiositor/`).

**Not done (out of scope for this handoff slice):**
- No Curiositor / `pmw` application code changes (that app is **not** in this workspace)
- No Ableton/FL manuals scraped or copied (copyright)
- No Max for Live device implementation yet
- No web DAW slim-down implementation yet

---

## Critical context Claude Fable must not lose

### A) Two different roadmaps — never merge
| File | Meaning |
|------|---------|
| `CORE-CURIOSITY-ENGINE-ROADMAP.md` | **What we build** |
| `MANUALS-PATTERN-INDEX.md` | **Patterns mined from manuals** (input only) |

### B) Product heart (priority order)
1. Curiosity engines + inspiration → automation redraw  
2. Song Sketch 2–class form editing for **any** curiosity / granularity / 1..N tracks  
3. Node / line / group **leader → follower** automation lanes  
4. Stacked Session **curiosity matrices** + swipe on name bar  
5. Web: Arrangement ↔ Inspiration swipe; Record draws selected curiosity automation  
6. Import popup: **A** inspiration→user key/BPM (default) / **B** user→inspiration  

Exceed Chord Changes: whole-song optional; multi-key; not 2-bar-only.  
Exceed Song Sketch 2: not arrangement-only; any curiosity.

### C) Go-to-market timebox
- **One more week** on bigger/web heart demo.
- If Jeremy unhappy with progress → **all-in Max for Live** from then on (same heart, stripped).
- Design M4L schema **in parallel** so pivot ≠ rewrite.

### D) Legal / product posture (from long thread)
- Specific inspiration is creatively right; unlicensed “hit curiosity vault” is shaky.
- Prefer user-owned / licensed / PD ingest; transform + combine; keep new artifacts.
- No mythic “30-second rule”; Hooktheory ≠ free MIDI dump license; multitrack shops = licensing.
- Studying Ableton/FL **organization** + screenshots with differentiation notes for design = OK; don’t clone trademarks/UI expression or republish manuals.

### E) Earlier platform advice (still relevant)
- Max users / free / gamified education / composer avatars → web modules + **thin multi-track host**, not full DAW first.
- Fast producer revenue → M4L engines.
- Current Jeremy plan: one week web heart attempt, then possible M4L-only pivot.

---

## What Claude Fable should do next

1. **Confirm correct repo** for Curiositor/`pmw`. If work should live there, **copy the `Song Prism Atlas/` folder** (keep the app vs manuals split) and continue there. Do not invent AKWF waveform features for this product.
2. Open `CORE-CURIOSITY-ENGINE-ROADMAP.md` and lock Jeremy’s **day-7 gate checkboxes**.
3. Pick **first vertical slice** (recommend: inspiration import + A/B key-BPM + one curiosity redraw on Record).
4. Implement in the real app repo **or** scaffold M4L device skeleton sharing the same curiosity schema.
5. When mining Ableton/FL UI: update **only** `MANUALS-PATTERN-INDEX.md` (own words); never dump manual text into the app roadmap.
6. Do not resume “full DAW feature completion” or Wanderer/Orbits chrome until the heart demos.

---

## Suggested first commit message style for follow-on work
`feat(curiositor): <slice> — inspiration→curiosity automation`

---

## Owner
Jeremy Belzer (`jeremybelzer@gmail.com`) — product decisions, day-7 pivot call, taste bar.


---

## Port status (updated 2026-09-14)

| Place | Status |
|-------|--------|
| `jeremybelzer-web/AKWF-FREE` PR #2 / branch `cursor/curiositor-roadmap-handoff-da10` | **Source of truth today** — docs live under `Song Prism Atlas/` |
| `jeremybelzer-web/pmw` GitHub | **Not yet** — Cloud Agents attached only to AKWF-FREE get **403** on push to `pmw` |
| Local port attempt | Commit prepared; push blocked for `cursor[bot]` without `pmw` repo attachment |

### What Claude / next agent must do

Open a **Cloud Agent on `jeremybelzer-web/pmw`** (not AKWF-FREE) and run:

1. Branch: `cursor/song-prism-atlas-port-b25c` from `main`
2. Copy these three files from AKWF-FREE branch `cursor/curiositor-roadmap-handoff-da10`:
   - `Song Prism Atlas/HANDOFF-CLAUDE-FABLE.md`
   - `Song Prism Atlas/roadmap/CORE-CURIOSITY-ENGINE-ROADMAP.md`
   - `Song Prism Atlas/roadmap/MANUALS-PATTERN-INDEX.md`
3. Optional: add a short `manuals/README.md` pointer like AKWF-FREE if that folder exists / is useful
4. Commit + push + open draft PR into `pmw` `main`
5. Then continue product work from `CORE-CURIOSITY-ENGINE-ROADMAP.md` in **pmw**

### Fetch one-liner (from a pmw checkout)

```bash
git fetch https://github.com/jeremybelzer-web/AKWF-FREE.git cursor/curiositor-roadmap-handoff-da10
git checkout FETCH_HEAD -- "Song Prism Atlas"
```

Artifacts also available from the port agent run:
- `Song-Prism-Atlas-port.zip`
- `song-prism-atlas-pmw.patch`
- Google Drive folder **Song Prism Atlas (port to pmw)**
