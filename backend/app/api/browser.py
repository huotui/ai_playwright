from fastapi import APIRouter, Depends
from app.core.browser import BrowserManager
from app.core.playwright_mcp import PlaywrightMCP
from app.core.snapshot import SnapshotGenerator

router = APIRouter(prefix="/api/browser", tags=["浏览器控制"])

active_sessions = {}

@router.post("/session/{session_id}")
async def create_session(session_id: str):
    browser_manager = await BrowserManager.get_instance()
    page = await browser_manager.create_session(session_id)
    active_sessions[session_id] = True
    return {"message": f"会话 {session_id} 已创建", "session_id": session_id}

@router.delete("/session/{session_id}")
async def close_session(session_id: str):
    browser_manager = await BrowserManager.get_instance()
    await browser_manager.close_session(session_id)
    if session_id in active_sessions:
        del active_sessions[session_id]
    return {"message": f"会话 {session_id} 已关闭"}

@router.post("/session/{session_id}/navigate")
async def navigate(session_id: str, url: str):
    browser_manager = await BrowserManager.get_instance()
    page = await browser_manager.get_page(session_id)
    if not page:
        return {"error": "会话不存在"}
    
    mcp = PlaywrightMCP(page)
    result = await mcp.navigate_to_url(url)
    return result

@router.get("/session/{session_id}/snapshot")
async def get_snapshot(session_id: str):
    browser_manager = await BrowserManager.get_instance()
    page = await browser_manager.get_page(session_id)
    if not page:
        return {"error": "会话不存在"}
    
    mcp = PlaywrightMCP(page)
    return await mcp.get_snapshot()

@router.post("/session/{session_id}/action")
async def execute_action(session_id: str, action: str, parameters: dict):
    browser_manager = await BrowserManager.get_instance()
    page = await browser_manager.get_page(session_id)
    if not page:
        return {"error": "会话不存在"}
    
    mcp = PlaywrightMCP(page)
    return await mcp.execute_action(action, parameters)
