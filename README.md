# Scraper

Microservice for downloading images or text from web pages.
System supports data collection, eg. for machine learning.

### Environment

- docker-compose version 1.28.0
- Docker version 20.10.2

### Start app

```docker-compose up -d```

### Resources

*   POST ```/images```              - order downloading images from web page, providing a url
*   POST ```/content```             - order donloading text from web page, providing a url
*   GET  ```/status/{order_id}```   - check order status
*   GET  ```/download/{order_id}``` - download finished order

### Example usage

Order downloading:

```curl -d 'https://flask-restful.readthedocs.io/' -X POST localhost:3021/content```

Check status:

```curl localhost:3021/status/{order_id}```

Download:

```curl localhost:3021/status/{order_id}```

### Tests

```pytest test/test_scraper.py``` 

```python3 test/run_api_tests.py --url localhost:3021``` 
