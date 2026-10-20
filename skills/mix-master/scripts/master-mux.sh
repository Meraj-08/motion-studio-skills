#!/usr/bin/env bash
# Master a soundtrack and put it on a rendered picture without touching the picture (video stream is copied).
# Two-pass loudnorm to the social target, AAC 320k, plus a small review copy. Optional light sharpen, done ONCE on the
# picture master (it re-encodes), never on every mux.
#
# Usage:
#   master-mux.sh picture.mp4 soundtrack.wav out.mp4                 # −14 LUFS / −1 dBTP, + out-small.mp4
#   LUFS=-16 TP=-1.5 master-mux.sh picture.mp4 soundtrack.wav out.mp4
#   SMALL=0 master-mux.sh ...                                        # skip the small copy
#   master-mux.sh --sharpen picture.mp4 picture-sharp.mp4            # unsharp 5:5:0.5 on luma only (+60–70 % edge
#                                                                    #   contrast on UI text, no halos), CRF 14
set -euo pipefail
if [[ ${1:-} == --sharpen ]]; then
  IN=${2:?}; OUT=${3:?}
  ffmpeg -v error -y -i "$IN" -map 0:v -vf "unsharp=5:5:0.5:5:5:0.0" -c:v libx264 -preset slow -crf 14 -pix_fmt yuv420p \
    -movflags +faststart "$OUT"
  echo "wrote $OUT"; exit 0
fi
PIC=${1:?usage: master-mux.sh picture.mp4 soundtrack.wav out.mp4}; WAV=${2:?}; OUT=${3:?}
LUFS=${LUFS:--14}; TP=${TP:--1}; LRA=${LRA:-11}
# pass 1: measure
M=$(ffmpeg -hide_banner -nostats -i "$WAV" -af "loudnorm=I=$LUFS:TP=$TP:LRA=$LRA:print_format=json" -f null - 2>&1 | \
    python3 -c "import sys; s=sys.stdin.read(); print(s[s.rindex('{'):s.rindex('}')+1])")
g(){ python3 -c "import json,sys; print(json.loads(sys.argv[1])['$1'])" "$M"; }
# pass 2: linear normalisation with the measured values (keeps the mix's dynamics instead of riding them)
AF="loudnorm=I=$LUFS:TP=$TP:LRA=$LRA:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true,aresample=48000"
VDUR=$(ffprobe -v error -select_streams v:0 -show_entries format=duration -of csv=p=0 "$PIC")
ffmpeg -v error -y -i "$PIC" -i "$WAV" -map 0:v -map 1:a -c:v copy -af "$AF" -c:a aac -b:a 320k -t "$VDUR" \
  -movflags +faststart "$OUT"
R=$(ffmpeg -hide_banner -nostats -i "$OUT" -vn -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I|Peak):" | tr -s ' ' | tr '\n' ' ')
echo "wrote $OUT ·$R"
GOT=$(echo "$R" | grep -oE "I: *-?[0-9.]+" | grep -oE "\-?[0-9.]+")
python3 -c "import sys; g=float('$GOT'); t=float('$LUFS'); sys.exit(0 if abs(g-t)<=1 else 1)" || \
  echo "note: reached $GOT LUFS, not $LUFS: the true-peak ceiling ($TP dBTP) limits a spiky mix. Add a limiter or compress the mix if the target matters."
if [[ ${SMALL:-1} == 1 ]]; then
  S="${OUT%.mp4}-small.mp4"
  ffmpeg -v error -y -i "$OUT" -vf "scale=1280:-2" -c:v libx264 -preset slow -crf 26 -c:a aac -b:a 160k -movflags +faststart "$S"
  echo "wrote $S ($(du -h "$S" | cut -f1))"
fi
