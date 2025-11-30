from fastapi import Request, HTTPException

def get_windows_user(request: Request):
    user = getattr(request.state, "windows_user", None)
    if not user:
        raise HTTPException(status_code=401, detail="Windows user not authenticated.")
    return user