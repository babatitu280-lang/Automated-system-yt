#!/usr/bin/env python3
"""Generate a simple faceless vertical Short using FFmpeg + espeak-ng."""
import os, random, subprocess, textwrap
from pathlib import Path

OUT = Path("output")
OUT.mkdir(exist_ok=True)
CHANNEL_NAME = "Your Channel"
WIDTH, HEIGHT, FPS = 1080, 1920, 30
DURATION = 30

def run(cmd):
    subprocess.run(cmd, check=True)

def read_ideas():
    ideas = [x.strip() for x in Path("ideas.txt").read_text(encoding="utf-8").splitlines() if x.strip() and not x.startswith("#")]
    if not ideas:
        return ["Three small ways to make today easier"]
    state = Path(".idea_index")
    idx = int(state.read_text()) if state.exists() else 0
    idea = ideas[idx % len(ideas)]
    state.write_text(str((idx + 1) % len(ideas)))
    return [idea]

def make_script(topic):
    # Template-based copy so the workflow needs no paid API or API key.
    return (
        f"Quick idea: {topic}. "
        "First, make it small enough to start in two minutes. "
        "Next, remove one distraction before you begin. "
        "Finally, repeat the habit tomorrow instead of trying to be perfect today. "
        "Save this if you want to try it, and follow for more simple ideas."
    )

def wrap_words(text, width=26):
    return textwrap.wrap(text, width=width)

def main():
    topic = read_ideas()[0]
    script = make_script(topic)
    (OUT / "script.txt").write_text(script, encoding="utf-8")
    (OUT / "metadata.txt").write_text(
        f"Suggested title: {topic[:85]} #Shorts\n"
        "Description: A quick, original tip. Review the video and edit this metadata before publishing.\n"
        "Approval required: YES — this workflow does not upload to YouTube.\n",
        encoding="utf-8"
    )

    # Free offline TTS provided by espeak-ng on the GitHub Ubuntu runner.
    run(["espeak-ng", "-s", "155", "-v", "en-us", "-w", str(OUT / "voice.wav"), script])

    # Create timed caption file using approximate word timing.
    words = script.split()
    total = 25.0
    per = total / max(1, len(words))
    def stamp(sec):
        ms = int(sec * 1000)
        h, ms = divmod(ms, 3600000)
        m, ms = divmod(ms, 60000)
        s, ms = divmod(ms, 1000)
        return f"{h:02}:{m:02}:{s:02},{ms:03}"
    chunks = [" ".join(words[i:i+6]) for i in range(0, len(words), 6)]
    with (OUT / "captions.srt").open("w", encoding="utf-8") as f:
        for i, chunk in enumerate(chunks, 1):
            start = i * 0.0 + (i-1) * (total / len(chunks))
            end = i * (total / len(chunks))
            f.write(f"{i}\n{stamp(start)} --> {stamp(end)}\n{chunk}\n\n")

    # Make a readable vertical video from animated background + large centered text.
    # Each text card is its own image generated with FFmpeg drawtext.
    cards = [
        f"QUICK IDEA",
        topic,
        "1. START SMALL",
        "2. REMOVE ONE DISTRACTION",
        "3. REPEAT TOMORROW",
        "SAVE THIS FOR LATER"
    ]
    # Text files avoid most FFmpeg escaping issues.
    for i, card in enumerate(cards):
        (OUT / f"card_{i}.txt").write_text(card, encoding="utf-8")

    # Single 30-second video with cards changing every 5 seconds.
    filters = []
    for i in range(len(cards)):
        filters.append(
            f"drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
            f"textfile={OUT / f'card_{i}.txt'}:reload=0:fontcolor=white:fontsize=76:"
            f"line_spacing=22:x=(w-text_w)/2:y=(h-text_h)/2:"
            f"box=1:boxcolor=0x111827@0.78:boxborderw=42:"
            f"enable='between(t,{i*5},{(i+1)*5})'"
        )
    vf = ",".join(filters)
    # Background color pulses slowly; audio narration runs over it.
    run([
        "ffmpeg", "-y", "-f", "lavfi", "-i",
        f"color=c=0x111827:s={WIDTH}x{HEIGHT}:r={FPS}:d={DURATION}",
        "-i", str(OUT / "voice.wav"),
        "-vf", vf,
        "-t", str(DURATION), "-r", str(FPS),
        "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "128k", "-shortest",
        "-movflags", "+faststart", str(OUT / "draft.mp4")
    ])
    print(f"Draft created for topic: {topic}")
    print("No YouTube upload was performed. Review output/draft.mp4 before publishing.")

if __name__ == "__main__":
    main()
