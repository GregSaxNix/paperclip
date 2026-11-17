' Hidden launcher for "Paperclip Monthly Rules Review" (Task Scheduler, first Tuesday of the month, 10:00 AM).
' Runs scripts\monthly_rules_review.py with pythonw so no console window opens or steals focus.
' Waits for it, so Task Scheduler sees the real run time and exit code.
' Club Wyndham midnight blackout (global rules Part 24): never run 23:29 to 00:10.
h = Hour(Now) : m = Minute(Now)
If (h = 23 And m >= 29) Or (h = 0 And m <= 10) Then WScript.Quit 0

Set sh = CreateObject("WScript.Shell")
sh.CurrentDirectory = "D:\paperclip"
rc = sh.Run("""C:\Python313\pythonw.exe"" ""D:\paperclip\scripts\monthly_rules_review.py""", 0, True)
WScript.Quit rc
