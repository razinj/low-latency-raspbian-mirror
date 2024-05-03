# Low Latency Raspbian Mirror Finder

Scraping [Raspbian mirrors](https://www.raspbian.org/RaspbianMirrors) using [Scrapy](https://scrapy.org/) for domains and then pinging them using `subprocess` to find the top results.

Create and activate a local env:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Scrape domains:

```bash
cd raspbian_mirrors
scrapy crawl mirrors -o urls.jsonl
```

Ping and display top results:

```bash
cd .. # Go back to main folder
python script.py
```

---

Lint:

```bash
pylint script.py raspbian_mirrors/raspbian_mirrors/spiders/mirrors.py
```

Format:

```bash
black .
```
