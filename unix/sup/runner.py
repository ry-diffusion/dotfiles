from config import PROFILES
from .utils import confirm
from .store import STORE_PATH, load, save
from .core import AlreadyInstalled, Injectable, NotInstalled, UserRefused
from atexit import register
from sys import argv

PROFILES: dict[str, list[Injectable]] = PROFILES

load()
register(save)

print(f"[@] using store at {STORE_PATH}")


def dump(modules: list[Injectable]):
    for module in modules:
        print(
            f"--> {module.id}:\n -> installed? {module.installed()}\n -> exists in system? {module.exists_in_system()}"
        )


def install_module(module: Injectable):
    print(f"= ({module.id}): ")

    if module.exists_in_system() and not module.installed():
        print(" !> unable to install: exists in filesystem.")
        if confirm("overwrite existing config"):
            module.backup_and_remove()
            print("\n  -> generated backup!")
            module.install()
            print("  -> installed")
        else:
            print("\n -> kept old configuration.")
        return

    try:
        module.install()
        print(" -> installed!")
    except AlreadyInstalled:
        print(" => already installed, no more actions required.")
    except UserRefused:
        print(" !> unable to install: user refused to install")


def uninstall_module(module: Injectable):
    print(f"= ({module.id}): ")
    try:
        module.uninstall()
        print(" => uninstalled! cya.")
    except UserRefused:
        print(" !> unable to install: user refused to uninstall!")
    except NotInstalled:
        print(" -> not installed, nothing to do.")


def install(modules: list[Injectable]):
    for module in modules:
        install_module(module)


def uninstall(modules: list[Injectable]):
    for module in modules:
        uninstall_module(module)


if __name__ == "__main__":
    [action, profile] = argv[1:]

    if profile not in PROFILES:
        print(f"error: unknown profile {profile}")
        exit(1)

    modules = PROFILES[profile]

    match action:
        case "dump":
            dump(modules)
        case "install":
            install(modules)
        case "uninstall":
            uninstall(modules)
