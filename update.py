import urllib.request
import re

# --- Configuration ---
# Pointing to your new base file and the desired output file
BASE_PLAYLIST = "TV/base.m3u"
OUTPUT_PLAYLIST = "TV/new.m3u"

EXTERNAL_SOURCES = [
    {
        "url": "https://github.com/srhady/toffee-bd/raw/refs/heads/main/toffee_playlist.m3u",
        "group": "Toffee (NS Only)"
    },
    {
        "url": "https://github.com/ahan443/FAST-IPTV/raw/refs/heads/main/FIFA.m3u",
        "group": "FIFA"
    }
]
# ---------------------

def update_playlist():
    print("Reading base playlist...")
    try:
        with open(BASE_PLAYLIST, 'r', encoding='utf-8') as f:
            base_content = f.read().strip()
    except Exception as e:
        print(f"Error reading {BASE_PLAYLIST}: {e}")
        base_content = "#EXTM3U"

    merged_lines = []

    for source in EXTERNAL_SOURCES:
        url = source["url"]
        target_group = source["group"]
        print(f"Downloading: {target_group}...")
        
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                external_content = response.read().decode('utf-8')
        except Exception as e:
            print(f"Failed to download {url}: {e}")
            continue

        lines = external_content.splitlines()
        for line in lines:
            if line.strip().upper() == "#EXTM3U":
                continue
            
            if line.startswith("#EXTINF:"):
                if re.search(r'group-title="[^"]*"', line):
                    line = re.sub(r'group-title="[^"]*"', f'group-title="{target_group}"', line)
                else:
                    parts = line.split(',', 1)
                    if len(parts) == 2:
                        line = f'{parts[0]} group-title="{target_group}",{parts[1]}'
            
            merged_lines.append(line)

    print("Saving updated playlist...")
    with open(OUTPUT_PLAYLIST, 'w', encoding='utf-8') as f:
        f.write(base_content + "\n\n")
        f.write("\n".join(merged_lines) + "\n")
    print("Done!")

if __name__ == "__main__":
    update_playlist()
