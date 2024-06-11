
import requests
import time
import os

# local import
from url_list import url_list

def download_file(url, senson_name):
    filename = url.split('/')[-1]
    filename = requests.utils.unquote(filename)  # Decode URL-encoded string to normal string

    # Create the senson folder if it does not exist
    os.makedirs(senson_name, exist_ok=True)

    # Concate senson folder and file name
    full_path = os.path.join(senson_name, filename)

    # Send a HTTP request to the server
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        # Get the total file size from headers
        total_size = int(r.headers.get('content-length', 0))
        # Initialize variables to track progress
        downloaded_size = 0

        # Open a local file for writing downloaded data
        with open(full_path, 'wb') as f:
            # Loop over the content incrementally
            for chunk in r.iter_content(chunk_size=8192):
                # Update the downloaded size
                downloaded_size += len(chunk)
                # Write the chunk to the local file
                f.write(chunk)
                # Calculate the percentage completed
                percent_completed = (downloaded_size / total_size) * 100
                # Print the progress
                print(f"\rDownloading {filename}: {percent_completed:.2f}%", end="")

    print()  # for new line after download completion
    return full_path

for senson_name, urls in url_list.items():
    print(f"Start Downloading folder: {senson_name}")
    for url in urls:
        print(f"Downloading {url}")
        filename = download_file(url, senson_name)
        print(f"Downloaded {filename}")
        time.sleep(10)

print("All files downloaded.")
