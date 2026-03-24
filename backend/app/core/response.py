from typing import Any

def success_response(data: Any) -> dict:
    return {"success": True, "data": data, "error": None}

def error_response(code: str, message: str) -> dict:
    return {"success": False, "data": None, "error": { "code": code, "message": message }}