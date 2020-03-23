# EtsyAnalyzer
This program downloads shop listings from Etsy and computes the most relevant terms for each shop.

It has been tested with Python 3.6.9 and 3.7.4 only.

To ensure you have necessary packages installed run
```
pip install -U -r requirements.txt
```

You can run the program with
```
python main.py --api_key <API-KEY>
```
where `API-KEY` is your Etsy developer API key.

You can run the test with
```
python test_relevance.py
```

Note: You may need to substitute `pip3` for `pip` and `python3` for `python` on some systems.
