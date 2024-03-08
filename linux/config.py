from sup.core import Link, SudoCopy

MODULES = [
    Link("neovim", "confs/neovim", "~/.config/nvim"),
    Link("fish", "confs/fish", "~/.config/fish"),
    Link("helix", "confs/helix", "~/.config/helix"),
    SudoCopy("paru", "confs/paru.conf", "/etc/paru.conf"),
]