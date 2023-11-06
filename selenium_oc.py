import time
import random
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import List


class SeleniumOC:
    # Unified use of CSS SELECTOR for locators
    # Get Chromedriver at https://googlechromelabs.github.io/chrome-for-testing/

    def __init__(self, driver):
        self.driver = driver

    def _get_element_by_text(self, css_selector: str, by_text: str):
        elements = self.driver.find_elements(By.CSS_SELECTOR, css_selector)
        text_list = [e.text if e else '' for e in elements]

        for i, _text in enumerate(text_list):
            if _text == by_text:
                return elements[i]
        return None

    def _get_text_with_multiple(self, css_selector, multiple: bool = True):
        if multiple:
            elems = self.get_elements(css_selector, multiple=True)
            return [elem.text for elem in elems]
        return self.get_elements(css_selector).text

    def _get_attr_with_multiple(self, css_selector, attr, multiple: bool = True):
        if multiple:
            elems = self.get_elements(css_selector, multiple=True)
            return [elem.get_attribute(attr) for elem in elems]
        return self.get_elements(css_selector).get_attribute(attr)

    def _scroll_and_input(self, css_selector: str, send_keys: str):
        element = self.get_elements(css_selector)
        self.scroll_to_element(element)
        element.send_keys(send_keys)

    def open(self, url: str):
        self.driver.get(url)

    def close(self):
        self.driver.quit()

    def hard_delay(self, sleep_time: int = 0):
        if sleep_time:
            time.sleep(sleep_time)
            return
        time.sleep(random.randint(2, 5))

    def get_url(self):
        return self.driver.current_url

    def get_handle_title(self):
        return self.driver.title

    def scroll_to_element(self, element: WebElement):
        location_y = element.location['y'] - 130
        location_y = 0 if location_y < 0 else location_y
        self.driver.execute_script(f"window.scrollTo(0, {str(location_y)})")

    def get_elements(self, css_selector: str, multiple: bool = False, by_text: str = ""):
        if multiple:
            return self.driver.find_elements(By.CSS_SELECTOR, css_selector)
        if by_text:
            return self._get_element_by_text(css_selector, by_text)
        return self.driver.find_element(By.CSS_SELECTOR, css_selector)

    def must_get_element(self, css_selector: str, time_out: int = 30):
        # Wait for an element (default wait time is 30s) if the timeout is exceeded, the program terminates.

        return WebDriverWait(self.driver, timeout=time_out).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)),
            message=f"[E] expected element not found: {css_selector}",
        )

    def must_get_text(self, css_selector: str, text: str, time_out: int = 30):
        # Wait for the text of the element (default wait time is 30 seconds), if the timeout is exceeded, the program will terminate.

        return WebDriverWait(self.driver, timeout=time_out).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, css_selector), text),
            message=f"[E] expected text not found: {text}",
        )

    def must_no_element(self, css_selector: str, time_out: int = 30):
        return WebDriverWait(self.driver, timeout=time_out).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, css_selector)),
            message=f"[E] expected elements remain: {css_selector}",
        )

    def get_text(self, css_selector: str | List[str], multiple: bool = False):
        # Allow passing single or multiple css selectors

        # The multiple defaults to False, which means that we will target the first matching element for each css selector
        # If set the multiple to True it will match all matching elements of each css selector.

        if isinstance(css_selector, list):
            result = []
            for i in css_selector:
                _text = self._get_text_with_multiple(i, multiple)
                result.append(_text) if _text else result.append("")
            return result
        return self._get_text_with_multiple(css_selector, multiple)

    def get_attrs(self, css_selector: str | List[str], attr: str, multiple: bool = False):
        # Allow passing single or multiple css selectors

        # The multiple defaults to False, which means that we will target the first matching element for each css selector
        # If set the multiple to True it will match all matching elements of each css selector.

        if isinstance(css_selector, list):
            result = []
            for i in css_selector:
                _attr = self._get_attr_with_multiple(i, attr, multiple)
                result.append(_attr) if _attr else result.append("")
            return result
        return self._get_attr_with_multiple(css_selector, attr, multiple)

    def scroll_and_click(self, css_selector: str, by_text: str = ""):
        element = self.get_elements(css_selector, by_text=by_text)
        if not element:
            print(f"[W] element is not localized, check the: {css_selector}")
            print(f"[W] by_text: {by_text}")
            return False

        self.scroll_to_element(element)
        element.click()
        return True

    def scroll_and_input(self, css_selector: str | List[str], send_keys: str | List[str]):
        if isinstance(css_selector, str) and isinstance(send_keys, str):
            self._scroll_and_input(css_selector, send_keys)
            return True
        if isinstance(css_selector, list) and isinstance(send_keys, list):
            for i in range(len(css_selector)):
                self._scroll_and_input(css_selector[i], send_keys[i])
            return True
        return False

    def switch_window_and_execute(self, handle_index, fun, back: bool = True, **kwargs):
        # 1. Switch windows
        # 2. Execute function
        # 3. Return to the first window

        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[handle_index])
        result = fun(**kwargs)
        if back:
            self.driver.switch_to.window(handles[handle_index])
        return result

    def save_html_to_local(self, pth: str):
        _html = self.driver.page_source
        with open(pth, "w", encoding="utf-8") as f:
            f.write(_html)
