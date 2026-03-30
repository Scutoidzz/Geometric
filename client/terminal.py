from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

import PyQt6.QtCore as QtCore
import PyQt6.QtGui as QtGui
import PyQt6.QtWidgets as QtWidgets


CommandHandler = Callable[[list[str]], None]
ScreenFactory = Callable[[list[str]], QtWidgets.QWidget | None]


@dataclass(slots=True)
class TerminalCommand:
    name: str
    description: str
    handler: CommandHandler | None = None
    screen_factory: ScreenFactory | None = None
    aliases: tuple[str, ...] = field(default_factory=tuple)


class TerminalInput(QtWidgets.QLineEdit):
    history_previous = QtCore.pyqtSignal()
    history_next = QtCore.pyqtSignal()

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() == QtCore.Qt.Key.Key_Up:
            self.history_previous.emit()
            return
        if event.key() == QtCore.Qt.Key.Key_Down:
            self.history_next.emit()
            return
        super().keyPressEvent(event)


class GeometricTerminal(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self.setWindowTitle("Geometric Client")
        self.resize(980, 620)

        self.commands: dict[str, TerminalCommand] = {}
        self.history: list[str] = []
        self.history_index = 0
        self._active_screen_name: str | None = None

        self._build_ui()
        self._register_builtin_commands()
        self.print_system(
            "Client started. Make sure your device is plugged in over USB."
        )

    def _build_ui(self) -> None:
        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(12)

        self.mode_label = QtWidgets.QLabel("USB Shell: Geometric Client")
        title_font = QtGui.QFont("Courier New", 13, QtGui.QFont.Weight.Bold)
        self.mode_label.setFont(title_font)
        root.addWidget(self.mode_label)

        self.stack = QtWidgets.QStackedWidget()
        root.addWidget(self.stack)

        self.terminal_page = QtWidgets.QWidget()
        self._build_terminal_page()
        self.stack.addWidget(self.terminal_page)

        self.client_page = QtWidgets.QWidget()
        self._build_client_page()
        self.stack.addWidget(self.client_page)

        self.setStyleSheet(
            """
            QWidget {
                background: #101418;
                color: #e6edf3;
            }
            QPlainTextEdit, QLineEdit, QFrame#clientCard {
                background: #0b0f13;
                border: 1px solid #25313d;
                border-radius: 10px;
            }
            QPlainTextEdit {
                padding: 12px;
            }
            QLineEdit {
                padding: 10px 12px;
            }
            QPushButton {
                background: #1f6feb;
                border: none;
                border-radius: 8px;
                color: white;
                padding: 8px 14px;
            }
            QPushButton:hover {
                background: #388bfd;
            }
            QLabel#clientTitle {
                font-size: 20px;
                font-weight: 700;
            }
            QLabel#clientBody {
                color: #9fb0c0;
            }
            """
        )

    def _build_terminal_page(self) -> None:
        layout = QtWidgets.QVBoxLayout(self.terminal_page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        self.transcript = QtWidgets.QPlainTextEdit()
        self.transcript.setReadOnly(True)
        self.transcript.setLineWrapMode(QtWidgets.QPlainTextEdit.LineWrapMode.NoWrap)
        terminal_font = QtGui.QFont("Courier New", 11)
        self.transcript.setFont(terminal_font)
        layout.addWidget(self.transcript)

        prompt_row = QtWidgets.QHBoxLayout()
        prompt_row.setSpacing(8)

        prompt = QtWidgets.QLabel("geo@client:$")
        prompt.setFont(terminal_font)
        prompt_row.addWidget(prompt)

        self.command_input = TerminalInput()
        self.command_input.setFont(terminal_font)
        self.command_input.setPlaceholderText("Enter a command")
        self.command_input.returnPressed.connect(self.execute_current_command)
        self.command_input.history_previous.connect(self.show_previous_history)
        self.command_input.history_next.connect(self.show_next_history)
        prompt_row.addWidget(self.command_input, 1)

        layout.addLayout(prompt_row)

    def _build_client_page(self) -> None:
        layout = QtWidgets.QVBoxLayout(self.client_page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        button_row = QtWidgets.QHBoxLayout()
        button_row.addStretch(1)

        self.back_button = QtWidgets.QPushButton("Return to terminal")
        self.back_button.clicked.connect(self.return_to_terminal)
        button_row.addWidget(self.back_button)
        layout.addLayout(button_row)

        self.client_card = QtWidgets.QFrame()
        self.client_card.setObjectName("clientCard")
        card_layout = QtWidgets.QVBoxLayout(self.client_card)
        card_layout.setContentsMargins(18, 18, 18, 18)
        card_layout.setSpacing(10)

        self.client_title = QtWidgets.QLabel("Geometric App")
        self.client_title.setObjectName("clientTitle")
        card_layout.addWidget(self.client_title)

        self.client_description = QtWidgets.QLabel("")
        self.client_description.setObjectName("clientBody")
        self.client_description.setWordWrap(True)
        card_layout.addWidget(self.client_description)

        self.client_content = QtWidgets.QVBoxLayout()
        self.client_content.setSpacing(10)
        card_layout.addLayout(self.client_content)
        card_layout.addStretch(1)

        layout.addWidget(self.client_card, 1)

    def _register_builtin_commands(self) -> None:
        self.register_command("help", "List available commands.", self.show_help)
        self.register_command("clear", "Clear the terminal transcript.", self.clear_output)
        self.register_command("exit", "Close the Geometric terminal window.", self.exit_terminal)
        self.register_command("home", "Return from a client screen to the terminal.", self.go_home)

        self.register_screen_command(
            "curl",
            title="Curl",
            description="Fake Geometric curl dashboard. Replace this screen with your real curl UI when ready.",
            screen_factory=self.build_curl_screen,
        )
        self.register_screen_command(
            "status",
            title="Device Status",
            description="Example app screen for battery, USB, and thermal data.",
            screen_factory=self.build_status_screen,
        )

    def register_command(
        self,
        name: str,
        description: str,
        handler: CommandHandler,
        aliases: tuple[str, ...] = (),
    ) -> None:
        command = TerminalCommand(
            name=name,
            description=description,
            handler=handler,
            aliases=aliases,
        )
        self._store_command(command)

    def register_screen_command(
        self,
        name: str,
        title: str,
        description: str,
        screen_factory: ScreenFactory | None = None,
        aliases: tuple[str, ...] = (),
    ) -> None:
        def open_screen(arguments: list[str]) -> None:
            widget = screen_factory(arguments) if screen_factory else None
            self.open_client_screen(name, title, description, widget)

        command = TerminalCommand(
            name=name,
            description=f"Open the {title} client screen.",
            handler=open_screen,
            screen_factory=screen_factory,
            aliases=aliases,
        )
        self._store_command(command)

    def _store_command(self, command: TerminalCommand) -> None:
        keys = (command.name, *command.aliases)
        for key in keys:
            self.commands[key] = command

    def execute_current_command(self) -> None:
        raw_command = self.command_input.text().strip()
        self.command_input.clear()
        if not raw_command:
            return

        self.history.append(raw_command)
        self.history_index = len(self.history)
        self.print_user(raw_command)

        parts = raw_command.split()
        command_name = parts[0].lower()
        arguments = parts[1:]

        command = self.commands.get(command_name)
        if command is None or command.handler is None:
            self.print_error(
                f"Unknown command: {command_name}. Type 'help' for the Geometric command list."
            )
            return

        command.handler(arguments)

    def show_previous_history(self) -> None:
        if not self.history:
            return
        self.history_index = max(0, self.history_index - 1)
        self.command_input.setText(self.history[self.history_index])

    def show_next_history(self) -> None:
        if not self.history:
            return
        if self.history_index >= len(self.history) - 1:
            self.history_index = len(self.history)
            self.command_input.clear()
            return
        self.history_index += 1
        self.command_input.setText(self.history[self.history_index])

    def print_user(self, message: str) -> None:
        self.transcript.appendPlainText(f"geo@client:$ {message}")
        self._scroll_transcript_to_end()

    def print_system(self, message: str) -> None:
        self.transcript.appendPlainText(message)
        self._scroll_transcript_to_end()

    def print_error(self, message: str) -> None:
        self.transcript.appendPlainText(f"[error] {message}")
        self._scroll_transcript_to_end()

    def _scroll_transcript_to_end(self) -> None:
        scrollbar = self.transcript.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def show_help(self, _: list[str]) -> None:
        unique_commands = {
            command.name: command for command in self.commands.values()
        }
        command_lines = [
            f"{name:<10} {command.description}"
            for name, command in sorted(unique_commands.items())
        ]
        self.print_system("Available Geometric commands:")
        for line in command_lines:
            self.print_system(f"  {line}")

    def clear_output(self, _: list[str]) -> None:
        self.transcript.clear()
        self.print_system("Transcript cleared.")

    def exit_terminal(self, _: list[str]) -> None:
        self.print_system("Closing Geometric client.")
        self.close()

    def go_home(self, _: list[str]) -> None:
        self.return_to_terminal()

    def return_to_terminal(self) -> None:
        if self.stack.currentWidget() is self.terminal_page:
            self.command_input.setFocus()
            return
        if self._active_screen_name:
            self.print_system(f"Returned from {self._active_screen_name} to terminal.")
        self._active_screen_name = None
        self.mode_label.setText("USB Shell: Geometric Client")
        self.stack.setCurrentWidget(self.terminal_page)
        self.command_input.setFocus()

    def open_client_screen(
        self,
        name: str,
        title: str,
        description: str,
        widget: QtWidgets.QWidget | None = None,
    ) -> None:
        self._active_screen_name = name
        self.client_title.setText(title)
        self.client_description.setText(description)
        self._clear_client_content()
        self.client_content.addWidget(widget or self.default_screen_body(name))
        self.mode_label.setText(f"Client App: {title}")
        self.stack.setCurrentWidget(self.client_page)
        self.print_system(f"Opened Geometric client app: {name}")

    def _clear_client_content(self) -> None:
        while self.client_content.count():
            item = self.client_content.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def default_screen_body(self, name: str) -> QtWidgets.QWidget:
        body = QtWidgets.QLabel(
            f"'{name}' does not have a custom widget yet. Register a screen factory to render one."
        )
        body.setWordWrap(True)
        return body

    def build_curl_screen(self, _: list[str]) -> QtWidgets.QWidget:
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)
        layout.setContentsMargins(0, 8, 0, 0)
        layout.setSpacing(10)

        headline = QtWidgets.QLabel("HTTP request staging area")
        headline_font = headline.font()
        headline_font.setPointSize(15)
        headline_font.setBold(True)
        headline.setFont(headline_font)
        layout.addWidget(headline)

        for line in (
            "Target: https://example.com/api",
            "Method: GET",
            "Headers: Authorization, Content-Type",
            "Status: idle",
        ):
            layout.addWidget(QtWidgets.QLabel(line))

        hint = QtWidgets.QLabel(
            "Swap this placeholder out with the real curl dashboard once that UI is ready."
        )
        hint.setWordWrap(True)
        layout.addWidget(hint)
        layout.addStretch(1)
        return widget

    def build_status_screen(self, _: list[str]) -> QtWidgets.QWidget:
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QFormLayout(widget)
        layout.setContentsMargins(0, 8, 0, 0)
        layout.setHorizontalSpacing(16)
        layout.setVerticalSpacing(10)
        layout.addRow("USB link", QtWidgets.QLabel("connected"))
        layout.addRow("Battery", QtWidgets.QLabel("84%"))
        layout.addRow("Temperature", QtWidgets.QLabel("38.5 C"))
        layout.addRow("Task", QtWidgets.QLabel("waiting for client command"))
        return widget


def build_demo_terminal() -> GeometricTerminal:
    terminal = GeometricTerminal()
    terminal.register_screen_command(
        "notes",
        title="Quick Notes",
        description="Example custom command showing how Geometric-only screens can be added.",
        screen_factory=lambda _: _build_notes_screen(),
    )
    return terminal


def _build_notes_screen() -> QtWidgets.QWidget:
    widget = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout(widget)
    layout.setContentsMargins(0, 8, 0, 0)
    layout.setSpacing(8)

    title = QtWidgets.QLabel("Notes synced from the phone shell")
    title_font = title.font()
    title_font.setPointSize(14)
    title_font.setBold(True)
    title.setFont(title_font)
    layout.addWidget(title)

    editor = QtWidgets.QTextEdit()
    editor.setPlaceholderText("Write anything here. This widget is yours to replace.")
    layout.addWidget(editor)
    return widget


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = build_demo_terminal()
    window.show()
    sys.exit(app.exec())
