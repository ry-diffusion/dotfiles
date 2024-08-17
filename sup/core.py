from os.path import exists, expanduser, realpath, isdir
from os import symlink, system, unlink, makedirs
from subprocess import run
from .utils import backup_and_remove
from .store import STORE
from .error import FailedToRunCommand, CantUninstall, AlreadyInstalled, UserRefused, NotInstalled

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


class Powershell(Injectable):
    command: str
    id: str

    def __init__(self, command: str) -> None:
        self.id = "powershell-command"
        self.command = expanduser(command)

    def installed(self) -> bool:
        return False 

    def exists_in_system(self) -> bool:
        return False

    def install(self):
        if self.id in STORE.installed:
            raise AlreadyInstalled()

        cmd = ["powershell", "-noni", "-nop", "-c", self.command]
        print(f"$ {' '.join(cmd)}")
        if run(cmd).returncode != 0:
            raise FailedToRunCommand()

    def uninstall(self):
        raise CantUninstall
    

class InstallPwshProfile(Injectable):
    sourcePath: str
    id: str

    def get_profile_path(self):
        command = "pwsh -Command $PROFILE"
        result = run(command, capture_output=True, text=True, shell=True)

        return result.stdout.strip()

    def __init__(self, id: str, target: str) -> None:
        self.id = id
        self.sourcePath = realpath(expanduser(target))


    def exists_in_system(self) -> bool:
        return exists(self.sourcePath)

    def installed(self) -> bool:
        return self.id in STORE.installed


    def install(self):
        if self.id in STORE.installed:
            raise AlreadyInstalled()
        
        symlink(self.sourcePath, self.get_profile_path())
        STORE.installed.append(self.id)

    def uninstall(self):
        unlink(self.sourcePath)

class EnsureDirectory(Injectable):
    def __init__(self, path: str) -> None:
        self.path = realpath(expanduser(path))
        self.id = "ensure-directory"

    def exists_in_system(self) -> bool:
        return False

    def installed(self) -> bool:
        return False
    
    def install(self):
        if self.id in STORE.installed:
            raise AlreadyInstalled()

        if not isdir(self.path):
            makedirs(self.path)        

        STORE.installed.append(self.id)

    