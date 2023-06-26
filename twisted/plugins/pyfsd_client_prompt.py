try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

from twisted.application.internet import TCPClient
from twisted.application.service import IServiceMaker, MultiService
from twisted.internet.stdio import StandardIO
from twisted.plugin import IPlugin
from twisted.python.usage import Options
from zope.interface import implementer

from pyfsd.client.factory import FSDClientFactory
from pyfsd.client.prompt import PromptProtocol
from pyfsd.define.utils import verifyConfigStruct
from pyfsd.object.client import Client
from pyfsd.setup_loguru import setupLoguru

DEFAULT_CONFIG = """[client]
address = ""
port = 6809
type = "PILOT"
cid = ""
password = ""
callsign = ""
realname = ""
rating = 1
sim_type = 0"""


class FSDClientOptions(Options):
    optFlags = [
        ["disable-loguru", "l", "Use default logger instead of loguru."],
    ]
    optParameters = [
        ["config-path", "c", "pyfsd_client.toml", "Path to the config file."],
    ]


@implementer(IServiceMaker, IPlugin)
class FSDClientServiceMaker:
    tapname = "fsdclient"
    description = "FSD Client Prompt"
    options = FSDClientOptions

    def makeService(self, options: FSDClientOptions):
        if not options["disable-loguru"]:
            setupLoguru()
        try:
            with open(options["config-path"], "rb") as config_file:
                config = tomllib.load(config_file)
        except FileNotFoundError:
            with open(options["config-path"], "w") as config_file:
                config_file.write(DEFAULT_CONFIG)
            print("Edit {options['config-path']} and run again.")
            return
        verifyConfigStruct(
            config,
            {
                "client": {
                    "address": str,
                    "port": int,
                    "type": str,
                    "cid": str,
                    "password": str,
                    "callsign": str,
                    "realname": str,
                    "rating": int,
                    "sim_type": int,
                }
            },
        )
        config_client = config["client"]
        client = Client(
            config_client["type"],
            config_client["callsign"].encode(),
            config_client["rating"],
            config_client["cid"],
            9,
            config_client["realname"].encode(),
            config_client["sim_type"],
            None,
        )
        root_service = MultiService()
        factory = FSDClientFactory(client)
        TCPClient(
            config_client["address"],
            config_client["port"],
            factory,
            15,
            None,
        ).setServiceParent(root_service)
        StandardIO(
            PromptProtocol(factory.buildProtocol(None), config_client["password"])
        )
        return root_service


serviceMaker = FSDClientServiceMaker()
