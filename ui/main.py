import PyQt6.QtWidgets as QtWidgets
import PyQt6.QtCore as QtCore
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from client.terminal import build_demo_terminal
from ui.feature import plugin


class PluginSignals(QtCore.QObject):
    plugin_signal = QtCore.pyqtSignal()

def homescreen():
    window = QtWidgets.QWidget()
    card = QtWidgets.QFrame()
    card.setObjectName("card")
    card.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
    card.setSizePolicy(
        QtWidgets.QSizePolicy.Policy.Expanding,
        QtWidgets.QSizePolicy.Policy.Expanding,
    )
    card_layout = QtWidgets.QVBoxLayout()
    card_layout.setContentsMargins(0, 0, 0, 0)
    card_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    clock = QtWidgets.QLabel("Blank:Clock")
    clock_font = clock.font()
    clock_font.setPointSize(49)
    clock.setFont(clock_font)
    clock.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    card_title = QtWidgets.QLabel("Not plugged in")
    card_title.setObjectName("cardTitle")
    card_body = QtWidgets.QLabel("Plug a USB cable in to access the command line")
    card_body.setObjectName("cardBody")
    card_layout.addWidget(clock)
    card_layout.addWidget(card_title)
    card_layout.addWidget(card_body)
    card.setLayout(card_layout)

    container = QtWidgets.QVBoxLayout()
    container.setContentsMargins(0, 0, 0, 0)
    container.addWidget(card)
    window.setLayout(container)
    window.setWindowTitle("Geometric")
    window.resize(1212, 540) #<- Pixel 9a dimensions but horizontal.
    
    return window


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    plugin_signals = PluginSignals()
    plugin.attach_plugin_signal(plugin_signals.plugin_signal)
    window = homescreen()
    window.client_windows = []
    simulate_button = QtWidgets.QPushButton("Simulate USB plug in")
    simulate_button.clicked.connect(plugin_signals.plugin_signal.emit)
    window.layout().addWidget(simulate_button)
    terminal_button = QtWidgets.QPushButton("Open Geometric terminal")

    def open_terminal():
        terminal = build_demo_terminal()
        window.client_windows.append(terminal)
        terminal.show()

    terminal_button.clicked.connect(open_terminal)
    window.layout().addWidget(terminal_button)
    window.show()
    sys.exit(app.exec())
 
