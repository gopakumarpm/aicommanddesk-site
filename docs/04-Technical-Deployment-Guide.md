# AICommandDesk.com — Technical Deployment Guide

**Document Version:** 1.0
**Date:** February 2026
**For:** Non-technical founder — step-by-step instructions

---

## TABLE OF CONTENTS

1. What You Have Built (Architecture Overview)
2. Setting Up GitHub (Your Code Storage)
3. Deploying to Netlify (Making It Live)
4. Connecting Your Domain (AICommandDesk.com)
5. Setting Up Decap CMS (Your Publishing Dashboard)
6. Setting Up Google Analytics & Search Console
7. Setting Up Your Email Newsletter
8. How to Write & Publish New Blog Posts
9. How to Update Your Website
10. Troubleshooting Common Issues
11. Monthly Maintenance Checklist

---

## 1. WHAT YOU HAVE BUILT

### 1.1 Architecture Overview

```
Your Computer (source code)
       |
       ↓
GitHub Repository (stores your code online)
       |
       ↓
Netlify (builds & hosts your website)
       |
       ↓
AICommandDesk.com (your live website)
       |
       ↓
Decap CMS (/admin) → lets you write blog posts in a browser
```

### 1.2 Technology Stack (What Each Piece Does)

| Technology | What It Does | Cost |
|-----------|-------------|------|
| **Astro** | Builds your website from source files into fast HTML | Free |
| **Tailwind CSS** | Makes the website look beautiful | Free |
| **GitHub** | Stores your website code online (like Google Drive for code) | Free |
| **Netlify** | Hosts your website on the internet | Free (starter plan) |
| **Decap CMS** | Lets you write blog posts through a web browser | Free |
| **GoDaddy** | Where you bought your domain name | ₹1,200/year |

### 1.3 Your Project Files

```
aicommanddesk-site/
├── src/                    ← Your website source code
│   ├── components/         ← Reusable parts (header, footer, etc.)
│   ├── content/blog/       ← YOUR BLOG POSTS (Markdown files)
│   ├── layouts/            ← Page templates
│   ├── pages/              ← Individual pages (home, about, etc.)
│   └── styles/             ← CSS styling
├── public/                 ← Static files (images, admin panel)
│   ├── admin/              ← Decap CMS configuration
│   ├── images/             ← Your images
│   └── favicon.svg         ← Site icon
├── package.json            ← Project dependencies
├── astro.config.mjs        ← Astro settings
├── tailwind.config.mjs     ← Design settings
└── netlify.toml            ← Netlify deployment settings
```

---

## 2. SETTING UP GITHUB

### 2.1 Create a GitHub Account

1. Go to **https://github.com**
2. Click **"Sign up"**
3. Enter your email, create a password, choose a username
4. Verify your email
5. Select the **Free plan** (that's all you need)

### 2.2 Install Git on Your Computer

1. Go to **https://git-scm.com/downloads**
2. Download for Windows
3. Run the installer (keep all default settings — just click Next)
4. After installation, open **Terminal** (or Command Prompt)
5. Type this and press Enter:
   ```
   git --version
   ```
6. You should see something like: `git version 2.43.0`

### 2.3 Configure Git (One-Time Setup)

Open Terminal and type these commands (replace with YOUR info):

```bash
git config --global user.name "Your Name"
git config --global user.email "your-email@gmail.com"
```

### 2.4 Create a GitHub Repository

1. Go to **https://github.com/new**
2. Repository name: `aicommanddesk-site`
3. Description: "AICommandDesk.com website"
4. Select: **Public** (needed for Netlify free plan)
5. Do NOT check any boxes (no README, no .gitignore)
6. Click **"Create repository"**
7. You will see a page with commands — keep this page open

### 2.5 Push Your Code to GitHub

Open Terminal, navigate to your project folder, and run:

```bash
cd "d:/Data-science/Claude/Blogging/aicommanddesk-site"

git init
git add .
git commit -m "Initial commit: AICommandDesk.com website"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/aicommanddesk-site.git
git push -u origin main
```

**Replace `YOUR-USERNAME` with your actual GitHub username.**

When prompted, enter your GitHub username and password (or personal access token).

### 2.6 Verify Upload

1. Go to **https://github.com/YOUR-USERNAME/aicommanddesk-site**
2. You should see all your project files listed
3. If you see them — your code is safely stored online

---

## 3. DEPLOYING TO NETLIFY

### 3.1 Create a Netlify Account

1. Go to **https://app.netlify.com**
2. Click **"Sign up"**
3. Choose **"Sign up with GitHub"** (easiest method)
4. Authorise Netlify to access your GitHub

### 3.2 Deploy Your Site

1. In Netlify dashboard, click **"Add new site"** → **"Import an existing project"**
2. Select **"GitHub"**
3. Choose the repository: `aicommanddesk-site`
4. Configure build settings:
   - **Branch to deploy:** `main`
   - **Build command:** `npm run build`
   - **Publish directory:** `dist`
5. Click **"Deploy site"**

### 3.3 Wait for Deployment

- Netlify will build your site (takes 1-3 minutes)
- You will see a green "Published" status when done
- Netlify gives you a temporary URL like: `random-name-12345.netlify.app`
- Click it to see your LIVE website

### 3.4 Verify Your Site

Open the Netlify URL and check:
- [ ] Homepage loads correctly
- [ ] Navigation works (all pages accessible)
- [ ] Blog posts display properly
- [ ] Dark mode toggle works
- [ ] Mobile view looks good (resize browser or use phone)
- [ ] Newsletter forms are visible

---

## 4. CONNECTING YOUR DOMAIN

### 4.1 Add Custom Domain in Netlify

1. In Netlify, go to **Site settings** → **Domain management**
2. Click **"Add custom domain"**
3. Type: `aicommanddesk.com`
4. Click **"Verify"** → **"Add domain"**
5. Also add: `www.aicommanddesk.com`

### 4.2 Update DNS in GoDaddy

Netlify will show you the DNS records you need. Here's what to do:

1. Go to **https://dcc.godaddy.com** (GoDaddy Domain Control Center)
2. Click on **aicommanddesk.com**
3. Go to **DNS** or **DNS Management**
4. **Option A (Recommended): Use Netlify DNS**
   - In Netlify, go to Domain settings → click "Set up Netlify DNS"
   - Netlify will give you nameservers (like: dns1.p06.nsone.net)
   - In GoDaddy, change nameservers to the ones Netlify provides
   - This gives Netlify full control (easiest to manage)

5. **Option B: Keep GoDaddy DNS (Manual Records)**
   - Add an **A record**: Host `@` → Points to `75.2.60.5`
   - Add a **CNAME record**: Host `www` → Points to `your-site-name.netlify.app`
   - Delete any existing A records for `@`

### 4.3 Enable HTTPS (SSL Certificate)

1. In Netlify → Domain settings → HTTPS
2. Click **"Verify DNS configuration"**
3. Click **"Provision certificate"**
4. Wait 5-15 minutes for SSL to activate
5. Enable **"Force HTTPS"** toggle

### 4.4 Verify Domain Connection

After DNS propagation (can take up to 48 hours, usually 1-4 hours):

- [ ] https://aicommanddesk.com loads your site
- [ ] https://www.aicommanddesk.com redirects correctly
- [ ] The padlock icon appears (HTTPS active)
- [ ] No "Not Secure" warning

---

## 5. SETTING UP DECAP CMS

Decap CMS lets you write blog posts through a web browser (like WordPress) without touching any code.

### 5.1 Enable Netlify Identity

1. In Netlify dashboard → **Site settings** → **Identity**
2. Click **"Enable Identity"**
3. Under Registration → select **"Invite only"** (so only you can log in)
4. Under External providers → enable **"Google"** (for easy login)

### 5.2 Enable Git Gateway

1. Still in Identity settings → **Services** → **Git Gateway**
2. Click **"Enable Git Gateway"**
3. This allows Decap CMS to save posts directly to your GitHub repository

### 5.3 Invite Yourself

1. In Identity → click **"Invite users"**
2. Enter YOUR email address
3. Click **"Send"**
4. Check your email and click the invitation link
5. Set a password

### 5.4 Access Your CMS

1. Go to: **https://aicommanddesk.com/admin/**
2. Click **"Login with Netlify Identity"**
3. Enter your email and password (or use Google login)
4. You should see the Decap CMS dashboard with "Blog Posts" collection

### 5.5 How to Write a New Blog Post via CMS

1. Go to https://aicommanddesk.com/admin/
2. Click **"Blog Posts"** → **"New Blog Post"**
3. Fill in the fields:
   - **Title:** Your post title
   - **Description:** 1-2 sentence summary (this appears in Google results)
   - **Publish Date:** Select today's date
   - **Author:** AI Command Desk (or your name)
   - **Category:** Choose from dropdown
   - **Tags:** Add relevant tags (comma-separated)
   - **Featured Post:** Toggle on/off
   - **Draft:** Keep ON until ready to publish
   - **Body:** Write your article using the rich text editor
4. Click **"Save"** → This creates a draft (saved to GitHub)
5. Change status from "Draft" to **"Ready"**
6. Click **"Publish"** → Changes go live in 1-2 minutes

---

## 6. SETTING UP GOOGLE ANALYTICS & SEARCH CONSOLE

### 6.1 Google Analytics 4

1. Go to **https://analytics.google.com**
2. Click **"Start measuring"**
3. Account name: `AICommandDesk`
4. Property name: `AICommandDesk.com`
5. Select your country and currency (India, INR)
6. Choose **Business** and select relevant categories
7. Accept terms of service
8. Choose **Web** platform
9. Enter: `https://aicommanddesk.com`
10. Stream name: `AICommandDesk Website`
11. You will get a **Measurement ID** (looks like: `G-XXXXXXXXXX`)

**To add this to your site:**
You need to add the Google Analytics script to your website's head section. Ask Claude Code to help add the GA4 tracking code to your BaseLayout.astro file.

### 6.2 Google Search Console

1. Go to **https://search.google.com/search-console**
2. Click **"Add property"**
3. Choose **"URL prefix"**
4. Enter: `https://aicommanddesk.com`
5. For verification, choose **"HTML tag"** method
   - Copy the meta tag
   - Add it to your BaseLayout.astro `<head>` section
   - Deploy the change
6. Click **"Verify"**
7. Go to **Sitemaps** → Submit: `https://aicommanddesk.com/sitemap-index.xml`

---

## 7. SETTING UP YOUR EMAIL NEWSLETTER

### 7.1 Recommended: Beehiiv (Free Tier)

1. Go to **https://beehiiv.com**
2. Sign up for free plan
3. Create publication: "AI Command Brief"
4. Set up your profile and branding

### 7.2 Connect Newsletter to Your Website

Once you have Beehiiv set up, you need to update the newsletter forms on your site to actually submit to Beehiiv.

**Option A: Use Netlify Forms (Current Setup)**
Your forms already work with Netlify Forms. You can view submissions in:
Netlify Dashboard → Forms → See form submissions

**Option B: Replace with Beehiiv Embed**
Ask Claude Code to replace the newsletter forms with Beehiiv embed code. You will get this code from your Beehiiv dashboard → Growth → Embeds.

### 7.3 Create Your Welcome Sequence

In Beehiiv → Automations → Create:
1. Email 1 (Immediate): Welcome + deliver lead magnet
2. Email 2 (Day 2): The #1 mistake managers make with AI
3. Email 3 (Day 4): 3 AI tools I recommend
4. Email 4 (Day 7): Your first AI automation
5. Email 5 (Day 10): What to read next

---

## 8. HOW TO WRITE & PUBLISH NEW BLOG POSTS

### Method 1: Through Decap CMS (Recommended for You)

1. Go to https://aicommanddesk.com/admin/
2. Login
3. New Blog Post → Write → Save → Publish
4. Wait 1-2 minutes for Netlify to rebuild
5. Your new post is live

### Method 2: Through Markdown Files (Advanced)

1. Create a new `.md` file in `src/content/blog/`
2. Add frontmatter (the metadata between `---` marks)
3. Write content in Markdown format
4. Push to GitHub
5. Netlify auto-deploys

**Frontmatter template:**
```markdown
---
title: "Your Article Title Here"
description: "A 150-character description for SEO"
date: 2026-02-20
author: "AI Command Desk"
category: "AI Tools"
tags: ["tools", "productivity", "2026"]
featured: false
draft: false
---

Your article content starts here...

## First Section Heading

Your content...

## Second Section Heading

More content...
```

---

## 9. HOW TO UPDATE YOUR WEBSITE

### Automatic Updates (Blog Posts)

When you publish through Decap CMS or push to GitHub:
- Netlify detects the change automatically
- Rebuilds your site (1-2 minutes)
- Deploys the new version
- No action needed from you

### Manual Updates (Site Changes)

If you need Claude Code to make changes to the site:
1. Claude Code makes changes locally
2. Push changes to GitHub:
   ```bash
   cd "d:/Data-science/Claude/Blogging/aicommanddesk-site"
   git add .
   git commit -m "Description of changes"
   git push
   ```
3. Netlify auto-deploys within 2 minutes

---

## 10. TROUBLESHOOTING COMMON ISSUES

### Site Not Loading After Domain Change

**Cause:** DNS propagation can take up to 48 hours
**Fix:** Wait. Check again in a few hours. Use https://dnschecker.org to verify

### Decap CMS Not Loading

**Cause:** Identity or Git Gateway not configured
**Fix:**
1. Verify Netlify Identity is enabled
2. Verify Git Gateway is enabled
3. Make sure you accepted the invitation email
4. Try clearing browser cache and logging in again

### New Blog Post Not Appearing

**Cause:** Build may have failed or post is still in draft
**Fix:**
1. Check if `draft: false` in the post frontmatter
2. Check Netlify deploy logs for errors
3. Go to Netlify → Deploys → check if latest deploy succeeded

### Build Failed on Netlify

**Cause:** Code error in a recent change
**Fix:**
1. Go to Netlify → Deploys → click the failed deploy
2. Read the error log (scroll to the bottom for the error message)
3. Ask Claude Code to fix the issue based on the error

### Images Not Showing

**Cause:** Images not uploaded to correct folder
**Fix:** Upload images to `public/images/` folder and reference them as `/images/filename.jpg`

---

## 11. MONTHLY MAINTENANCE CHECKLIST

### Weekly Tasks
- [ ] Publish 2 blog posts
- [ ] Check Netlify for any failed deploys
- [ ] Monitor Google Analytics for traffic trends

### Monthly Tasks
- [ ] Review Google Search Console for errors
- [ ] Check for broken links on the site
- [ ] Update any outdated information in articles
- [ ] Back up your content (GitHub is already a backup)
- [ ] Review and respond to contact form submissions (Netlify → Forms)
- [ ] Check site speed at https://pagespeed.web.dev

### Quarterly Tasks
- [ ] Update the Resources page with new tools
- [ ] Review and update Privacy Policy if needed
- [ ] Audit all blog posts for outdated content
- [ ] Review affiliate links (make sure they still work)
- [ ] Check Netlify plan usage (bandwidth, build minutes)

### Annual Tasks
- [ ] Renew domain on GoDaddy
- [ ] Review overall site design (does it need a refresh?)
- [ ] Update copyright year in footer (automatic in code)

---

**End of Technical Deployment Guide**

*Keep this guide handy. Whenever you need to do something technical, refer to the relevant section. If something is unclear, ask Claude Code for help.*
