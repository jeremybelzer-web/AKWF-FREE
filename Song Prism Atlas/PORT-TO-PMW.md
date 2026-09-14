# Port Song Prism Atlas → jeremybelzer-web/pmw

## Why this file exists
Docs were drafted in **AKWF-FREE** (wrong repo for the app). They must live in **pmw**.

## Blocker
Cloud Agents attached only to `AKWF-FREE` cannot push to `pmw` (`Permission denied to cursor[bot]` / HTTP 403).

## Finish the port (pmw-attached agent)

```bash
git checkout -b cursor/song-prism-atlas-port-b25c
git fetch https://github.com/jeremybelzer-web/AKWF-FREE.git cursor/curiositor-roadmap-handoff-da10
git checkout FETCH_HEAD -- "Song Prism Atlas"
git add "Song Prism Atlas"
git commit -m "docs(curiositor): port Song Prism Atlas handoff + roadmaps from AKWF-FREE"
git push -u origin cursor/song-prism-atlas-port-b25c
```

Then open a draft PR into `main`.

## Files
- `HANDOFF-CLAUDE-FABLE.md`
- `roadmap/CORE-CURIOSITY-ENGINE-ROADMAP.md`
- `roadmap/MANUALS-PATTERN-INDEX.md`
- `PORT-TO-PMW.md` (this file — can delete after port)
