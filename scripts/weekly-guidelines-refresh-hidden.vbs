' Hidden launcher for "Paperclip Weekly Guidelines Refresh" (Task Scheduler, Monday 10:00 AM).
' Runs scripts\weekly_guidelines_refresh.py with pythonw so no console window opens or steals focus.
' Waits for it, so Task Scheduler sees the real run time and exit code.
' Club Wyndham midnight blackout (global rules Part 24): never run 23:29 to 00:10.
h = Hour(Now) : m = Minute(Now)
If (h = 23 And m >= 29) Or (h = 0 And m <= 10) Then WScript.Quit 0

Set sh = CreateObject("WScript.Shell")
sh.CurrentDirectory = "D:\paperclip"
rc = sh.Run("""C:\Python313\pythonw.exe"" ""D:\paperclip\scripts\weekly_guidelines_refresh.py""", 0, True)
WScript.Quit rc
