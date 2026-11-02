# NPC reference sprite integration plan

**Goal:** replace the four provisional NPC SVGs in the active V4 renderer with raster sprites matching the owner's four-car reference.
**Architecture:** preserve Phaser, Cascavel, simulation and six-car results. Prepare one shared-scale atlas per team, anchor the rear axle at the same ground point as the official cars, and choose frames from the simulated steering/brake state. Keep the old SVG files as retired history, never preload them in the updated runtime.

The owner explicitly requested these car designs and production sprites. Public code/assets publication remains authorized for this repository and the isolated /teste-v4/ preview. Canonical drivers/logos and previous pages remain untouched.

- [x] Prepare four six-frame atlases: rear, left, right, rear brake, left brake, right brake. Preserve the supplied body, colors, unmarked panels and tow hook side.
- [x] Add failing tests for six view states, steering hysteresis, active raster preload and actual brake state; implement the small visual selector and simulator flag.
- [x] Integrate atlas texture/frame selection with physical scale and rear-axle pivot; inspect screenshots and curves/braking in real Phaser.
- [x] Audit alpha/dimensions/frame hashes, document generated derivation and source access limits, record public-repository research and run all suites.
- [ ] Commit source, copy only the V4 folder, verify old Pages files, publish with guarded refs, run the public browser workflow and inspect its evidence.

The chat attachment is visually available but has no local file ID/path. image_gen edits the supplied reference directly; its result is a visual derivation, not a byte-for-byte extraction of that attachment. The raw generated sheet and every transformation will be versioned and verified.
