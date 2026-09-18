from __future__ import annotations

import sys

from nexvary_scada.api import app, main, runtime


def run() -> None:
    if "--check" in sys.argv:
        values = runtime.poll()
        assert app.title == "NEXVARY SCADA"
        assert values
        print(f"NEXVARY SCADA executable smoke check OK: {len(values)} tags")
        return
    main()


if __name__ == "__main__":
    run()
