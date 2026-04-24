import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# ── URLs ──────────────────────────────────────────────────────────────────────
ADOBE_URL: str = os.getenv("ADOBE_URL", "https://podcast.adobe.com/en/enhance#")

# ── Paths ─────────────────────────────────────────────────────────────────────
PROFILE_DIR: Path = Path(os.getenv("CHROME_PROFILE_DIR", "chrome_profile"))
INPUT_DIR: Path = Path(os.getenv("INPUT_DIR", "input"))
OUTPUT_DIR: Path = Path(os.getenv("OUTPUT_DIR", "output"))

# Audio file extensions recognised when scanning INPUT_DIR
AUDIO_EXTENSIONS: frozenset[str] = frozenset({
    ".mp3", ".wav", ".aac", ".m4a", ".flac", ".ogg", ".opus",
})

# ── Timeouts ──────────────────────────────────────────────────────────────────
AUTH_CHECK_TIMEOUT_MS: int = 3_000
LOGIN_POLL_INTERVAL_S: float = 2.0
PROCESSING_TIMEOUT_MS: int = 300_000  # 5 minutes

# ── Human-like pause range (seconds) ─────────────────────────────────────────
PAUSE_MIN_S: float = 1.0
PAUSE_MAX_S: float = 3.0

# ── XPath selectors ───────────────────────────────────────────────────────────
# Brittle by nature (depend on Adobe's DOM); update here if the site changes.
_BASE = "xpath=/html/body/sp-theme/div/div[1]/div/div/div/div"

XPATH_SIGN_IN_BTN: str = (
    f"xpath=/html/body/sp-theme/div/div[1]/div/div/div/div[1]"
    f"/div/div[2]/div[2]/a"
)
XPATH_VERSION_PICKER: str = (
    f"{_BASE}/div[2]/div/div[1]/div[1]/div/div[2]/sp-picker"
)
XPATH_VERSION_ITEM: str = (
    f"{_BASE}/div[2]/div/div[1]/div[1]/div/div[2]/sp-picker/sp-menu-item[2]"
)
XPATH_UPLOAD_BTN: str = (
    f"{_BASE}/div[2]/div/div[1]/div[2]/sp-button"
)
XPATH_DOWNLOAD_BTN: str = (
    f"{_BASE}/div[5]/div/overlay-trigger/div/button"
)
