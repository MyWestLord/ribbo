# RIBBO: choreography

[← back to README](../README.md)

Tempo **120 BPM**: 1 beat = 0.5 s, 1 bar = 2 s. Everything (bounces, ripples, lasers and LED moods) is driven by
`beat = t × 2` inside `renderAt(t)`, and the soundtrack in `tools/music.py` uses the same grid.

| Time | Bars | Stage | Move | Face |
|---|---|---|---|---|
| 0–2 s | 1 | Night pond, synthwave sun, fireflies | Groove bounce on every kick, head bob | `chill`, random blinks |
| 2–4 s | 2 | Bass enters | Alternating arm pumps, shoulder shimmy | `chill` |
| 4–8 s | 3–4 | 🔦 Lasers on, claps in | Alternating **hands up** with hip sway | `happy`, mouth sings |
| 8–10 s | 5 | Orbit camera, hue-cycling lights | **360° hop-spin**, both hands up | `star` |
| 10–11 s | 6a | | Double-time squats | `:3` |
| 11–12 s | 6b | Kick drops out, riser | Crouch and charge, tiny shake | `> <` charging |
| 12–14 s | 7 | 💥 **DROP**: rainbow sunburst, 3 frogs, 3 lily pads | Synced **jumps** with mid-air twists, ripples on every landing | `happy` / `star` |
| 14–16 s | 8 | | Both arms up, wave cascade between the three frogs | `♥ ♥` |
| 16–19 s | 9 | End card | Bye-bye wave, title in, fade out | `♥ ♥` |

## Tricks that sell it

- **Hit on the beat, not between.** Each beat starts with a squash (`exp(-phase·5)`), and the airborne arc fills the rest of the beat.
- **Cascade.** In the drop the three frogs are offset by 0.12 beats, so the line reads as a wave instead of a copy-paste.
- **Anticipation.** One full bar of silence-ish build (kick out, eyes `> <`, body crouched) makes the drop land twice as hard.
- **The world dances too.** Water ripples, pad rings, lasers and light colours all pulse with the same beat envelope.
