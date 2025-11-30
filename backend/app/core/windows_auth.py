import os
import getpass
from typing import Tuple

try:
    import win32api
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False

try:
    import ldap3
    LDAP3_AVAILABLE = True
except ImportError:
    LDAP3_AVAILABLE = False

def get_windows_user(request) -> Tuple[str, str]:
    """
    Returns Windows username using:
    1. X-Forwarded-User header (IIS)
    2. os.getlogin()
    3. getpass.getuser()
    4. win32api.GetUserName()
    
    Returns:
        Tuple[str, str]: (username, auth_mode)
    """
    # 1. IIS mode (if header exists)
    iis_user = request.headers.get("X-Forwarded-User")
    if iis_user:
        return iis_user, "iis"

    # 2. Local native mode
    try:
        return os.getlogin(), "native"
    except:
        pass

    try:
        return getpass.getuser(), "native"
    except:
        pass

    if WIN32_AVAILABLE:
        try:
            return win32api.GetUserName(), "native"
        except:
            pass

    return None, "unknown"

def get_user_details(username: str) -> dict:
    """
    If ldap3 is installed and domain is joined, return:
    - full name
    - domain groups
    - email (if available)
    """
    details = {
        "full_name": username,
        "groups": [],
        "email": None
    }
    
    if not LDAP3_AVAILABLE:
        return details
        
    # TODO: Implement LDAP lookup for domain joined machines
    # This would require domain controller information and proper authentication
    # For now, we'll return the basic information
    
    return details