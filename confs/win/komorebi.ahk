#Requires AutoHotkey v2.0.2
#SingleInstance Force

WorkspaceNumber := 9

ArrayFromZero(Length) {
  temp := []

  Loop Length {
    temp.Push(A_Index-1)
  }

  return temp
}

Komorebic(cmd) {
  Run(format("komorebic.exe {}", cmd), , "Hide")
}

; Set workspaces (start from 0)
; ArrayFromZero(9) => [0,1,2,3,4,5,6,7,8]
global numbers := ArrayFromZero(WorkspaceNumber)

init() {
  for num in numbers { 
    RunWait("komorebic workspace-padding 0 " . num . " 10",,"hide")
    RunWait("komorebic container-padding 0 " . num . " 8",,"Hide")
  }
}

;; run init function at start
init()

; Change the focused window, Alt + Vim direction keys
; Focus windows
!h::Komorebic("focus left")
!j::Komorebic("focus down")
!k::Komorebic("focus up")
!l::Komorebic("focus right")

; Move windows
!+h::Komorebic("move left")
!+j::Komorebic("move down")
!+k::Komorebic("move up")
!+l::Komorebic("move right")

; Promote the focused window to the top of the tree, ,Alt + Shift + Enter
!+Enter::Komorebic("promote")

!+r::Komorebic("change-layout rows")
!+c::Komorebic("change-layout columns")
!+b::Komorebic("change-layout bsp")

; Toggle the Monocle layout for the focused window, ,Alt + Shift + F
; Monocle is similar to maximizing, but it will pinned the focused
; window down
!+f::Komorebic("toggle-monocle")

; Use Alt + F to toggle maximize window
; You should always use this shortcut to maximize
; or komorebi won't handle it like issue #12
; https://github.com/LGUG2Z/komorebi/issues/12
!f::Komorebic("toggle-maximize")

; Flip horizontally, ,Alt + Shift + X
!+x::Komorebic("flip-layout horizontal")

; Flip vertically, ,Alt + Shift + Y
!+y::Komorebic("flip-layout vertical")

; Float the focused window Alt + T
!t::Komorebic("toggle-float")
; Toggle Tiling for workspace. Alt + Shift + T
!+t::Komorebic("toggle-tiling")

; Pause responding to any window events or komorebic commands Alt + P
!p::Komorebic("toggle-pause")

; Switch to workspace
; Alt + 1~9
; Equal to bind key !1 to !9 to workspace 0 ~ 8
For num in numbers{
  Hotkey("!" . (num+1), (key) =>
  Komorebic("focus-workspace " . Integer(SubStr(key, 2))-1))
}

; Move window to workspace
; Alt + Shift + 1~9
; Equal to bind key !+1 to !+9 to workspace 0 ~ 8
For num in numbers {
  Hotkey("!+" . (num+1), (key) => 
  Komorebic("move-to-workspace " . Integer(SubStr(key, 3))-1))
}

; Force a retile if things get janky Ctrl + Shift + R
^+r::Komorebic("retile")

;; Native (AHK) Windows Key Rebinding

;; Close Focused Window Alt + X
!x::WinClose("A")

;; Restart komorebi in a hard way
!+q::{

  Komorebic("restore-windows")
  RunWait("powershell " . "Stop-Process -Name 'komorebi'",,"Hide")
  Komorebic("start")
  ;; Delay 1000 milisecond
  Sleep(1000)
  init()
}

;; Get Window Info
;; Helpful for debugging
!+m::{
  window_id := ""
  MouseGetPos(,,&window_id)
  window_title := WinGetTitle(window_id)
  window_class := WinGetClass(window_id)
  MsgBox(window_id "`n" window_class "`n" window_title)
}

;; this is a global state. 
;; ? how to moddify it to a functional style?
global minimized_window := ""
;; Window should not be minimized
global FilterOutClass := ["WorkerW", "Shell_TrayWnd", "NotifyIconOverflowWindow"]
;; Alt + M
;; toggle minimize
;; minimize window will be saved until restore
;; useful when a window (especially vscode) get stuck
!m::{
  try {
    ;; If there is a window under the cursor then active it
    window_id := ""
    MouseGetPos(,,&window_id)
    WinActivate(window_id)
    ;; then process
    active_id := WinGetID("A")
    window_state := WinGetMinMax("A")
    if (minimized_window != ""){
      WinRestore(minimized_window)
      global minimized_window := ""
    } else {
      for filter in FilterOutClass{
        if(WinGetClass(active_id) == filter){
          ;; break out of the function
          return
        }
      }
      WinMinimize(active_id)
      global minimized_window := active_id
    }
  } catch as e {
    ;; If there's an error, it likely is cannot find focused window
    ;; this will focus a window under mouse cursor
    ;; I don't think this catch is meaningful
    window_id := ""
    MouseGetPos(,,&window_id)
    WinActivate(window_id)
  }
}