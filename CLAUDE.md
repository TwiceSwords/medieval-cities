# Medieval Cities: notes for Claude Code

The owner is TwiceSwords. Ask before touching files outside this repo. Never touch Windows updates on the owner's PC.
Always list the changes or decisions you made on your own initiative, beyond what was asked.

## Layout
- `index.html`: the **live game (v1.5)**, 2D canvas renderer. Leave it alone unless asked; it is the safe backup.
- `next/`: the **3D preview (v2.0-preview)**, the same game plus a Three.js renderer. All new work goes here.
  - `next/index.html`: the whole game in one file (rules, AI, online play, UI, renderer).
  - `next/lib/`: Three.js r180 (`three.module.js` + `three.core.js`), `GLTFLoader.js`, `SkeletonUtils.js`, `BufferGeometryUtils.js`.
    These are loaded locally through an import map; there is no build step.
  - `next/models/`: put AI-generated `.glb` unit models here (Meshy, Tripo, Rodin, Hunyuan3D…).
- `next/` saves to its own localStorage key (`medieval-cities-3d-save-v1`), so it never overwrites live-game saves.
- Pages deploys straight from `main` (no workflow); `next/` is served at https://twiceswords.github.io/medieval-cities/next/

## How the 3D renderer works (search `3D RENDERER` in next/index.html)
- **Three stacked layers:**
  - bottom canvas `#c`: the painted 2D ground, grid, fog, zones, range tints; it receives all mouse events;
  - WebGL `#gl`: units, cities and wall pieces as real 3D meshes with shadows;
  - top canvas `#c2`: labels, health bars, floating numbers, projectiles and the night tint.
- **The camera matches the old 2D view:** an orthographic camera tilted by `asin(SQ)`, with bounds computed from `z`, `off`, `OX`, `OY` each frame.
  - So `center()`, `hexPath()`, `pick()` and every 2D overlay still line up exactly with the 3D objects.
  - World mapping: `X = boardX`, `Z = boardY / SQ`, `Y = liftPx / CE`; 1 world unit = 1 board pixel; meshes are scaled by `K`.
- **Drawing:** `drawMesh()` is still the single drawing call. When `R3.on` is set it forwards to `R3.submit()` instead of painting.
  - `drawUnits()` sets `R3.tag = {key, u, gy}` before each call, so objects are pooled per unit, city or piece.
  - `groundY(u)` gives the unlifted ground position, used for depth.
- **Procedural models:** the old low-poly meshes are converted to BufferGeometry (`r3Geometry`) and re-posed every frame by `meshPose()`.
  - `meshPose()` holds the same walk, attack, death, stun and breathing code the 2D renderer uses.
- **Ground:** an invisible hex-top mesh (`r3Ground`, ShadowMaterial) catches shadows and hides units standing behind hills.
- **Renderer toggle:** the `🧊 Renderer` button switches 3D and 2D and is remembered. `?r=2d` forces 2D. If WebGL fails, the game falls back to 2D automatically.

## Adding AI-generated models
1. Save the model as `next/models/<type>.glb`. Types are the `UNIT_TYPES` keys: swordsman, spearman, archer, horseman, knight, mage, skeleton, mammoth…
2. Add it to `MODEL_FILES` near the top of the 3D renderer block, e.g. `swordsman: 'models/swordsman.glb'`.
3. Models are auto-scaled to the old model's height and placed on the ground.
   - Use `MODEL_YAW[type]` if a model faces the wrong way.
4. **Animations:** clips named like `idle`, `walk` or `run`, `attack` and `death` or `die` play automatically (case-insensitive).
   - Without clips, the code bobs, leans and topples the model.
5. **Team colour:** any material whose name contains `team` gets the faction colour. A team ring is always drawn at the feet.
- Tested with three.js's sample `Soldier.glb` (Idle/Walk/Run clips): it scaled, cast shadows and animated correctly.
  That sample is not shipped.

## Testing
- Serve the folder (`python3 -m http.server`) and open `index.html`.
- Headless tests used Playwright plus a `test.html` copy that exposes `window.__T = { ev: s => eval(s), … }`.
- **Software rendering:** with SwiftShader WebGL the game runs at about 6 fps and animations take longer in real time. Real GPUs are fine.

## Ideas not done yet
- A rotatable or tiltable camera: now possible in 3D, but pick() and the 2D overlays would have to move onto raycasts and the 3D ground.
- True 3D terrain (trees, rocks, water mesh) to replace the painted ground.
- GLB models for cities and wall pieces (same pooling; keys `city:*`, `piece:*`).
