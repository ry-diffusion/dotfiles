from sup.core import EnsureDirectory, Link, Powershell, SudoCopy, InstallPwshProfile

KOMORBI_CONFIG_HOME = "~/Komorebi"
MISC_CONFIG_HOME = "~/.config"

PROFILES = {
    "macOS": [
        Link("neovim", "confs/neovim", "~/.config/nvim"),
        Link("fish", "confs/fish", "~/.config/fish"),
        Link("helix", "confs/helix", "~/.config/helix"),
        Link("git", "confs/gitconfig", "~/.gitconfig"),
    ],
    
    "termux": [
        Link("git", "confs/gitconfig-termux", "~/.gitconfig")
    ],

    "archLinux": [
        Link("neovim", "confs/neovim", "~/.config/nvim"),
        Link("fish", "confs/fish", "~/.config/fish"),
        Link("helix", "confs/helix", "~/.config/helix"),
        Link("git", "confs/gitconfig-linux", "~/.gitconfig"),
        Link("cargo", "confs/cargo-config.toml", "~/.cargo/config.toml"),
        Link("hypr", "confs/hypr", "~/.config/hypr"),
        # SudoCopy("paru", "confs/paru.conf", "/etc/paru.conf"),
    ],
    "Windows": [
        EnsureDirectory(KOMORBI_CONFIG_HOME),
        Link(
            "komorebi",
            "confs/win/komorebi.json",
            f"{KOMORBI_CONFIG_HOME}/komorebi.json",
        ),
        Link(
            "komorebi-ahk",
            "confs/win/komorebi.ahk",
            f"{KOMORBI_CONFIG_HOME}/komorebi.ahk",
        ),
        Link("kanata", "confs/kanata.kbd", f"{MISC_CONFIG_HOME}/kanata.kbd"),
        InstallPwshProfile("win-pwsh-profile", "confs/win/profile.ps1"),
        Link("git", "confs/gitconfig", "~/.gitconfig"),
        Powershell("git config --global gpg.program (Get-Command gpg).Source"),
    ],
}
