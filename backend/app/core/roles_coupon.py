from typing import List, Union
from fastapi import Depends, HTTPException, status
from app.api.deps_coupon import CouponUser

# Define available roles
COUPON_ADMIN = "coupon_admin"
COUPON_MANAGER = "coupon_manager"
USER = "user"

# All available roles
AVAILABLE_ROLES = [COUPON_ADMIN, COUPON_MANAGER, USER]

def require_role(required_roles: Union[str, List[str]]):
    """
    Dependency to check if user has required role(s).
    
    Args:
        required_roles: Role or list of roles that are allowed to access the endpoint
        
    Returns:
        CouponUser: The current user if they have the required role
        
    Raises:
        HTTPException: If user doesn't have required role
    """
    # If a single role is passed, convert it to a list
    if isinstance(required_roles, str):
        required_roles = [required_roles]
    
    def role_checker(current_user: CouponUser):
        # Check if user has any of the required roles
        user_roles = getattr(current_user, 'roles', [])
        
        # If user has no roles, assign default user role
        if not user_roles:
            user_roles = [USER]
            
        # Check if user has any of the required roles
        if any(role in user_roles for role in required_roles):
            return current_user
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
            
    return role_checker

# Convenience functions for common role checks
require_coupon_admin = require_role(COUPON_ADMIN)
require_coupon_manager = require_role([COUPON_MANAGER, COUPON_ADMIN])
require_user = require_role([USER, COUPON_MANAGER, COUPON_ADMIN])