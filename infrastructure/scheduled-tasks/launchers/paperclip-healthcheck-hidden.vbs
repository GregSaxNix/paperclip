' Paperclip HealthCheck — wscript launcher for hidden powershell execution.
' Eliminates the brief cmd window flash that powershell.exe -WindowStyle Hidden cannot fully suppress.
' Re-registered scheduled task runs: wscript.exe "D:\paperclip\scripts\paperclip-healthcheck-hidden.vbs"
' Skip 23:29-00:10 so this job cannot steal focus during Club Wyndham T1 clicks.
h = Hour(Now) : m = Minute(Now)
If (h = 23 And m >= 29) Or (h = 0 And m <= 10) Then WScript.Quit 0
Set objShell = CreateObject("WScript.Shell")
objShell.Run "powershell.exe -ExecutionPolicy Bypass -File ""D:\paperclip\scripts\paperclip-healthcheck.ps1""", 0, False
