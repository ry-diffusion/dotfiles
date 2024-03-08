from os.path import exists, expanduser, realpath
from json import dump, load as load_json

STORE_VERSION = 1
STORE_PATH = realpath(expanduser("~/.local/share/sup_store.json"))


class StoreState:
    version: int = STORE_VERSION
    installed: list[str] = []

    def _restore(self, json: dict):
        self.installed = json["installed"]
        self.version = json["version"]

    def _todict(self) -> dict:
        return {
            "version": self.version,
            "installed": self.installed,
        }


STORE = StoreState()


def save():
    with open(STORE_PATH, "w") as sp:
        dump(STORE._todict(), sp)


def load():
    if not exists(STORE_PATH):
        save()

    with open(STORE_PATH, "r") as sp:
        target = load_json(sp)
        STORE._restore(target)
