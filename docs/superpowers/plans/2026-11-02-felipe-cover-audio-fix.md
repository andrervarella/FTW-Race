# Felipe cover posture and audio activation plan

**Goal:** improve only Felipe's opening-cover posture while retaining his approved identity, and fix missing music/effects from the first allowed user activation onward.

**Architecture:** retain the approved cover composition, logos, selection portraits and all podium/car sprites. Add a dedicated front-posture Felipe cover image after visual approval. Keep the original Web Audio synthesizer and correct audio activation/control lifecycle based on a live reproduction, preserving explicit effects/mute modes.

**Scope/authorization:** current user explicitly requested both fixes; prior public code/assets authorization and isolated teste-v4 publication remain in effect. New portrait proposal was shown separately and in the cover; the owner answered “Aprovar a pose” before integration. First-gesture browser audio policy remains in force.

- [x] Reproduce initial sound-button silence with live samples; add meaningful RED regression, correct first activation/mode handling and verify GREEN, touch/keyboard/blur/fullscreen/mute.
- [x] Obtain visual approval for the new front-posture cover-only Felipe, preserve source, encode proportionally and update title layer/provenance without changing his other sprites.
- [x] Run all suites, live audio signal checks and real browser flows locally and in the packaged copy; verify previous Pages files unchanged.
- [x] Commit source, publish only teste-v4 under guarded refs and inspect independent public browser/audio artifacts before delivering the link.

Public verification: run41507715470 success; Pages41507467319 success; artifact13171512175 downloaded, hash/CRC checked and reports/screenshots inspected. See FELIPE_AUDIO_FIX_QA.md.
