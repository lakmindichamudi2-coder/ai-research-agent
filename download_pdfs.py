import os
import requests

pdf_urls = [
    "https://arxiv.org/pdf/1706.03762.pdf",
    "https://arxiv.org/pdf/2005.11401.pdf",
    "https://arxiv.org/pdf/2210.03629.pdf",
    "https://arxiv.org/pdf/2201.11903.pdf",
    "https://arxiv.org/pdf/2305.10601.pdf",
    "https://arxiv.org/pdf/2304.03442.pdf",
    "https://arxiv.org/pdf/2308.08155.pdf",
    "https://arxiv.org/pdf/2308.11432.pdf",
    "https://arxiv.org/pdf/2310.11511.pdf",
    "https://arxiv.org/pdf/2401.15884.pdf",
    "https://arxiv.org/pdf/2401.08406.pdf",
    "https://arxiv.org/pdf/2306.13549.pdf",
    "https://arxiv.org/pdf/1512.03385.pdf",
    "https://arxiv.org/pdf/2305.09972.pdf",
    "https://arxiv.org/pdf/2304.09110.pdf",
    "https://arxiv.org/pdf/2308.03688.pdf",
    "https://arxiv.org/pdf/2402.04253.pdf",
    "https://arxiv.org/pdf/2310.11703.pdf",
    "https://arxiv.org/pdf/2302.11382.pdf",
    "https://arxiv.org/pdf/2203.08155.pdf"
]

os.makedirs("./docs", exist_ok=True)

print("Starting Auto-Download...")
for i, url in enumerate(pdf_urls, 1):
    file_path = f"./docs/paper_{i}.pdf"
    print(f"Downloading [{i}/20]: {url}")
    response = requests.get(url)
    with open(file_path, "wb") as f:
        f.write(response.content)

print("Done downloading all PDFs!")