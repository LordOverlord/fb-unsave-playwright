# fb-unsave-playwright

**Purge your Facebook Saved items like a machine.**  
This script automates the process of removing all saved content from your [Facebook Saved](https://www.facebook.com/saved) page using [Playwright](https://playwright.dev). It is fast, precise, and requires no manual clicking.

## ⚙️ Features

- Automates clicking the "More" button and selecting **Unsave**
- Iterates through **all visible saved items**
- **Skips the global "More" button** in the page header
- Automatically **reloads the page** after processing visible items
- Designed for **Netscape-format cookies** (from browser extensions like *EditThisCookie*)
- Written in **Python + Playwright Async API**

---

## 🚀 Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/youruser/fb-unsave-playwright.git
cd fb-unsave-playwright
```

### 2. Install requirements

```bash
pip install -r requirements.txt
python -m playwright install
```

### 3. Export your Facebook cookies

- Use a browser extension like [EditThisCookie](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg)
- Export them in **Netscape format**
- Save the file as `cookies.facebook.txt` in the root of this repository

### 4. Run the script

```bash
python unsave.facebook.py
```

### 5. Repeat if needed

If you have thousands of saved items, the script may not complete the purge in one run.

Simply run it again to continue where it left off:

```bash
python unsave.facebook.py
```

> ℹ️ **Tip**: If you have thousands of saved items, the script may not complete the purge in one run.
> Simply run it again to continue from where it left off, or increase the `max_rounds` value in the code.

> 💡 **Note**: If the script stops working after a large number of saved items, make sure the `SAVED_URL` is set to `https://www.facebook.com/saved/?dashboard_section=ALL` instead of the default `referrer=...`. Facebook changes its internal routing dynamically.

## 🛠️ Advanced Usage
> 🔍 **PWSH Loop**: Use this one liner for pwsh, to run the script until all the saves are unsaved, or until something else happens.

```powershell
1..5 | ForEach-Object { Write-Host "🔁 Run #$_"; python .\unsave.facebook.py; Start-Sleep -Seconds 120 }
```

## ✅ Completed Tasks

### 🧠 Core Script
- [x] Functional Playwright script to unsave Facebook Saved items
- [x] Handles Netscape-format cookies (e.g., from EditThisCookie)
- [x] Ignores global "More" button (uses correct per-item menu)
- [x] Detects and clicks "Unsave" span
- [x] Uses round-based loop with `max_rounds`
- [x] Supports updated URL `?dashboard_section=ALL` for better loading
- [x] Script includes comments for easy understanding
- [x] No infinite loops (softban protection)
- [x] Compatible with PowerShell via one-liner loop

### 📦 Packaging & Documentation
- [x] Clean `requirements.txt`
- [x] `.gitignore` excludes cookies, virtualenvs, and system files
- [x] BSD 3-Clause LICENSE with author attribution
- [x] `README.md` with:
  - Quick start guide
  - Advanced tip (repeat if needed)
  - Disclaimer with softban warning
  - URL correction note

### 🚀 Repo & Testing
- [x] GitHub repository created: `fb-unsave-playwright`
- [x] Initial commit and push completed
- [x] Markdown formatting verified visually

---

## 🔜 Pending / Future Tasks

### 🧪 Testing
- [ ] Script tested in fresh virtual environment
- [ ] Tested on Windows 10 and Linux (Ubuntu)

### 🐳 Dockerization (optional)
- [ ] Create `Dockerfile`
- [ ] Create `.dockerignore`
- [ ] Add Docker usage instructions to README

### 🔧 Script Improvements
- [ ] Logging to `.log` file per run (e.g., `unsave.log`)
- [ ] Cumulative unsave counter (persisted across runs)
- [ ] CLI toggle for headless mode (`--headless`)
- [ ] Filtering by item type (e.g., reel, post, video)
- [ ] Dry-run mode: detect items that would be unsaved without clicking


## 🔐 Disclaimer

> 🧠 After fully purging 5000+ items, Facebook's Saved feed may enter a soft-corrupted state where the frontend can't recover. These issues tend to resolve automatically after internal cleanup (may take days or weeks).


- This script interacts with your Facebook account using your cookies.
- Use responsibly. No data is stored or transmitted externally.
- Facebook’s layout may change and break selectors — if that happens, feel free to open an issue or contribute a fix.
- While unlikely, running the script too aggressively or without delays may trigger **temporary rate limits or softbans** from Facebook. Use with moderation.



## License

This project is licensed under the BSD 3-Clause License.
Attribution required — if you reuse or modify this project, please credit the original author: [@overlordco](https://github.com/overlordco)
