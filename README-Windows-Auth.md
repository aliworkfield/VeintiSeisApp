# Windows Authentication Setup

This application supports Windows Authentication for seamless Single Sign-On (SSO) experience when deployed with IIS.

## How It Works

1. IIS handles Windows Authentication and injects the `X-Windows-User` header into requests
2. The backend processes this header to authenticate users
3. Users are automatically created in the database on first login
4. Role mapping can be configured via `WINDOWS_ADMIN_USERS` environment variable

## Development Setup

### Backend
```bash
cd backend
fastapi run app/main.py --host localhost --port 8001
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Frontend will be available at http://localhost:5175
Backend API will be available at http://localhost:8001

## Windows Authentication Configuration

For Windows Authentication to work:

1. Deploy the application behind IIS
2. Enable Windows Authentication in IIS
3. Disable Anonymous Authentication
4. Ensure IIS is configured to pass the `X-Windows-User` header

## Environment Variables

Configure these in your `.env` files:

### Backend (.env)
```
WINDOWS_ADMIN_USERS=user1@domain,user2@domain
WINDOWS_EMAIL_DOMAIN=your-domain.local
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:8001
```

## Testing Windows Authentication

In development, you can simulate Windows Authentication by manually adding the `X-Windows-User` header to API requests:

```
X-Windows-User: domain\\username
```

The application will automatically:
1. Attempt Windows authentication on load
2. Create user records as needed
3. Map users to admin roles based on configuration
4. Redirect authenticated users to the main application