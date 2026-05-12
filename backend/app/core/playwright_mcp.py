from typing import Dict, Any, Optional, List
from playwright.sync_api import Page
from app.core.snapshot import SnapshotGenerator
import json
import time

class PlaywrightMCP:
    def __init__(self, page: Page):
        self.page = page
    
    def navigate_to_url(self, url: str) -> Dict[str, Any]:
        self.page.goto(url, wait_until='networkidle', timeout=30000)
        return self._get_current_state()
    
    def click_element(self, selector: str) -> Dict[str, Any]:
        self.page.click(selector, timeout=10000)
        self.page.wait_for_load_state('networkidle')
        return self._get_current_state()
    
    def fill_input(self, selector: str, text: str) -> Dict[str, Any]:
        self.page.fill(selector, text, timeout=10000)
        return self._get_current_state()
    
    def press_key(self, key: str) -> Dict[str, Any]:
        self.page.keyboard.press(key)
        return self._get_current_state()
    
    def select_option(self, selector: str, value: str) -> Dict[str, Any]:
        self.page.select_option(selector, value=value, timeout=10000)
        return self._get_current_state()
    
    def get_text_content(self, selector: str) -> Dict[str, Any]:
        text = self.page.text_content(selector, timeout=10000)
        return {"text": text, "selector": selector}
    
    def get_element_attribute(self, selector: str, attribute: str) -> Dict[str, Any]:
        value = self.page.get_attribute(selector, attribute, timeout=10000)
        return {"attribute": attribute, "value": value, "selector": selector}
    
    def get_page_title(self) -> Dict[str, Any]:
        return {"title": self.page.title()}
    
    def get_page_url(self) -> Dict[str, Any]:
        return {"url": self.page.url}
    
    def wait_for_selector(self, selector: str, timeout: int = 10000) -> Dict[str, Any]:
        self.page.wait_for_selector(selector, timeout=timeout)
        return self._get_current_state()
    
    def double_click_element(self, selector: str) -> Dict[str, Any]:
        self.page.dblclick(selector, timeout=10000)
        return self._get_current_state()
    
    def take_screenshot(self, full_page: bool = True) -> Dict[str, Any]:
        screenshot_base64 = SnapshotGenerator.take_screenshot(self.page, full_page)
        return {"screenshot": screenshot_base64, "full_page": full_page}
    
    def execute_javascript(self, script: str) -> Dict[str, Any]:
        result = self.page.evaluate(script)
        return {"result": result}
    
    def get_snapshot(self) -> Dict[str, Any]:
        return SnapshotGenerator.generate(self.page)
    
    def _get_current_state(self) -> Dict[str, Any]:
        return {
            "url": self.page.url,
            "title": self.page.title(),
            "success": True
        }
    
    def execute_action(self, action: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        action_map = {
            "navigate_to_url": self.navigate_to_url,
            "click_element": self.click_element,
            "fill_input": self.fill_input,
            "press_key": self.press_key,
            "select_option": self.select_option,
            "get_text_content": self.get_text_content,
            "get_element_attribute": self.get_element_attribute,
            "get_page_title": self.get_page_title,
            "get_page_url": self.get_page_url,
            "wait_for_selector": self.wait_for_selector,
            "double_click_element": self.double_click_element,
            "take_screenshot": self.take_screenshot,
            "execute_javascript": self.execute_javascript,
            "get_snapshot": self.get_snapshot,
        }
        
        if action not in action_map:
            return {"error": f"Unknown action: {action}", "success": False}
        
        try:
            result = action_map[action](**parameters)
            if "success" not in result:
                result["success"] = True
            return result
        except Exception as e:
            return {"success": False, "error": str(e)}
