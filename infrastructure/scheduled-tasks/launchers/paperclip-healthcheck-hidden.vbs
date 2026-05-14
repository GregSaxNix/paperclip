' Paperclip HealthCheck — wscript launcher for hidden powershell execution.
' Eliminates the brief cmd window flash that powershell.exe -WindowStyle Hidden cannot fully suppress.
' Re-registered scheduled task runs: wscript.exe "D:\paperclip\scripts\paperclip-healthcheck-hidden.vbs"
Set objShell = CreateObject("WScript.Shell")
objShell.Run "powershell.exe -ExecutionPolicy Bypass -File ""D:\paperclip\scripts\paperclip-healthcheck.ps1""", 0, False
