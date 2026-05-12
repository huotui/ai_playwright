from typing import Dict, Any, Optional, List
from openai import OpenAI
from app.config import settings
import json
import time

class AITestAgent:
    
    SYSTEM_PROMPT = """你是一个专业的自动化测试工程师。你的任务是根据用户的自然语言测试指令，使用 Playwright MCP 工具执行 Web 自动化测试。

当前页面快照：
{snapshot}

用户的测试目标：
{instruction}

请分析当前页面，决定下一步操作，并调用相应的 MCP 工具。

可选工具及参数：
- navigate_to_url: {{"url": "string"}} - 导航到指定URL
- click_element: {{"selector": "string"}} - 点击页面元素
- fill_input: {{"selector": "string", "text": "string"}} - 填写输入框
- get_text_content: {{"selector": "string"}} - 获取元素文本
- get_page_title: {{}} - 获取页面标题
- get_page_url: {{}} - 获取当前URL
- wait_for_selector: {{"selector": "string"}} - 等待元素出现
- take_screenshot: {{}} - 截图
- press_key: {{"key": "string"}} - 按键操作
- execute_javascript: {{"script": "string"}} - 执行JS代码

返回严格的 JSON 格式：
{{
  "action": "工具名称",
  "parameters": {{}},
  "reasoning": "决策理由",
  "completed": false,
  "result": "测试结果描述（仅在completed为true时填写）"
}}

重要提示：
1. 使用稳健的选择器策略：优先使用role选择器或可见文本
2. 每次操作后检查页面状态是否变化
3. 如果遇到错误，尝试不同的选择器或等待后重试
4. 测试完成后，设置completed为true并提供最终测试结果
"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.OPENAI_API_KEY
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=settings.OPENAI_API_BASE
        )
        self.model = settings.OPENAI_MODEL
        self.max_iterations = 30

    def execute_test(self, instruction: str, mcp) -> Dict[str, Any]:
        logs = []
        screenshots = []
        iteration = 0
        
        snapshot = mcp.get_snapshot()
        snapshot_text = json.dumps(snapshot, ensure_ascii=False)
        
        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT.format(
                snapshot=snapshot_text,
                instruction=instruction
            )},
        ]
        
        while iteration < self.max_iterations:
            iteration += 1
            logs.append(f"迭代 {iteration}: AI 正在分析页面并决策下一步操作...")
            
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0,
                    max_tokens=1000
                )
                
                content = response.choices[0].message.content
                
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0].strip()
                
                action_data = json.loads(content)
                
                action = action_data.get("action")
                parameters = action_data.get("parameters", {})
                reasoning = action_data.get("reasoning", "")
                completed = action_data.get("completed", False)
                result = action_data.get("result", "")
                
                logs.append(f"AI决策: {reasoning}")
                logs.append(f"执行操作: {action} with {json.dumps(parameters, ensure_ascii=False)}")
                
                if completed:
                    logs.append(f"测试完成: {result}")
                    return {
                        "success": True,
                        "result": result,
                        "logs": logs,
                        "screenshots": screenshots,
                        "iterations": iteration
                    }
                
                action_result = mcp.execute_action(action, parameters)
                
                if action_result.get("success"):
                    logs.append(f"操作成功: {json.dumps(action_result, ensure_ascii=False)}")
                else:
                    error_msg = action_result.get("error", "未知错误")
                    logs.append(f"操作失败: {error_msg}")
                    action_data["error"] = error_msg
                
                messages.append({"role": "assistant", "content": content})
                messages.append({
                    "role": "user", 
                    "content": f"操作执行结果: {json.dumps(action_result, ensure_ascii=False)}"
                })
                
                new_snapshot = mcp.get_snapshot()
                messages.append({
                    "role": "user",
                    "content": f"新页面快照: {json.dumps(new_snapshot, ensure_ascii=False)}"
                })
                
                if iteration % 5 == 0:
                    screenshot = mcp.take_screenshot(full_page=True)
                    screenshots.append(screenshot.get("screenshot"))
                    logs.append("截图已保存")
                
                time.sleep(1)
                
            except Exception as e:
                error_msg = f"AI 调用失败: {str(e)}"
                logs.append(error_msg)
                return {
                    "success": False,
                    "result": error_msg,
                    "logs": logs,
                    "screenshots": screenshots,
                    "iterations": iteration
                }
        
        return {
            "success": False,
            "result": "测试超时：达到最大迭代次数",
            "logs": logs,
            "screenshots": screenshots,
            "iterations": iteration
        }
