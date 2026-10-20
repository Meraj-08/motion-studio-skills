# Measuring a reference

Without a reference, generated motion falls back to the same default: centered text, gradient, everything fading in.
Naming a style beats describing one, and a measured reference beats both.

## Give the reference one job

Pick it for one thing: a card entrance with a controlled landing, a transition that keeps the product in view, a cursor
action that makes the result obvious, the pacing of a launch film, a palette. Take the grammar, never the content,
logos or characters.

Kinds of reference:
- **A frame**: say what to take (palette, type, grain) and what not (subject).
- **A video**: extract frames and measure it (below).
- **A library** of your own images or past films: write `docs/STYLE.md` from it first. It's a look nobody else has.
- **The product's own website**: for brand colours, backgrounds and small details (match the stage to the site's hero and any
  added UI to the app's own pixels).

## Measure a reference video

```bash
ffprobe -v error -show_entries stream=width,height,r_frame_rate,duration -of json reference.mp4
mkdir -p frames && ffmpeg -i reference.mp4 -vf "fps=2,scale=960:-2" frames/ref-%04d.jpg      # overview
ffmpeg -ss 3.2 -i reference.mp4 -frames:v 24 frames/entrance-%02d.png                         # consecutive frames
python scripts/picture-events.py reference.mp4                                                # its cut rhythm
python scripts/beatgrid.py reference.mp4                                                      # its music grid
```

Then write `docs/REFERENCE.md`:

```text
Source: 1920×1080, 30 fps, 22.4 s.
Entrance  frames 96–111 (3.20–3.70 s): card from y+60, opacity 0→1, scale 0.96→1.0, ~2 % overshoot.   [measured]
Landing   frame 111; bounding box x310 y260 w1300 h560 (source px).                                    [measured]
Order     product → headline (+0.10 s) → supporting label (+0.25 s).                                    [measured]
Hold      readable from 3.85 s to 6.10 s (2.25 s) before the next event pulls attention.                [measured]
Cuts      on the music's downbeats; hits on the 2 and 4 of each bar.                                    [estimated: check frames 180–200]
Proposal  our export shot uses the same entrance and hold with our report screen.                      [creative choice]
```

Label measured values, visual estimates and creative choices separately; for an uncertain value, name the frames that
would settle it. Spatial estimates from images are approximate, so check positions against the extracted frames.

## Prompt (paste with the reference in the project)

```text
Analyze the main product reveal in reference.mp4. Report dimensions, frame rate and duration. Extract overview images,
then consecutive frames around the entrance and landing, and inspect them. Save docs/REFERENCE.md with timestamps and
frame numbers for entrance, landing, hold and cut; bounding boxes at start and landing; direction, duration, scale,
opacity and overshoot; the order product/headline/labels appear; the readable hold and the state carried into the next
shot. Label measured values, estimates and creative choices separately. Then propose ONE original shot using our
assets: layout, focal point, entrance, product response, reading hold. List missing assets and open questions.
Return the plan before implementing.
```

## When choosing between looks

Show the options side by side as stills, all of the same frame, so only the variable changes (for a stage choice:
generated backgrounds, then wallpaper styles, then photos and painted skies, same window and frame each time).
Then 6–7 s motion samples of the affected moments. Only then a full render.
