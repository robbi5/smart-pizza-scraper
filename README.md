Smart Pizza Scraper
-------------------

This small python script scrapes the pizza availability of a [Smart Pizza Machine by API Tech](https://www.apitech-solution.com/gb/en/smart-machines) into an sqlite database. Even if the company has _API_ in their name, sadly there isn't a hint for an public API endpoint - so I had to regress to MITM their new flutter based app again.

To use (with python>= 3.6):
```
pip install -r requirements.txt
cp .env.sample .env
# edit .env (to set MACHINE_ID)
python scrape.py

```

To get the MACHINE_ID, run `python3 machines.py <lat> <lon>`.