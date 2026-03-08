import requests
import tarfile
import os
from tqdm import tqdm

url = "https://www.cs.cmu.edu/~enron/enron_mail_20150507.tar.gz"
filename = "enron_mail.tar.gz"

if not os.path.exists("data/enron"):
    os.makedirs("data/enron")

    print("Downloading Enron dataset...")
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))

    with open(f"data/{filename}", 'wb') as f, tqdm(
        desc=filename,
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            size = f.write(data)
            bar.update(size)

    print("Extracting...")
    with tarfile.open(f"data/{filename}", 'r:gz') as tar:
        tar.extractall("data/enron")

    print("Dataset downloaded and extracted to data/enron/")