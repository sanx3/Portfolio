# Sanjith Punnose – Portfolio Website

A cinematic portfolio with **auto-updating filmography** from IMDb.

---

## 🚀 Setup Guide (One Time – 10 mins)

### Step 1 — Create a GitHub Account
Go to [github.com](https://github.com) and sign up for free.

### Step 2 — Create a New Repository
1. Click **"New"** repository
2. Name it: `sanjithpunnose` (or anything you like)
3. Set it to **Public**
4. Click **Create repository**

### Step 3 — Upload These Files
Upload all files from this folder to your repository:
- `index.html`
- `films.json`
- `scraper/fetch_imdb.py`
- `.github/workflows/update-films.yml`

### Step 4 — Enable GitHub Pages
1. Go to your repository **Settings**
2. Click **Pages** in the left sidebar
3. Under **Source**, select **Deploy from a branch**
4. Select **main** branch → **/ (root)**
5. Click **Save**

✅ Your site will be live at:
`https://YOUR-USERNAME.github.io/sanjithpunnose`

---

## 🔄 How Auto-Update Works

Every day at **6:00 AM UTC (11:30 AM IST)**, GitHub automatically:
1. Runs `scraper/fetch_imdb.py`
2. Fetches your latest credits from IMDb
3. Updates `films.json`
4. Your portfolio reflects the new films instantly

You can also trigger it manually:
- Go to **Actions** tab in GitHub
- Click **Auto-Update IMDb Films**
- Click **Run workflow**

---

## ✏️ Customising Your Portfolio

### Update Director / Music Director info
Open `films.json` and edit the `dir` and `music` fields for any film.

### Add a film manually
Add a new entry to `films.json`:
```json
{
  "year": 2026,
  "title": "New Movie Title",
  "lang": "Malayalam",
  "dir": "Director Name",
  "music": "Music Director Name"
}
```

---

## 📞 Contact
- IMDb: https://www.imdb.com/name/nm15360041/
- Instagram: https://www.instagram.com/sanjithpunnose/
- WhatsApp: +91 70341 37352
