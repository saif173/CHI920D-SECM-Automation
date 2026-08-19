import sys
from pathlib import Path

from streamlit.web import cli as stcli


def main():

    # Location of the packaged application
    if getattr(sys, "frozen", False):
        base_dir = Path(sys._MEIPASS)
    else:
        base_dir = Path(__file__).resolve().parent

    home = base_dir / "Home.py"

    sys.argv = [
        "streamlit",
        "run",
        str(home),
        "--server.headless=true",
        "--browser.gatherUsageStats=false",
    ]

    sys.exit(stcli.main())


if __name__ == "__main__":
    main()