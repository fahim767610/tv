import urllib.request
import re
import os

# The source playlists and your desired group names
SOURCES = [
    {"url": "https://github.com/fahim767610/tv/raw/refs/heads/main/base.m3u", "group": None},
    {"url": "https://github.com/ahan443/FAST-IPTV/raw/refs/heads/main/FIFA.m3u", "group": "FIFA"},
    {"url": "https://github.com/srhady/toffee-bd/raw/refs/heads/main/toffee_playlist.m3u", "group": "Toffee (NS Only)"}
]

def process_m3u(url, target_group):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8')
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return ""
    
    lines = content.splitlines()
    output = []
    
    for line in lines:
        # Skip empty lines and the duplicate #EXTM3U headers
        if not line.strip() or line.upper().startswith('#EXTM3U'):
            continue
            
        if line.upper().startswith('#EXTINF:'):
            if target_group:
                # If group-title exists, replace it
                if 'group-title="' in line:
                    line = re.sub(r'group-title="[^"]*"', f'group-title="{target_group}"', line)
                else:
                    # If it doesn't exist, insert it right before the channel name comma
                    parts = line.rsplit(',', 1)
                    if len(parts) == 2:
                        line = f'{parts[0]} group-title="{target_group}",{parts[1]}'
        
        output.append(line)
        
    return '\n'.join(output)

def main():
    # Ensure TV directory exists
    os.makedirs('TV', exist_ok=True)
    
    final_content = ["#EXTM3U"]
    
    for source in SOURCES:
        print(f"Processing {source['url']}...")
        processed = process_m3u(source['url'], source['group'])
        if processed:
            final_content.append(processed)
    
    # Save the combined file
    with open('TV/new.m3u', 'w', encoding='utf-8') as f:
        f.write('\n'.join(final_content))
        
    print("Successfully updated TV/new.m3u")

if __name__ == '__main__':
    main()
