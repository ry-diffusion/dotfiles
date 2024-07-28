from sup.core import Link, Powershell, SudoCopy


PROFILES = {
    "macOS": [
        Link("neovim", "confs/neovim", "~/.config/nvim"),
        Link("fish", "confs/fish", "~/.config/fish"),
        Link("helix", "confs/helix", "~/.config/helix"),
        Link("git", "confs/gitconfig", "~/.gitconfig"),
    ],
    "ubuntu": [
        Link("neovim", "confs/neovim", "~/.config/nvim"),
        Link("fish", "confs/fish", "~/.config/fish"),
        Link("helix", "confs/helix", "~/.config/helix"),
        Link("git", "confs/gitconfig-linux", "~/.gitconfig"),
        Link("cargo", "confs/cargo-config.toml", "~/.cargo/config.toml"),
        # SudoCopy("paru", "confs/paru.conf", "/etc/paru.conf"),
    ],
    "Windows": [
        Link("git", "confs/gitconfig", "~/.gitconfig"),
        Powershell("git config --global gpg.program (Get-Command gpg).Source"),
    ],
}
