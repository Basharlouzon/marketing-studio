#!/usr/bin/env bash
# extract_qa_frames.sh — sample frames from rendered videos for visual-judge QA.
# Usage: ./extract_qa_frames.sh <video1.mp4> [video2.mp4 ...]
# Writes qa/<basename>-t<t>.png next to each video at t = 1, 5, 10, 14
# (EXTRA_TIMES env APPENDS timestamps for >15s videos, e.g. EXTRA_TIMES="20 25 29").
set -euo pipefail
TIMES_DEFAULT="1 5 10 14"
for video in "$@"; do
  dir="$(dirname "$video")"
  base="$(basename "$video" .mp4)"
  mkdir -p "$dir/qa"
  times="$TIMES_DEFAULT${EXTRA_TIMES:+ $EXTRA_TIMES}"
  for t in $times; do
    ffmpeg -y -loglevel error -ss "$t" -i "$video" -frames:v 1 "$dir/qa/${base}-t${t}.png"
  done
  echo "qa frames: $dir/qa/${base}-t*.png"
done
