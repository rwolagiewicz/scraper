import os
import pytest
from os import path
import sys
sys.path.append(".")
from scripts.scraper import Scraper
resources_dir = path.join(os.getcwd(), 'test/resources')


@pytest.mark.parametrize("html_file, result_file", (
    ('yahoo.html', 'yahoo_content'),
    ('google.html', 'google_content'),
))
def test_content(html_file, result_file):
    html_path = path.join(resources_dir, html_file)
    with open(path.join(resources_dir, result_file)) as f:
        assert Scraper('file://' + html_path).get_content() == f.read()

@pytest.mark.parametrize("html_file, result_file", (
    ('yahoo.html', 'yahoo_urls'),
    ('google.html', 'google_urls'),
))
def test_get_urls(html_file, result_file):
    html_path = path.join(resources_dir, html_file)
    urls = Scraper('file://' + html_path).get_img_urls()
    with open(path.join(resources_dir, result_file)) as f:
        assert '\n'.join(urls) == f.read()
