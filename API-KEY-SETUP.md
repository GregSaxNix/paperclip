# API Key Setup Instructions

These instructions are for Greg — step-by-step, no technical jargon.

---

## 1. Firecrawl API Key (Easy — 5 Minutes)

Firecrawl lets agents scrape web pages for recruitment sourcing, research, etc.

### What You Get Free
- **500 lifetime page scrapes** (no credit card needed)
- That's enough for testing and small jobs
- Paid plans available later if you need more

### Steps

1. Go to **https://www.firecrawl.dev/** in your browser
2. Click **Sign up** (top right)
3. Sign in with Google or create an account with email/password
4. Verify your email if prompted
5. Once in the dashboard, look for **API Keys** in the menu
6. Your key looks like: `fc-1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p`
7. **Copy it and save it somewhere safe** (password manager)

### Then Tell the Paperclip Session

> Store the Firecrawl API key in Paperclip's encrypted secrets. The key is: [paste your key here]. Store it as FIRECRAWL_API_KEY.

---

## 2. Microsoft 365 / Office 365 Integration (More Involved — 20 Minutes)

This lets agents read/send email, manage your calendar, and access contacts through your Microsoft 365 subscription.

### Before You Start
- You need **admin access** to your Microsoft 365 account (you should have this as a business owner)
- You'll be using Azure's free admin portal — no extra Azure subscription cost needed
- Your existing Microsoft 365 subscription is enough

### Step 1: Open the Admin Portal

1. Go to **https://entra.microsoft.com** in your browser
2. Sign in with your **Microsoft 365 admin account** (your Shine People Solutions work email)

### Step 2: Create an App Registration

1. In the left menu, click **Identity** → **Applications** → **App registrations**
2. Click the blue **"New registration"** button
3. Fill in:
   - **Name:** `Paperclip Office 365 Integration`
   - **Supported account types:** Select **"Accounts in this organizational directory only"**
   - **Redirect URI:** Leave empty
4. Click **Register**

### Step 3: Copy Your IDs

You'll land on an overview page. **Copy these two values and save them:**

- **Application (client) ID** — looks like `00001111-aaaa-2222-bbbb-3333cccc4444`
- **Directory (tenant) ID** — looks like `aaaabbbb-1111-2222-cccc-3333dddd4444`

### Step 4: Add Permissions

1. In the left menu under "Manage", click **API permissions**
2. Click **"Add a permission"**
3. Click **"Microsoft Graph"**
4. Click **"Delegated permissions"**
5. Search for and tick each of these:
   - `Mail.Read` (read emails)
   - `Mail.Send` (send emails)
   - `Calendars.ReadWrite` (manage calendar)
   - `Contacts.Read` (read contacts)
6. Click **"Add permissions"**
7. Back on the permissions page, click **"Grant admin consent for [Your Organisation]"**
8. Click **Yes** to confirm

### Step 5: Create a Secret (Password for the App)

1. In the left menu under "Manage", click **Certificates & secrets**
2. Click **"New client secret"**
3. Description: `Paperclip`
4. Expires: **6 months** (you'll need to renew it later — set a calendar reminder)
5. Click **Add**
6. **IMMEDIATELY copy the Value** (not the Secret ID) — it looks like `abc123xyzDEF~9_-qwertyABCD1234xyz5678`
7. **You can never see this value again after leaving this page** — save it now!

### Step 6: Save All Three Values

You now have three things to save securely:

| Value | What It Is | Example |
|---|---|---|
| **Tenant ID** | Your organisation's ID | `aaaabbbb-1111-2222-cccc-3333dddd4444` |
| **Client ID** | Your app's ID | `00001111-aaaa-2222-bbbb-3333cccc4444` |
| **Client Secret** | Your app's password | `abc123xyzDEF~9_-qwertyABCD1234xyz5678` |

### Then Tell the Paperclip Session

> Store the Microsoft 365 credentials in Paperclip's encrypted secrets:
> - MS365_TENANT_ID: [paste tenant ID]
> - MS365_CLIENT_ID: [paste client ID]
> - MS365_CLIENT_SECRET: [paste client secret]

---

## Important Reminders

- **Never paste these values into chat publicly** — only into the Paperclip Cursor session
- **The client secret expires** — set a calendar reminder for 2 weeks before expiry to create a new one
- **All values go into Paperclip's encrypted secrets store** — never in plain text files or environment variables
- **If a value gets compromised**, go back to the Azure portal and create a new client secret immediately, then delete the old one

---

## Checklist

### Firecrawl
- [ ] Signed up at firecrawl.dev
- [ ] Copied API key
- [ ] Stored in Paperclip encrypted secrets as FIRECRAWL_API_KEY

### Microsoft 365
- [ ] Logged into entra.microsoft.com
- [ ] Created app registration "Paperclip Office 365 Integration"
- [ ] Copied Tenant ID
- [ ] Copied Client ID
- [ ] Added permissions (Mail.Read, Mail.Send, Calendars.ReadWrite, Contacts.Read)
- [ ] Granted admin consent
- [ ] Created client secret and copied the value
- [ ] Stored all three values in Paperclip encrypted secrets
- [ ] Set calendar reminder to renew client secret before expiry
