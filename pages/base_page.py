class BasePage:
    def __init__(self, page):
        self.page = page
    def navigate(self, url):
        self.page.goto(url)

    def click(self, selector):
        self.page.click(selector)

    def fill(self, selector, text):
        self.page.fill(selector, text)

    def get_input_value(self, selector):
        return self.page.input_value(selector)

    def is_text_visible(self, text):
        return self.page.is_visible(f"text={text}")
    