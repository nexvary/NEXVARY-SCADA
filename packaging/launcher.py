from __future__ import annotations

import sys
import threading
import webbrowser

from nexvary_scada.api import app, main, runtime


def _open_executive_view() -> None:
    webbrowser.open("http://127.0.0.1:8765/#executive", new=1)


def run() -> None:
    if "--check" in sys.argv:
        values = runtime.poll()
        assert app.title == "NEXVARY SCADA"
        assert values
        print(f"NEXVARY SCADA executable smoke check OK: {len(values)} tags")
        return

    if "--no-browser" not in sys.argv:
        threading.Timer(1.2, _open_executive_view).start()
    main()


if __name__ == "__main__":
    run()
