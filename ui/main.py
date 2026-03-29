import PyQt6.QtWidgets as QtWidgets
import PyQt6.QtCore as QtCore
import os
import sys

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
    window = homescreen()
    window.show()
    sys.exit(app.exec())
