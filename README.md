# Scraper

Scraper downloading images or text from web pages.

### Environment

- docker-compose version 1.28.0
- Docker version 20.10.2

### Start app

```docker compose up -d```

### Tests

```pytest test/test_scraper.py``` 

```python3 test/run_api_tests.py --url localhost:3021``` 


### comment for FeedbackSemantive:
The solution has been automated and Docker containered.

Architecture allows to accept large numbers of URLs,
which maker is processing one by one.

Number of makers might be increased in order to speed up processing.

Api tests could be more detailed.
