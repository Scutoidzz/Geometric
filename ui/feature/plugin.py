import PyQt6.QtWidgets as QtWidgets
import PyQt6.QtCore as QtCore
import PyQt6.QtGui as QtGui
import os
import sys

_runner = None


class geo_ui(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.container = self
        self.homelayout = QtWidgets.QHBoxLayout(self)
        # other layouts
        self.weatherlayout = QtWidgets.QLabel()
        self.weatherlargefont = QtGui.QFont("Arial", 32)
        self.weatherlayout.setFont(self.weatherlargefont)

        self.vertical_line = QtWidgets.QFrame()
        self.vertical_line.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.vertical_line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.vertical_line.setLineWidth(2)

        self.forecast = QtWidgets.QHBoxLayout()


class _PluginRunner(QtCore.QObject):
    @QtCore.pyqtSlot()
    def run(self):
        self.ui = geo_ui()
        self.ui.show()


def attach_plugin_signal(plugin_signal: QtCore.pyqtSignal):
    global _runner
    if _runner is None:
        _runner = _PluginRunner()
    plugin_signal.connect(_runner.run, QtCore.Qt.ConnectionType.QueuedConnection)
