---
scope: assets/**
---

# Asset rules — assets/**

Enforced by `/asset audit`.

## Directory structure

```
assets/
  sprites/          # 2D art
    characters/<name>/
    environment/<area>/
    ui/<screen>/
    effects/
  models/           # 3D art
    characters/<name>/
    props/<category>/
    environment/<area>/
  animations/
    <rig>/<clip>.<ext>
  audio/
    sfx/<category>/
    music/<track>.<ext>
    voice/<character>/<line>.<ext>
  data/             # data tables, configs
  fonts/
  shaders/          # asset-adjacent shaders (compiled alongside art)
```

## Naming conventions

- **Lowercase with underscores.** `hero_idle.png`, not `Hero-Idle.PNG` or `heroIdle.png`.
- **Category prefix optional but recommended when collisions likely:** `sfx_footstep_grass.wav`, `ui_button_click.wav`.
- **Variants use numeric suffix:** `hero_attack_01.png`, `hero_attack_02.png`.
- **States for UI:** `button_normal.png`, `button_hover.png`, `button_pressed.png`, `button_disabled.png`.

## File-size thresholds (default — tune per project)

| Type | Soft limit | Hard limit |
|---|---|---|
| PNG sprite (single frame) | 512 KB | 2 MB |
| Spritesheet | 4 MB | 16 MB |
| Model (.fbx/.glb) | 5 MB | 25 MB |
| Audio SFX (wav/ogg) | 500 KB | 2 MB |
| Music track | 10 MB | 30 MB |
| Single VO line | 500 KB | 2 MB |

Over soft → flag for review. Over hard → block.

## Required metadata

- Sprites used in atlases: include `.tres` / `.meta` / import config alongside.
- Audio: include sample rate and channels in filename or sidecar if non-standard (22.05k mono for SFX, 44.1k stereo for music).

## Forbidden

- **No raw `.psd`, `.ai`, `.blend` working files in `assets/`.** Those live in `assets-source/` (gitignored or LFS).
- **No filenames with spaces.** Ever.
- **No files committed that don't have a referenced use** — `/asset audit` flags orphans for the user to decide.
- **No binaries over the hard limit without a written justification** in the feature's asset spec.
