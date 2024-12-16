import os
import time
import urllib2
import socket
import xbmc
import xbmcgui

# Define custom headers
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Accept': '*/*',
    'Connection': 'keep-alive'
}

# Function to test download speed
def test_download_speed(dialog):
    url = "https://github.com/BitDoctor/speed-test-file/raw/refs/heads/master/10mb.txt"  # Test file
    request = urllib2.Request(url, headers=HEADERS)
    
    # Open request
    response = urllib2.urlopen(request)
    file_size = int(response.headers['Content-Length'])  # File size in bytes
    block_size = 8192  # Read in 8KB chunks
    downloaded_size = 0
    start_time = time.time()

    # Read data in chunks to simulate real-time download and update progress
    while True:
        chunk = response.read(block_size)
        if not chunk:
            break

        downloaded_size += len(chunk)
        elapsed_time = time.time() - start_time
        if elapsed_time > 0:
            speed_kbps = (downloaded_size / elapsed_time) / 1024  # Convert to Kbps
            progress = int((downloaded_size / float(file_size)) * 100)
            dialog.update(progress, 
                          "Testing Download Speed...",
                          "Speed: {:.2f} Kbps".format(speed_kbps),
                          "Progress: {}%".format(progress))
    
        if dialog.iscanceled():
            return None  # Allow user to cancel

    # Calculate final download speed in Mbps
    end_time = time.time()
    total_time = end_time - start_time
    download_speed_mbps = (file_size * 8) / (total_time * 1024 * 1024)  # Convert to Mbps

    return download_speed_mbps

# Function to test latency (ping)
def test_ping(dialog):
    dialog.update(0, "Testing Ping...")
    target = "8.8.8.8"  # Google DNS
    port = 53  # Use port 53 for DNS
    start_time = time.time()

    try:
        # Test connection
        socket.create_connection((target, port), timeout=2)
        end_time = time.time()
        ping = (end_time - start_time) * 1000  # Convert to ms
        return ping
    except socket.error:
        return None

# Main function to run the speed test
def run_speed_test():
    dialog = xbmcgui.DialogProgress()
    dialog.create("Speed Test", "Starting the speed test... Please wait.")

    try:
        # Test download speed
        download_speed = test_download_speed(dialog)
        if download_speed is None:
            dialog.close()
            xbmcgui.Dialog().ok("Speed Test Canceled", "The speed test was canceled.")
            return

        # Test ping
        ping = test_ping(dialog)

        # Format results
        download_speed_text = "Download Speed: {:.2f} Mbps".format(download_speed)
        ping_text = "Ping: {:.2f} ms".format(ping if ping is not None else 0)

        # Show final results
        dialog.close()
        xbmcgui.Dialog().ok("Speed Test Results", download_speed_text, ping_text)

    finally:
        dialog.close()

if __name__ == '__main__':
    run_speed_test()
