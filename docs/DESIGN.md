# RIBBO: design notes

[← back to README](../README.md)

## Silhouette

RIBBO sits like a real frog: a wide, low body pitched ~17° nose-up, knees folded out to the sides and two straight
front arms planted in front. Everything is built from glossy, toy-like volumes with **white joint caps** at every pivot,
the visual language of the crab-bot family it belongs to.

| Part | Build | Notes |
|---|---|---|
| Shell | Ellipsoid 1.2 × 0.8 × 1.32 | Glossy red, clear-coat highlight, black chassis band |
| Belly | Ellipsoid, white | Reads as "frog belly" from the front |
| Eye domes | 2 × sphere + white bezel + black lens | Each lens hosts a 5 × 5 LED matrix |
| Mouth | Black visor strip | 11 × 3 LED matrix |
| Cheeks | Soft pink LEDs | Always on, very important |
| Hind legs | Hip → knee → ankle (2-bone IK) + long foot | 3 toes with black rubber tips |
| Front arms | Shoulder → elbow → wrist (2-bone IK) + palm | 3 fingers with rubber tips |
| Back | White vent plate | |

## Palette

| Token | Hex | Used for |
|---|---|---|
| Shell red | `#E32730` | Body, eye domes, limb segments |
| Joint white | `#E9E9EE` | Joint caps, belly, bezels |
| Chassis | `#1A1A1E` | Band, rubber toe tips |
| Lens black | `#050506` | Eye lenses, mouth visor |
| LED mint | `#3CFFB4` | Eyes and mouth |
| Cheek pink | `#FF6B9A` | Cheek LEDs |
| Pad neon | `#4DFF8A` | Lily-pad dance floor (hue-cycles in the drop) |

## LED expression sheet

Eyes (5 × 5 per lens):

| Mood | Pattern | When |
|---|---|---|
| `chill` | rounded block | Intro groove |
| `blink` | single line | Random blinks |
| `happy` | `^ ^` | Hands-up section, drop |
| `star` | `+ +` | Spinning, every 4th jump |
| `charging` | `> <` | Build-up before the drop |
| `in love` | `♥ ♥` | Wave section, outro |

Mouth (11 × 3): `smile`, `open` (singing), `grin`, `w` (`:3`), `flat`.

## Rig

- **Ground frame `G`**: position, jump height, yaw.
- **Body frame `B`** = `G · T(0, h, 0) · Rz(roll) · Rx(−pitch) · S(squash)`. Squash-and-stretch keeps the volume roughly constant.
- **Legs**: analytic 2-bone IK from the hip in `B` to an ankle target in `G`, with a pole vector that pushes the knees
  out and up (that's what makes the frog read as a frog). Mid-jump the ankle targets slide down and back, so the legs
  extend.
- **Arms**: the same IK, blending between a planted hand target in `G` and a raised, waving target in `B`.

## Proposed physical build (concept)

The video is a simulation. This is how a tabletop RIBBO could be built:

| | |
|---|---|
| DOF | 10: 3 per hind leg (hip yaw, hip pitch, knee) + 2 per arm |
| Actuators | 9 g micro servos (SG90 / MG90S class) |
| Brain | ESP32-S3 (Wi-Fi + I2S microphone for beat tracking) |
| Face | 2 × 8 × 8 LED matrices behind a smoked acrylic lens + LED strip mouth |
| Power | 1S LiPo + 5 V boost, ~20 min of non-stop dancing |
| Shell | 3D-printed PETG, sanded and clear-coated |
