from os.path import exists, expanduser, realpath, isdir
from os import symlink, system, unlink

from .utils import backup_and_remove
from .store import STORE


class Injectable:
    id: str

    def installed(self) -> bool:
        return False

    def exists_in_system(self) -> bool:
        return False

    def install(self):
        pass

    def uninstall(self):
        pass

    def backup_and_remove(self):
        pass


class AlreadyInstalled(Exception):
    pass


class UserRefused(Exception):
    pass


class NotInstalled(Exception):
    pass


class Link(Injectable):
    source: str
    target: str
    id: str

    def __init__(self, id: str, source: str, target: str) -> None:
        self.source = realpath(source)
        self.target = expanduser(target)
        self.id = id

    def exists_in_system(self) -> bool:
        return exists(self.target)

    def installed(self) -> bool:
        return self.id in STORE.installed

    def install(self):
        if self.installed():
            raise AlreadyInstalled()

        symlink(self.source, self.target, isdir(self.source))
        STORE.installed.append(self.id)

    def backup_and_remove(self):
        backup_and_remove(self.target)

    def uninstall(self):
        if not self.installed():
            raise NotInstalled()

        unlink(self.target)
        STORE.installed.remove(self.id)


class SudoCopy(Injectable):
    source: str
    target: str
    id: str

    def __init__(self, id: str, source: str, target: str) -> None:
        self.id = id
        self.source = realpath(source)
        self.target = expanduser(target)

    def installed(self) -> bool:
        return self.id in STORE.installed

    def exists_in_system(self) -> bool:
        return exists(self.target)

    def install(self):
        if self.id in STORE.installed:
            raise AlreadyInstalled()

        command = f"sudo cp -r {self.source} {self.target}"
        print(f"$ {command}")
        if system(command) != 0:
            raise UserRefused()

        STORE.installed.append(self.id)

    def uninstall(self):
        if not self.installed():
            raise NotInstalled()

        command = f"sudo rm -ri {self.target}"
        print(f"$ {command}")

        if system(command) != 0:
            raise UserRefused()

        STORE.installed.remove(self.id)
