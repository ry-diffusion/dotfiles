function Log($Color, $Message, $Text) {
    Write-Host -NoNewline -ForegroundColor $Color "${Message}"
    Write-Host " ${Text}"
}

$Message = "DarkBlue"
$Info = "DarkGreen"
$Yellow = "DarkYellow"

$Configs = @{
    "App\Git\config" = "~/.gitconfig";
}

Log $Info "Info" "Installing dotfiles"

foreach ($Key in $Configs.Keys) {
    $Value = $Configs[$Key]
	$Path = (Resolve-Path $Key)

    if (-not (Test-Path $Value)) {
        Log $Message "  Install" "${Value} (${Key})"
        New-Item -ItemType HardLink -Target "$Path" -Path $Value
    }
    else {
        Log $Yellow "   Ignore" "${Value} (${Key})"
    }
}