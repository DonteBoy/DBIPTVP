import requests
import threading

class ChannelChecker:
    def __init__(self, playlist_file):
        self.playlist_file = playlist_file
        self.urls_to_check = self.extract_urls()

    def extract_urls(self):
        urls = []
        with open(self.playlist_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith('http'):
                    urls.append(line.strip())
        return urls

    def check_channel(self, url):
        try:
            response = requests.get(url, timeout=3)
            if response.status_code != 200:
                return False
        except requests.exceptions.RequestException:
            return False
        return True

    def remove_bad_channels(self):
        removed_count = 0
        for url in self.urls_to_check[1:]:  # Skip the first line
            if not self.check_channel(url):
                with open(self.playlist_file, 'r') as f:
                    lines = f.readlines()
                with open(self.playlist_file, 'w') as f:
                    for line in lines:
                        if line.strip() == url:
                            removed_count += 1
                        else:
                            f.write(line)
        return removed_count

    def check_channels_and_report(self):
        removed_count = self.remove_bad_channels()
        total_count = len(self.urls_to_check) - 1  # Total count excluding the first line
        print(f"Checked {total_count} channels. Removed {removed_count} bad channels.")

    def start(self):
        self.check_channels_and_report()

if __name__ == "__main__":
    playlist_file = "1.m3u"  # Replace with your playlist file
    checker = ChannelChecker(playlist_file)
    checker.start()





# DBIPTVP