# Assistant OS — Monday Review Reminder
# Pops a notification and opens the review dashboard in default browser.

[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms') | Out-Null
[System.Windows.Forms.MessageBox]::Show(
    "Time to review pending Assistant OS items (recruiting-playbook, brand-voice, shine-website-launch). Click OK to open the dashboard.",
    "Assistant OS Reminder",
    'OK',
    'Information'
) | Out-Null

Start-Process 'file:///D:/assistant-os/dashboard/review.html'
