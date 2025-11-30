# Windows Authentication Integration for VeintiSeisApp

This document describes the Windows Authentication integration implemented for the VeintiSeisApp backend and frontend.

## Overview

The integration enables seamless Single Sign-On (SSO) experience when the application is deployed with IIS, using Windows Authentication (Kerberos/NTLM) without requiring users to enter login credentials.

## Architecture

```
Browser → IIS (Windows Auth) → Reverse Proxy → FastAPI (localhost:8000)
IIS injects X-Forwarded-User = DOMAIN\username
FastAPI reads this header and identifies the user
```

## Backend Changes

### 1. New Windows Authentication Endpoint

Created `app/api/routes/login_windows.py` with a new endpoint:
- `GET /api/v1/login/windows` - Returns Windows authentication status

### 2. Updated Windows Auth Router

Enhanced `app/api/routes/windows_auth.py` with:
- `GET /api/v1/windows-user` - Direct access to Windows user without DB mapping

### 3. Windows Authentication Middleware

Created `app/core/middleware/windows_auth.py`:
- Extracts `X-Forwarded-User` header from requests
- Stores Windows user in request state

### 4. Windows User Dependency

Created `app/core/security/windows_user.py`:
- Provides `get_windows_user` dependency for route protection

### 5. CORS Configuration

Updated CORS to allow requests from IIS hostname (`http://myapi.local`)

### 6. Router Registration

Modified `app/api/main.py` to include the new Windows authentication router

## Frontend Changes

### 1. Enhanced Login Page

Updated `frontend/src/routes/login.tsx`:
- Added "Login with Windows Authentication" button
- Implemented Windows authentication flow

### 2. Authentication Hook

Enhanced `frontend/src/hooks/useAuth.ts`:
- Improved Windows authentication detection
- Automatic authentication on app load

## Database Integration

The User model can be linked to Windows users:
- Added optional `windows_username` field to User model
- Enables automatic user creation and mapping

## IIS Configuration Requirements

For the integration to work, IIS must be configured with:

1. **Required IIS modules:**
   - Windows Authentication
   - URL Rewrite
   - Application Request Routing (ARR)

2. **IIS settings:**
   - Disable Anonymous Authentication
   - Enable Windows Authentication
   - Reverse proxy all traffic to `http://127.0.0.1:8000`
   - Add header: `X-Forwarded-User = %{LOGON_USER}`

## API Endpoints

### Windows Authentication Endpoints

1. `GET /api/v1/login/windows`
   - Verifies Windows authentication status
   - Returns authentication information

2. `GET /api/v1/windows-user`
   - Returns the Windows user authenticated by IIS
   - Direct access without database mapping

3. `GET /api/v1/me`
   - Returns user information (existing endpoint, compatible with Windows auth)

## Testing

In development, you can simulate Windows Authentication by manually adding the `X-Forwarded-User` header to API requests:

```
X-Forwarded-User: DOMAIN\username
```

## Security Considerations

- FastAPI trusts the `X-Forwarded-User` header injected by IIS
- Ensure IIS is properly configured to prevent header spoofing
- Use HTTPS in production environments
- Regularly review and audit authentication logs

## Deployment

1. Deploy the application behind IIS
2. Configure IIS for Windows Authentication
3. Set up reverse proxy to forward requests to FastAPI
4. Ensure proper header forwarding (`X-Forwarded-User`)

The application will automatically:
1. Attempt Windows authentication on load
2. Create user records as needed
3. Map users to admin roles based on configuration
4. Redirect authenticated users to the main application