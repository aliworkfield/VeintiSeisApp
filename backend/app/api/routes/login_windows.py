from fastapi import APIRouter, Request, HTTPException

router = APIRouter()

@router.get("/windows")
def login_with_windows(request: Request):
    """
    Read Windows-authenticated username forwarded by IIS.
    Example header:
        X-Forwarded-User: 'DOMAIN\\username'
    """
    user = request.headers.get("X-Forwarded-User")

    if not user:
        raise HTTPException(status_code=401, detail="Missing Windows authentication header.")

    return {
        "authenticated": True,
        "windows_user": user
    }