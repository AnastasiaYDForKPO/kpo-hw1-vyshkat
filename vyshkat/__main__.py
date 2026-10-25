import sys

from .bootstrap import build_container
from .console import ConsoleApp, ConsoleIO
from .demo import run_demo


def main():
    container = build_container()
    app = container.resolve(ConsoleApp)
    if "--demo" in sys.argv:
        run_demo(app, container.resolve(ConsoleIO))
    else:
        app.run()


main()