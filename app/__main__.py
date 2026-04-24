import argparse
import asyncio
import logging
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)

log = logging.getLogger(__name__)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m app",
        description="Adobe Podcast Enhance — browser automation CLI",
    )
    sub = parser.add_subparsers(dest="command", metavar="COMMAND")

    sub.add_parser(
        "login",
        help="Open a browser window to authenticate with Adobe manually",
    )

    run_cmd = sub.add_parser(
        "run",
        help="Enhance one or more audio files via Adobe Podcast",
    )
    run_cmd.add_argument(
        "inputs",
        nargs="*",
        metavar="INPUT",
        help="Audio files to enhance (default: all audio files in input/)",
    )
    run_cmd.add_argument(
        "--output-dir",
        default=None,
        metavar="DIR",
        help="Directory to save enhanced files (default: output/)",
    )

    return parser


async def _run_all(input_files: list[Path], output_dir: Path) -> None:
    from app.scraper.enhance import enhance_audio

    total = len(input_files)
    for i, path in enumerate(input_files, 1):
        log.info("── File %d/%d: %s", i, total, path.name)
        await enhance_audio(path, output_dir)


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "login":
        from app.scraper.login import login
        asyncio.run(login())

    elif args.command == "run":
        from app.config import AUDIO_EXTENSIONS, INPUT_DIR, OUTPUT_DIR

        if args.inputs:
            input_files = [Path(p) for p in args.inputs]
        else:
            if not INPUT_DIR.exists():
                print(f"Input directory '{INPUT_DIR}' does not exist.")
                sys.exit(1)
            input_files = sorted(
                f for f in INPUT_DIR.iterdir()
                if f.suffix.lower() in AUDIO_EXTENSIONS
            )
            if not input_files:
                print(f"No audio files found in {INPUT_DIR}/")
                sys.exit(1)

        output_dir = Path(args.output_dir) if args.output_dir else OUTPUT_DIR
        log.info("Found %d file(s) to process", len(input_files))
        asyncio.run(_run_all(input_files, output_dir))

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
