$Env:KOMOREBI_CONFIG_HOME = "$Env:USERPROFILE/Komorebi"

function Logcat {
    param (
        [string]$pkg,
        [string[]]$args
    )

    if (-not $pkg) {
        Write-Error 'Usage: Logcat -pkg <pkg> [-args <args>]'
        return
    }

    $uid = adb shell pm list packages -U $pkg | Select-String -Pattern 'uid:(\d+)' | ForEach-Object { $_.Matches[0].Groups[1].Value }
    if (-not $uid) {
        Write-Error "Package '$pkg' not found"
        return
    }

    adb logcat -b all -v color --uid=$uid @args
}

$THEME = "catppuccin_frappe"

oh-my-posh init pwsh --config "$env:POSH_THEMES_PATH\$THEME.omp.json" | Invoke-Expression

Set-PSReadLineKeyHandler -Key Tab -Function MenuComplete

