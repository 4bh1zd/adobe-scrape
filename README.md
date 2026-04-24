# Adobe Podcast Enhancer

Automates [Adobe Podcast Enhance](https://podcast.adobe.com/en/enhance) to upload an audio file, process it with Adobe's AI enhancement, and download the result — no manual interaction required after the first login.

## Requirements

- Python 3.10+
- Google Chrome installed
- An Adobe account

## Setup

**1. Create and activate a virtual environment**

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
playwright install chromium
```

**3. (Optional) Configure via environment variables**

Copy `.env.example` to `.env` and adjust as needed:

```bash
cp .env.example .env
```

| Variable | Default | Description |
|----------|---------|-------------|
| `ADOBE_URL` | `https://podcast.adobe.com/en/enhance#` | Target Adobe Podcast URL |
| `CHROME_PROFILE_DIR` | `chrome_profile` | Directory for the persistent browser session |
| `INPUT_DIR` | `input` | Directory to read audio files from |
| `OUTPUT_DIR` | `output` | Directory to save enhanced files to |

## Usage

### Login (first time only)

Opens a Chrome window for you to log in to Adobe manually. The session is saved to `chrome_profile/` and reused on all future runs.

```bash
python -m app login
```

Run this again any time your session expires.

### Enhance audio

Drop one or more audio files into the `input/` folder, then run:

```bash
python -m app run
```

All audio files in `input/` are processed sequentially. Enhanced files are saved to `output/` as `output-<original-filename>`.

Supported formats: `.mp3`, `.wav`, `.aac`, `.m4a`, `.flac`, `.ogg`, `.opus`

You can also pass files explicitly instead of using the `input/` folder:

```bash
# Single file, saves to output/
python -m app run path/to/recording.mp3

# Multiple specific files
python -m app run a.mp3 b.wav c.m4a

# Custom output directory
python -m app run --output-dir path/to/enhanced/
```

| Argument | Default | Description |
|----------|---------|-------------|
| `INPUT ...` | all audio files in `input/` | One or more audio files to enhance |
| `--output-dir` | `output/` | Where to save the enhanced files |

## Project structure

```
adobe-scrape/
├── input/               # Drop audio files here (contents gitignored)
├── output/              # Enhanced files are saved here (contents gitignored)
├── app/
│   ├── __main__.py      # CLI entry point (login / run commands)
│   ├── config.py        # All constants — URLs, timeouts, XPaths, paths
│   └── scraper/
│       ├── __init__.py  # Public API: enhance_audio
│       ├── auth.py      # is_logged_in() — detects Adobe session state
│       ├── browser.py   # browser_context() — shared browser factory
│       ├── login.py     # login() — manual login flow, saves session
│       └── enhance.py   # enhance_audio() — upload, process, download
├── .env.example         # Environment variable template
├── .gitignore
└── requirements.txt
```

## Notes

- `chrome_profile/` stores your browser session — do not commit it (gitignored)
- No credentials are stored in code or config — login is handled manually via the browser
- Audio processing can take up to 5 minutes depending on file length
- XPath selectors in `app/config.py` are tied to Adobe's current DOM — update them there if the site changes
