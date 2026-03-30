import PyQt6.QtCore as QtCore
import PyQt6.QtWidgets as QtWidgets


def _make_section_card(title: str) -> tuple[QtWidgets.QFrame, QtWidgets.QVBoxLayout]:
    card = QtWidgets.QFrame()
    card.setObjectName("clientCard")

    layout = QtWidgets.QVBoxLayout(card)
    layout.setContentsMargins(14, 14, 14, 14)
    layout.setSpacing(8)

    heading = QtWidgets.QLabel(title)
    heading_font = heading.font()
    heading_font.setPointSize(13)
    heading_font.setBold(True)
    heading.setFont(heading_font)
    layout.addWidget(heading)

    return card, layout


def build_curl_screen(_: list[str]) -> QtWidgets.QWidget:
    widget = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout(widget)
    layout.setContentsMargins(0, 8, 0, 0)
    layout.setSpacing(12)

    headline = QtWidgets.QLabel("HTTP request staging area")
    headline_font = headline.font()
    headline_font.setPointSize(15)
    headline_font.setBold(True)
    headline.setFont(headline_font)
    layout.addWidget(headline)

    subhead = QtWidgets.QLabel(
        "Prepare a request on the desktop, then send the finished payload to the phone."
    )
    subhead.setWordWrap(True)
    layout.addWidget(subhead)

    request_card, request_layout = _make_section_card("Request")
    request_layout.addWidget(QtWidgets.QLabel("Target: https://example.com/api"))
    request_layout.addWidget(QtWidgets.QLabel("Method: GET"))
    request_layout.addWidget(
        QtWidgets.QLabel("Headers: Authorization, Content-Type")
    )
    request_layout.addWidget(QtWidgets.QLabel("Body: empty"))
    layout.addWidget(request_card)

    status_card, status_layout = _make_section_card("Transfer Status")
    status_layout.addWidget(QtWidgets.QLabel("USB link: connected"))
    status_layout.addWidget(QtWidgets.QLabel("Last response: not started"))
    status_layout.addWidget(QtWidgets.QLabel("Phone task: waiting"))
    layout.addWidget(status_card)

    actions = QtWidgets.QHBoxLayout()
    actions.setSpacing(10)

    queue_button = QtWidgets.QPushButton("Queue Request")
    preview_button = QtWidgets.QPushButton("Preview Headers")
    actions.addWidget(queue_button)
    actions.addWidget(preview_button)
    actions.addStretch(1)
    layout.addLayout(actions)

    helper = QtWidgets.QLabel(
        "This is the shared curl screen used by the Geometric terminal command."
    )
    helper.setWordWrap(True)
    helper.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
    layout.addWidget(helper)

    layout.addStretch(1)
    return widget


def build_download_screen(_: list[str]) -> QtWidgets.QWidget:
    widget = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout(widget)
    layout.setContentsMargins(0, 8, 0, 0)
    layout.setSpacing(12)

    headline = QtWidgets.QLabel("Device downloads")
    headline_font = headline.font()
    headline_font.setPointSize(15)
    headline_font.setBold(True)
    headline.setFont(headline_font)
    layout.addWidget(headline)

    hint = QtWidgets.QLabel(
        "Stage packages here before sending them down to the phone over USB."
    )
    hint.setWordWrap(True)
    layout.addWidget(hint)

    downloads_card, downloads_layout = _make_section_card("Available Downloads")
    for line in (
        "1. System update 1.0.3",
        "2. Curl presets bundle",
        "3. Voice assistant assets",
        "4. Offline maps region pack",
    ):
        downloads_layout.addWidget(QtWidgets.QLabel(line))
    layout.addWidget(downloads_card)

    details_card, details_layout = _make_section_card("Selection Details")
    details_body = QtWidgets.QLabel(
        "Select a package to review size, checksum, and install readiness."
    )
    details_body.setWordWrap(True)
    details_layout.addWidget(details_body)
    #TODO: Make this show real data
    details_layout.addWidget(QtWidgets.QLabel("Download queue: empty"))
    details_layout.addWidget(QtWidgets.QLabel("Storage available: 12.4 GB"))
    layout.addWidget(details_card)

    footer = QtWidgets.QLabel(
        "Use this screen for package browsing while the terminal handles the command flow."
    )
    footer.setWordWrap(True)
    layout.addWidget(footer)

    layout.addStretch(1)
    return widget
