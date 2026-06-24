---
type: guide
id: today/planet-globe
title: "Planet Globe — spinnable Mars→Earth calorie hero (worked example)"
description: "How the opt-in 3D 'Planet' calorie globe was built: a freely-spinnable SceneKit sphere whose texture cross-fades Mars→Earth by calorie fraction. Full annotated code, the decisions, the iOS-27 SceneKit shader dead-end, the asset sourcing + licensing, and how it was verified — kept as a reusable successful example."
status: stable
tags: [today, globe, scenekit, 3d, animation, assets, worked-example, ios27]
created: 2026-06-24T00:00:00Z
updated: 2026-06-24T00:00:00Z
sources:
  - "https://www.solarsystemscope.com/textures/"
  - "https://svs.gsfc.nasa.gov/13016/"
  - "https://developer.apple.com/documentation/scenekit/scnscene"
---

# Planet Globe — spinnable Mars→Earth calorie hero (worked example)

> **Intention.** A motivating, opt-in calorie hero: the planet **terraforms from a
> barren red Mars (0 cal) to a lush blue Earth (at the goal)** as the day fills, and you
> can **spin it in any direction with a finger**. Built 2026-06-24. Shipped behind a new
> globe *style* so it is fully reversible (default stays Dotted).
>
> **Asset sources (keep the links):**
> [Solar System Scope textures](https://www.solarsystemscope.com/textures/) (Mars + Earth,
> **CC BY 4.0** — attribution required) · the earlier superseded approach used
> [NASA SVS "Mars Evolution from Wet to Dry" #13016](https://svs.gsfc.nasa.gov/13016/)
> (public domain, NASA/MAVEN/Lunar and Planetary Institute).

## Why this is in the KB
It's a **successful example** of: adding a 3D element to a SwiftUI app via SceneKit;
blending two textures by a value; a free-rotation (trackball) gesture; sourcing + licensing
real planet imagery; and verifying a graphics feature **headlessly** (simulator screenshots
+ log inspection, no screen takeover). It also records a real **iOS-27 SceneKit dead-end**
so it isn't repeated.

## File map
- `Nutritionist/Views/TodayView.swift` — `PlanetGlobe` (SwiftUI wrapper) + `PlanetSphereView`
  (`UIViewRepresentable` over `SCNView`) + its `Coordinator`. `import SceneKit` at the top.
- `Nutritionist/Models/AppSettings.swift` — `TodayGlobeStyle` enum gains `case planet`
  (the Settings picker iterates `allCases`, so it appears automatically).
- `Nutritionist/Assets.xcassets/PlanetMarsTexture.imageset`, `PlanetEarthTexture.imageset`
  — 2k equirectangular maps (Solar System Scope).
- Call site: the Today hero (`todayDateHero`) switches on `appSettings.todayGlobeStyle`.

## Concept → drive signal
The hero already computes `progress = min(todayCalories / dailyGoal, 1.0)`. That same
fraction drives the morph: **0 → Mars, 1 → Earth.** Nothing new to compute.

## The code (annotated)

### 1. The globe style (opt-in, reversible)
```swift
// AppSettings.swift — adding `.planet` makes it appear in the Settings picker
// (which iterates allCases). Default stays `.dotted`, so this ships dark/off.
enum TodayGlobeStyle: String, CaseIterable, Identifiable {
    case dotted, liquid, planet
    var id: String { rawValue }
    var label: String {
        switch self {
        case .dotted: return "Dotted"
        case .liquid: return "Liquid"
        case .planet: return "Planet"
        }
    }
}
```

### 2. Call site (Today hero)
```swift
if appSettings.todayGlobeStyle == .planet {
    PlanetGlobe(size: 132, progress: progress,        // progress = calories / goal, capped
                number: totalCalories.formatted(), unit: "cal")
} else if appSettings.todayGlobeStyle == .liquid {
    LiquidGlobe(/* … */)
} else {
    DottedGlobe(/* … */)
}
```

### 3. SwiftUI wrapper — clips the 3D view to a circle
```swift
struct PlanetGlobe: View {
    var size: CGFloat = 132
    var progress: Double = 0
    var number: String = ""   // kept for call-site compatibility; unused now (no on-globe number)
    var unit: String = "cal"  // unused

    var body: some View {
        PlanetSphereView(progress: max(0, min(progress, 1)))  // clamp once here
            .frame(width: size, height: size)
            .clipShape(Circle())                              // the square SCNView → a disc
            .overlay(Circle().stroke(.white.opacity(0.14), lineWidth: 0.5))
    }
}
```
*Why a wrapper:* keeps the SceneKit details out of the hero, and the `clipShape(Circle())`
turns the square renderer into a planet "coin" that drops into the existing round globe slot.

### 4. The SceneKit view (the heart)
```swift
struct PlanetSphereView: UIViewRepresentable {
    var progress: Double
    func makeCoordinator() -> Coordinator { Coordinator() }

    // A slow idle spin around Y; paused while the finger is down, resumed on release.
    static var idleSpin: SCNAction {
        .repeatForever(.rotateBy(x: 0, y: .pi * 2, z: 0, duration: 48))
    }

    func makeUIView(context: Context) -> SCNView {
        let view = SCNView()
        view.backgroundColor = .clear      // sits on the cream Today bg
        view.isOpaque = false              // so the clear bg shows through
        view.antialiasingMode = .multisampling2X
        view.rendersContinuously = true    // needed so the idle spin animates every frame

        let scene = SCNScene()
        let c = context.coordinator
        c.mars  = UIImage(named: "PlanetMarsTexture")
        c.earth = UIImage(named: "PlanetEarthTexture")

        let sphere = SCNSphere(radius: 1.0); sphere.segmentCount = 96  // smooth limb
        let mat = SCNMaterial()
        mat.lightingModel = .lambert
        mat.diffuse.contents = c.blended(max(0, min(progress, 1)))     // CPU cross-fade (below)
        c.lastBlend = max(0, min(progress, 1))
        sphere.firstMaterial = mat
        c.material = mat

        let planet = SCNNode(geometry: sphere)
        context.coordinator.planetNode = planet
        planet.eulerAngles = SCNVector3(0.35, 0, 0)  // gentle tilt so it doesn't look flat
        planet.runAction(Self.idleSpin, forKey: "idleSpin")
        scene.rootNode.addChildNode(planet)

        let cam = SCNNode(); cam.camera = SCNCamera()
        cam.camera?.fieldOfView = 30
        cam.position = SCNVector3(0, 0, 4.2)         // pull back so the sphere fits with margin
        scene.rootNode.addChildNode(cam); view.pointOfView = cam

        let ambient = SCNNode(); ambient.light = SCNLight()
        ambient.light?.type = .ambient; ambient.light?.intensity = 600   // lifts the dark side
        scene.rootNode.addChildNode(ambient)
        let key = SCNNode(); key.light = SCNLight()
        key.light?.type = .directional; key.light?.intensity = 750
        key.position = SCNVector3(-3, 2, 4); key.look(at: SCNVector3Zero) // a soft terminator
        scene.rootNode.addChildNode(key)

        view.scene = scene
        let pan = UIPanGestureRecognizer(target: context.coordinator,
                                         action: #selector(Coordinator.handlePan(_:)))
        view.addGestureRecognizer(pan)
        return view
    }

    // SwiftUI calls this on every re-render; recompute the (cost-y) texture only when the
    // calorie fraction actually moved.
    func updateUIView(_ view: SCNView, context: Context) {
        let c = context.coordinator
        let p = max(0, min(progress, 1))
        if abs(p - c.lastBlend) > 0.01 {
            c.lastBlend = p
            c.material?.diffuse.contents = c.blended(p)
        }
    }

    final class Coordinator: NSObject {
        var planetNode: SCNNode?
        var material: SCNMaterial?
        var mars: UIImage?
        var earth: UIImage?
        var lastBlend: Double = -1
        private var last: CGPoint = .zero

        /// CPU cross-fade — draw Earth over Mars at alpha = p. p=0 → Mars, p=1 → Earth.
        /// Shader-free (see the dead-end note) and cheap because it only runs on change.
        func blended(_ p: Double) -> UIImage? {
            guard let mars else { return earth }
            guard let earth, p > 0.001 else { return mars }   // exact Mars at 0
            let size = mars.size
            return UIGraphicsImageRenderer(size: size).image { _ in
                mars.draw(in: CGRect(origin: .zero, size: size))
                earth.draw(in: CGRect(origin: .zero, size: size),
                           blendMode: .normal, alpha: CGFloat(min(p, 1)))
            }
        }

        // Free rotation: world-space (pre-multiplied) trackball, so a drag rotates around
        // the SCREEN axes no matter how the globe is already turned → "spin any direction".
        @objc func handlePan(_ g: UIPanGestureRecognizer) {
            guard let node = planetNode, let view = g.view else { return }
            switch g.state {
            case .began:
                last = .zero
                node.removeAction(forKey: "idleSpin")        // stop auto-spin while dragging
            case .changed:
                let t = g.translation(in: view)
                let dx = Float(t.x - last.x), dy = Float(t.y - last.y)  // per-frame delta
                last = t
                let f: Float = 0.008                          // radians per point
                let rot = SCNMatrix4Mult(SCNMatrix4MakeRotation(dy * f, 1, 0, 0),   // vertical → X
                                         SCNMatrix4MakeRotation(dx * f, 0, 1, 0))   // horizontal → Y
                node.transform = SCNMatrix4Mult(rot, node.transform)  // PRE-multiply = world space
            case .ended, .cancelled, .failed:
                last = .zero
                node.runAction(PlanetSphereView.idleSpin, forKey: "idleSpin")  // resume idle
            default: break
            }
        }
    }
}
```

## Decisions & lessons (the reusable part)

1. **Why SceneKit, not a flat image.** The hard requirement was "spin in any direction with
   my finger." A 2D image (even a pre-rendered rotation sequence) can't free-rotate — that
   needs a real 3D sphere. SceneKit via `UIViewRepresentable` is the lightest way to embed one.

2. **Why a CPU cross-fade, not a shader (a real iOS-27 dead-end).** The natural way to blend
   two textures is an `SCNMaterial.shaderModifiers` `[.surface:]` that `mix()`es a Mars
   diffuse with a bound Earth texture. **iOS 27 SceneKit rejected every form tried:**
   - `texture2d<float> earthTex;` in `#pragma arguments` →
     `Warning: C3DBaseTypeFromMetalString: unknown type name 'texture2d<float>'`.
   - the GLSL fallback `sampler2D earthTex; … vec4 c = texture2D(...)` →
     `unknown type name 'sampler2D'` / `unknown type name 'vec4'` + `MTLLibraryError Code=3`.
   So **custom-texture shader-modifier blending is a dead end here.** The fix: composite on
   the CPU with `UIGraphicsImageRenderer` (Earth over Mars at `alpha = fraction`) and assign
   the result to `diffuse.contents`. It's robust, has no GPU/driver surprises, and is cheap
   because `updateUIView` only recomputes when the fraction moves (the `abs(p - lastBlend) > 0.01`
   guard).

3. **Why not two spheres + transparency.** An earlier attempt put an Earth shell (radius
   1.004) over a Mars sphere and faded its `transparency`. It had **depth/ordering issues**
   (showed Mars even at full progress). Abandoned in favor of the single-sphere CPU blend.

4. **World-space vs local rotation.** Pre-multiplying the incremental rotation
   (`rot * transform`) rotates around the screen's X/Y, which feels like a trackball.
   Post-multiplying (`transform * rot`) rotates around the globe's own axes (tumbling) and
   feels disorienting. We want pre-multiply.

5. **`rendersContinuously = true`** is required or the idle `SCNAction` won't animate
   (SCNView renders on demand by default).

## How it was verified (no screen takeover)
The user needs their machine, so **no computer-use / clicking**. Verification used only:
- `xcodebuild … build` and trusting a literal `BUILD SUCCEEDED`.
- **`simctl` screenshots** (`xcrun simctl io <dev> screenshot …`) — headless, doesn't touch
  the mouse/focus. Confirmed **Mars at 0 cal** and **Earth at 108% of goal**.
- To force the Earth end without UI taps: `xcrun simctl spawn <dev> defaults write
  <bundle> dailyCalorieGoal -int 500` then logged the sample card so `progress` hit 1.0.
- **Simulator log** to diagnose the shader dead-end:
  `xcrun simctl spawn <dev> log show --last 1m | grep -iE "unknown type|shaderModifier|MTLLibraryError"`.

## Reproduce / extend
1. Download equirectangular maps from Solar System Scope (`/textures/download/2k_mars.jpg`,
   `2k_earth_daymap.jpg`), validate they're real JPEGs (`file`), drop each into a
   `*.imageset` with a one-line `Contents.json` (universal, single image) — the asset
   catalog compiles new imagesets without editing `project.pbxproj`.
2. Add the globe `case`, the call-site branch, and the `PlanetGlobe`/`PlanetSphereView`.
3. To blend more bodies or stages, extend `blended(_:)` (more `draw` layers) — still CPU,
   still shader-free.

## Open follow-up
Add a visible **NASA / Solar System Scope credit** in Settings/About (CC BY needs
attribution; NASA asks for credit + no implied endorsement). Not yet shipped.

See also [[ios26-design-guide]] and the brand-identity content-layer rule
([[brand-identity-on-ios]]) — a photoreal planet is "content layer", which is where
personality belongs.
