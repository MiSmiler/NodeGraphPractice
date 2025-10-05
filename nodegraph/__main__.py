from PyQt6.QtWidgets import QApplication
from nodegraph.main_window import MainWindow

# Only needed for access to command line arguments
# import sys


def main():
    # You need one (and only one) QApplication instance per application.
    # Pass in sys.argv to allow command line arguments for your app.
    # If you know you won't use command line arguments QApplication([]) works too.
    app = QApplication([])
    window = MainWindow()
    window.show()

    # Start the event loop.
    app.exec()


if __name__ == "__main__":
    main()
