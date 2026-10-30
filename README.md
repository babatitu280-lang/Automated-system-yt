# Free Faceless Shorts Automation (Starter)

A phone-friendly, cloud-run starter for creating one vertical draft Short per day.
It does **not** publish anything automatically. GitHub Actions renders a draft MP4 and exposes it as a downloadable workflow artifact for you to review on Android.

## What this starter does
- Runs daily using GitHub Actions (UTC schedule; edit the cron to suit you).
- Chooses the next idea from `ideas.txt`.
- Builds a short, faceless, text-led video in 9:16 format.
- Creates free local narration with `espeak-ng` and renders with FFmpeg.
- Saves the MP4, script, and captions as a downloadable artifact.
- Never uploads to YouTube.

## Important limits
- This is a zero-API-cost starter, not a fully generative LLM. Script assembly is template-based so it can run without paid API keys.
- Visuals are animated text cards, not AI-generated footage. You can later replace the scene renderer with your own licensed footage or generated visuals.
- `espeak-ng` voice is robotic. A natural-sounding free voice may require a separate service, whose free tier and terms can change.
- GitHub Actions has usage limits and scheduled jobs can be delayed. Public-repository and account policies may vary.
- Review all content and rights before uploading. Do not add auto-publishing without an explicit approval gate.

## Set up from Android
1. Sign in to GitHub in your browser.
2. Create a new repository, e.g. `my-faceless-shorts`.
3. Upload all files/folders from this ZIP to the repository (GitHub mobile web supports adding files; the easiest route may be desktop mode).
4. Open **Actions** and enable workflows if GitHub asks.
5. Open **Actions → Daily draft Short → Run workflow** to test manually.
6. When it finishes, open the run and download the `short-draft-...` artifact.
7. Review the MP4 on your phone. Upload it manually in YouTube Studio only if you approve it.

## Schedule
`.github/workflows/daily-short.yml` runs daily at `14:00 UTC` (19:30 India Standard Time). To change it, edit the cron expression. GitHub scheduled workflows use UTC and can be delayed.

## Output
The artifact contains:
- `draft.mp4` — vertical video, 1080×1920
- `script.txt` — narration
- `captions.srt` — simple captions
- `metadata.txt` — suggested title and description

## Make it yours
Edit `CHANNEL_NAME` and `ideas.txt` in `generate_short.py` / repository files. Keep the video original and add your own value; repetitive low-effort template content may not be suitable for monetization.
