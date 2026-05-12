from typing import Dict, Any, List
from playwright.sync_api import Page
import base64

class SnapshotGenerator:
    
    @staticmethod
    def generate(page: Page) -> Dict[str, Any]:
        dom_snapshot = SnapshotGenerator._generate_accessible_dom(page)
        
        return {
            "url": page.url,
            "title": page.title(),
            "dom_snapshot": dom_snapshot,
        }

    @staticmethod
    def _generate_accessible_dom(page: Page) -> str:
        script = """
        function generateSnapshot(element, depth) {
            if (!element) return '';
            
            var skipTags = ['SCRIPT', 'STYLE', 'NOSCRIPT', 'META', 'LINK', 'HEAD'];
            var ariaRoles = ['button', 'textbox', 'checkbox', 'radio', 'combobox', 
                           'listbox', 'menu', 'tab', 'dialog', 'alert', 'form'];
            
            var result = '';
            var indent = '';
            for (var i = 0; i < depth; i++) indent += '  ';
            var tag = element.tagName ? element.tagName.toLowerCase() : '';
            
            if (skipTags.indexOf(tag) !== -1) return '';
            if (element.offsetParent === null && tag !== 'body') return '';
            
            var role = element.getAttribute('role') || '';
            var ariaLabel = element.getAttribute('aria-label') || '';
            var name = element.getAttribute('name') || '';
            var id = element.getAttribute('id') || '';
            var placeholder = element.getAttribute('placeholder') || '';
            var type = element.getAttribute('type') || '';
            var value = element.value || '';
            var href = element.href || '';
            var src = element.src || '';
            var alt = element.alt || '';
            
            var attrs = [];
            if (id) attrs.push('id=\"' + id + '\"');
            if (role && ariaRoles.indexOf(role) !== -1) attrs.push('role=\"' + role + '\"');
            if (ariaLabel) attrs.push('aria-label=\"' + ariaLabel + '\"');
            if (placeholder) attrs.push('placeholder=\"' + placeholder + '\"');
            if (type && tag === 'input') attrs.push('type=\"' + type + '\"');
            if (value && tag === 'input') attrs.push('value=\"' + value + '\"');
            
            var openingTag = indent + '<' + tag + (attrs.length ? ' ' + attrs.join(' ') : '') + '>';
            
            var text = '';
            if (element.childNodes.length === 1 && element.childNodes[0].nodeType === Node.TEXT_NODE) {
                text = element.textContent.trim();
            }
            
            if (text) {
                openingTag += text;
            }
            
            result += openingTag + '\n';
            
            if (element.children) {
                for (var j = 0; j < element.children.length; j++) {
                    result += generateSnapshot(element.children[j], depth + 1);
                }
            }
            
            return result;
        }
        generateSnapshot(document.body, 0);
        """
        
        try:
            dom = page.evaluate(script)
            return dom if dom else ""
        except Exception as e:
            return f"<error: {str(e)}>"

    @staticmethod
    def take_screenshot(page: Page, full_page: bool = True) -> str:
        screenshot_bytes = page.screenshot(full_page=full_page)
        return base64.b64encode(screenshot_bytes).decode('utf-8')
