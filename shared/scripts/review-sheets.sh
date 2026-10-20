#!/usr/bin/env bash
# Images to LOOK AT before anyone watches the film: contact sheet, phone-size sheet, a frame strip around a fast moment,
# stills at chosen times, and a loop check. Open every PNG with the image viewer/Read tool and critique it.
#
# Usage:
#   review-sheets.sh film.mp4 [outdir]                       contact.png (2 fps) + phone.png (1 fps at 360 px wide)
#   review-sheets.sh film.mp4 outdir --strip 42.8            + strip-42.8.png: 12 consecutive frames from that time
#   review-sheets.sh film.mp4 outdir --stills 7,12.9,42.833  + still-<t>.png at full size (exact frames, accurate seek)
#   review-sheets.sh film.mp4 outdir --loop                  + loop_check.mp4: the film twice, to watch the seam
#   review-sheets.sh film.mp4 outdir --from 40 --to 48       limit the sheets to a window (for a re-rendered section)
set -euo pipefail
IN=${1:?usage: review-sheets.sh film.mp4 [outdir] [--strip t] [--stills t,t] [--loop] [--from s --to s]}
OUT=${2:-review-sheets}; shift $(( $# >= 2 ? 2 : 1 ))
mkdir -p "$OUT"
STRIP=""; STILLS=""; LOOP=""; FROM=""; TO=""
while [[ $# -gt 0 ]]; do case $1 in
  --strip) STRIP=$2; shift 2;; --stills) STILLS=$2; shift 2;; --loop) LOOP=1; shift;;
  --from) FROM=$2; shift 2;; --to) TO=$2; shift 2;; *) echo "unknown option $1"; exit 1;; esac; done

DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$IN")
WIN=(); [[ -n $FROM ]] && WIN+=(-ss "$FROM"); [[ -n $TO ]] && WIN+=(-to "$TO")
SPAN=$(python3 -c "print(float('${TO:-$DUR}') - float('${FROM:-0}'))")
ROWS=$(python3 -c "import math; print(max(1, math.ceil($SPAN * 2 / 8)))")
PROWS=$(python3 -c "import math; print(max(1, math.ceil($SPAN / 6)))")

# contact sheet: 2 frames per second, 8 across, each 240 px wide, labelled with the film time in seconds
ffmpeg -v error -y ${WIN[@]+"${WIN[@]}"} -i "$IN" -vf "fps=2,scale=240:-2,drawtext=text='%{pts\:flt\:${FROM:-0}} s':x=4:y=4:fontsize=18:fontcolor=white:box=1:boxcolor=black@0.7,tile=8x${ROWS}:padding=2:color=black" -frames:v 1 "$OUT/contact.png"
# phone test: how it reads 360 px wide (titles, UI labels, captions must still be legible here)
ffmpeg -v error -y ${WIN[@]+"${WIN[@]}"} -i "$IN" -vf "fps=1,scale=360:-2,tile=6x${PROWS}:padding=2:color=black" -frames:v 1 "$OUT/phone.png"
echo "wrote $OUT/contact.png and $OUT/phone.png"

if [[ -n $STRIP ]]; then
  ffmpeg -v error -y -ss "$STRIP" -i "$IN" -vf "scale=320:-2,tile=12x1:padding=2:color=black" -frames:v 1 "$OUT/strip-$STRIP.png"
  echo "wrote $OUT/strip-$STRIP.png (12 consecutive frames: look for pops, overlaps, text swapping too early)"
fi
if [[ -n $STILLS ]]; then
  IFS=, read -ra TS <<< "$STILLS"
  for t in "${TS[@]}"; do ffmpeg -v error -y -ss "$t" -i "$IN" -frames:v 1 "$OUT/still-$t.png"; done
  echo "wrote ${#TS[@]} stills in $OUT/"
fi
if [[ -n $LOOP ]]; then
  ffmpeg -v error -y -stream_loop 1 -i "$IN" -c copy "$OUT/loop_check.mp4"
  echo "wrote $OUT/loop_check.mp4"
fi
