from typing import TYPE_CHECKING

from zope.interface import Attribute, Interface, implementer

if TYPE_CHECKING:
    from .object.client import Client
    from .protocol.client import FSDClientProtocol
    from .service import PyFSDService


class IPyFSDPlugin(Interface):
    plugin_name = Attribute("plugin_name")

    def beforeStart(pyfsd: "PyFSDService") -> None:
        ...

    def beforeStop() -> None:
        ...

    def newConnectionEstablished(protocol: "FSDClientProtocol") -> None:
        ...

    def newClientCreated(protocol: "FSDClientProtocol") -> None:
        ...

    def lineReceivedFromClient(protocol: "FSDClientProtocol", byte_line: bytes) -> None:
        ...

    def clientDisconnected(protocol: "FSDClientProtocol", client: "Client") -> bool:
        ...


@implementer(IPyFSDPlugin)
class BasePyFSDPlugin:
    plugin_name = "<plugin name missing>"

    def beforeStart(self, pyfsd: "PyFSDService") -> None:
        ...

    def beforeStop(self) -> None:
        ...

    def newConnectionEstablished(self, protocol: "FSDClientProtocol") -> bool:
        ...

    def newClientCreated(self, protocol: "FSDClientProtocol") -> bool:
        ...

    def lineReceivedFromClient(
        self, protocol: "FSDClientProtocol", byte_line: bytes
    ) -> None:
        ...

    def clientDisconnected(
        self, protocol: "FSDClientProtocol", client: "Client"
    ) -> bool:
        ...


class PreventEvent(Exception):
    pass