# DPG Project Management System Frontend

## Setup

```bash
npm install
npm run dev  # Runs on http://localhost:3000
```

## Environment Variables

Create `.env.local`:

```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=DPG Project Management System
NEXT_PUBLIC_COLLEGE_NAME=DPG ITM College
NEXT_PUBLIC_COMPANY_NAME=NexyugTech
```

## Project Structure

- `app/` - Next.js pages and layouts
- `components/` - React components
- `services/` - API clients and utilities
- `middleware.ts` - Authentication middleware
- `store/` - Zustand state management
