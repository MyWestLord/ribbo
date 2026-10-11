#!/usr/bin/env bash
# One-shot pipeline: soundtrack -> frames -> mp4
set -euo pipefail
cd "$(dirname "$0")/.."

FRAMES=build/frames
mkdir -p "$FRAMES" media

echo "🎶  synthesising soundtrack"
python3 tools/music.py

echo "🎬  rendering 570 frames (two workers)"
python3 tools/render.py "$FRAMES" 0 285 &
python3 tools/render.py "$FRAMES" 285 570 &
wait

echo "📼  muxing video"
ffmpeg -y -v error -framerate 30 -i "$FRAMES/f%04d.jpg" -i music.wav \
  -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest \
  -movflags +faststart media/ribbo-dance.mp4

echo "🐸  done → media/ribbo-dance.mp4"
