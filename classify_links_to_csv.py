import csv
import glob
import os

# Busca el primer archivo que coincida con el patrón
INPUT_PATTERN = "facebook_saved_links_*.txt"
OUTPUT_FILE = "facebook_links_categorized.csv"

KEYWORDS = {
    "reel": "reel",
    "video": "videos",
    "profile": "profile"
}

def classify_link(link):
    for category, keyword in KEYWORDS.items():
        if keyword in link.lower():
            return category
    return "uncategorized"

def main():
    files = glob.glob(INPUT_PATTERN)
    if not files:
        print(f"❌ No se encontró ningún archivo con patrón {INPUT_PATTERN}")
        return

    input_file = files[0]
    print(f"📂 Usando archivo: {input_file}")

    links = []
    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            link = line.strip()
            if link:
                category = classify_link(link)
                links.append({"link": link, "categoria": category})

    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["link", "categoria"])
        writer.writeheader()
        writer.writerows(links)

    print(f"✅ CSV generado: {OUTPUT_FILE} ({len(links)} enlaces clasificados)")

if __name__ == "__main__":
    main()
