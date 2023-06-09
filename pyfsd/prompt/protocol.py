from typing import TYPE_CHECKING

from twisted.conch.manhole import (
    CTRL_A,
    CTRL_BACKSLASH,
    CTRL_C,
    CTRL_D,
    CTRL_E,
    CTRL_L,
    Manhole,
)
from twisted.conch.recvline import HistoricRecvLine

if TYPE_CHECKING:
    from twisted.conch.insults.insults import ServerProtocol


class PromptProtocol(Manhole):
    terminal: "ServerProtocol"

    def __init__(self) -> None:
        pass

    def connectionMade(self) -> None:
        HistoricRecvLine.connectionMade(self)
        self.keyHandlers[CTRL_C] = self.handle_INT
        self.keyHandlers[CTRL_D] = self.handle_EOF
        self.keyHandlers[CTRL_L] = self.handle_FF
        self.keyHandlers[CTRL_A] = self.handle_HOME
        self.keyHandlers[CTRL_E] = self.handle_END
        self.keyHandlers[CTRL_BACKSLASH] = self.handle_QUIT

    def lineReceived(self, line) -> None:
        pass

    def handle_INT(self) -> None:
        """
        Handle ^C as an interrupt keystroke by resetting the current input
        variables to their initial state.
        """
        self.pn = 0
        self.lineBuffer = []
        self.lineBufferIndex = 0

        self.terminal.nextLine()
        self.terminal.write(b"KeyboardInterrupt")
        self.terminal.nextLine()
        self.terminal.write(self.ps[self.pn])

    def initializeScreen(self) -> None:
        self.terminal.write(self.ps[self.pn])
        self.setInsertMode()

    def handle_QUIT(self):
        self.setTypeoverMode()
        self.terminal.transport.loseConnection()  # Avoid clear screen
