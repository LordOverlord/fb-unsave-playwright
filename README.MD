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



## 🔐 Disclaimer

- This script interacts with your Facebook account using your cookies.
- Use responsibly. No data is stored or transmitted externally.
- Facebook’s layout may change and break selectors — if that happens, feel free to open an issue or contribute a fix.
- While unlikely, running the script too aggressively or without delays may trigger **temporary rate limits or softbans** from Facebook. Use with moderation.



## License

This project is licensed under the BSD 3-Clause License.
Attribution required — if you reuse or modify this project, please credit the original author: [@overlordco](https://github.com/overlordco)
