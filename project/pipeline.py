import requests
import os


urls = [
    "https://www.bls.gov/cps/cpsaat03.xlsx",
    "https://www.bls.gov/cps/aa2022/cpsaat03.xlsx",
    "https://www.bls.gov/cps/aa2021/cpsaat03.xlsx",
    "https://www.bls.gov/cps/aa2020/cpsaat03.xlsx"
]

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

for i, url in enumerate(urls, start=1):
    file_path = os.path.join("./data", f"dataset_{i}.xlsx")
    if not os.path.exists(file_path):
        print(f"Downloading {url} as {file_path}...")
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded {file_path} successfully.")
        else:
            print(f"Failed to download {file_path}. HTTP Status: {response.status_code}")
    else:
        print(f"{file_path} already exists locally.")
