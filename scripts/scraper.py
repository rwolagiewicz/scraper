from selenium import webdriver

class Scraper():
    def __init__(self, url):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(url)

    def get_img_urls(self):
        images = self.driver.find_elements_by_tag_name('img')
        img_urls = [image.get_attribute('src') for image in images]
        self.driver.close()
        return img_urls

    def get_content(self):
        el = self.driver.find_element_by_tag_name('body')
        content = el.text
        self.driver.close()
        return content
