# DPG PMS - Frontend

React-based frontend for the DPG Project Management System. Built with Next.js, TypeScript, Tailwind CSS, and shadcn/ui.

## 🏗️ Folder Structure

```
frontend/
├── app/                           # Next.js app directory
│   ├── (auth)/                   # Authentication routes (public)
│   │   ├── login/
│   │   │   └── page.tsx          # Login page with OTP
│   │   └── verify-otp/
│   │       └── page.tsx          # OTP verification page
│   ├── (student)/                # Student dashboard (protected)
│   │   ├── dashboard/
│   │   │   └── page.tsx
│   │   ├── projects/
│   │   │   ├── page.tsx
│   │   │   ├── [id]/
│   │   │   │   └── page.tsx      # Project detail
│   │   ├── teams/
│   │   │   ├── page.tsx
│   │   │   └── [id]/
│   │   │       └── page.tsx      # Team detail
│   │   └── submissions/
│   │       └── page.tsx
│   ├── (supervisor)/             # Supervisor dashboard (protected)
│   │   ├── dashboard/
│   │   │   └── page.tsx
│   │   ├── teams/
│   │   ├── submissions/
│   │   └── scoring/
│   ├── (admin)/                  # Admin dashboard (protected)
│   │   ├── dashboard/
│   │   │   └── page.tsx
│   │   ├── projects/
│   │   ├── users/
│   │   ├── leaderboard/
│   │   └── analytics/
│   ├── layout.tsx                # Root layout
│   ├── page.tsx                  # Home page
│   └── globals.css               # Global styles
│
├── components/                    # Reusable components
│   ├── ui/                       # shadcn/ui components (auto-generated)
│   ├── auth/
│   │   ├── LoginForm.tsx
│   │   ├── OTPVerification.tsx
│   │   └── ProtectedRoute.tsx
│   ├── dashboard/
│   │   ├── StudentDashboard.tsx
│   │   ├── SupervisorDashboard.tsx
│   │   ├── AdminDashboard.tsx
│   │   ├── Sidebar.tsx
│   │   └── Navbar.tsx
│   ├── projects/
│   │   ├── ProjectCard.tsx
│   │   ├── ProjectForm.tsx
│   │   └── ProjectDetail.tsx
│   ├── teams/
│   │   ├── TeamCard.tsx
│   │   ├── TeamForm.tsx
│   │   └── TeamMemberList.tsx
│   ├── submissions/
│   │   ├── SubmissionForm.tsx
│   │   ├── SubmissionList.tsx
│   │   └── SubmissionDetail.tsx
│   ├── chatbot/
│   │   ├── ChatWindow.tsx
│   │   └── ChatMessage.tsx
│   ├── leaderboard/
│   │   └── LeaderboardTable.tsx
│   └── common/
│       ├── Header.tsx
│       ├── Footer.tsx
│       └── LoadingSpinner.tsx
│
├── hooks/                        # Custom React hooks
│   ├── useAuth.ts               # Authentication hook
│   ├── useProject.ts            # Project hook
│   ├── useTeam.ts               # Team hook
│   ├── useFetch.ts              # Data fetching hook
│   └── useNotification.ts       # Notification hook
│
├── store/                        # Zustand stores
│   ├── auth.ts                  # Auth store
│   ├── projects.ts              # Project store
│   ├── notifications.ts         # Notification store
│   └── ui.ts                    # UI state store
│
├── services/                     # API services
│   ├── api.ts                   # Base API client
│   ├── auth.ts                  # Auth service
│   ├── projects.ts              # Project service
│   ├── teams.ts                 # Team service
│   ├── submissions.ts           # Submission service
│   ├── chatbot.ts               # Chatbot service
│   └── analytics.ts             # Analytics service
│
├── types/                        # TypeScript definitions
│   └── index.ts                 # All types
│
├── utils/                        # Utility functions
│   ├── api-client.ts            # API client instance
│   ├── validators.ts            # Form validators
│   ├── formatters.ts            # Data formatters
│   └── constants.ts             # App constants
│
├── config/                       # Configuration
│   ├── api.ts                   # API config
│   └── constants.ts             # Constants
│
├── public/                       # Static assets
│   ├── logo.png
│   ├── icons/
│   └── images/
│
├── package.json
├── tsconfig.json
├── next.config.mjs
├── tailwind.config.js
├── postcss.config.js
└── .env.example
```

## 🚀 Getting Started

### Installation

```bash
# Install dependencies
npm install

# Setup environment
cp .env.example .env.local

# Edit .env.local with your API URL
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

### Development

```bash
npm run dev
# Open http://localhost:3000
```

### Build

```bash
npm run build
npm start
```

### Linting

```bash
npm run lint
npm run type-check
```

## 🔐 Authentication Flow

1. **Login Page** (`/auth/login`)
   - User enters email
   - Click "Send OTP"
   - OTP sent via SMTP

2. **OTP Verification** (`/auth/verify-otp`)
   - User enters 6-digit OTP
   - System verifies OTP
   - JWT token stored in localStorage
   - Redirected to role-based dashboard

3. **Protected Routes**
   - All dashboard routes protected with `ProtectedRoute` component
   - Redirects unauthenticated users to login

## 📊 Role-Based Dashboards

### Student Dashboard
- View enrolled projects
- Form teams or join existing teams
- Upload submissions
- Track project progress
- View feedback and scores
- Access RAG chatbot

### Supervisor Dashboard
- View assigned teams
- Review submissions
- Score stages (out of 10)
- Provide feedback
- Track team progress
- Download reports

### Admin Dashboard
- Create projects
- Manage users and roles
- Assign/change supervisors
- View analytics
- Access leaderboard
- Generate reports

## 🛠️ Key Technologies

- **Next.js 14** - React framework with App Router
- **React 18** - UI library
- **TypeScript** - Type safety
- **Tailwind CSS v4** - Styling
- **shadcn/ui** - Component library
- **Zustand** - State management
- **SWR** - Data fetching
- **React Hook Form** - Form handling
- **Zod** - Schema validation
- **Axios** - HTTP client
- **Framer Motion** - Animations

## 📝 Component Examples

### LoginForm Component
```tsx
import { LoginForm } from '@/components/auth/LoginForm';

export default function LoginPage() {
  return <LoginForm />;
}
```

### Protected Route
```tsx
import { ProtectedRoute } from '@/components/auth/ProtectedRoute';
import StudentDashboard from '@/components/dashboard/StudentDashboard';

export default function Page() {
  return (
    <ProtectedRoute allowedRoles={['STUDENT']}>
      <StudentDashboard />
    </ProtectedRoute>
  );
}
```

### Using Zustand Store
```tsx
import { useAuthStore } from '@/store/auth';

export function MyComponent() {
  const user = useAuthStore((state) => state.user);
  const isStudent = useAuthStore((state) => state.isStudent());

  return <div>{user?.name}</div>;
}
```

### Using SWR for Data
```tsx
import useSWR from 'swr';
import { apiClient } from '@/services/api';

export function ProjectList() {
  const { data, error, isLoading } = useSWR(
    '/projects',
    url => apiClient.get(url)
  );

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error loading projects</div>;

  return (
    <div>
      {data?.data?.map(project => (
        <ProjectCard key={project.id} project={project} />
      ))}
    </div>
  );
}
```

## 🎨 Styling with Tailwind

All components use Tailwind CSS v4. Custom colors are defined in `globals.css`:

```css
@theme inline {
  --color-primary: #007bff;
  --color-secondary: #6c757d;
  --color-success: #28a745;
  --color-danger: #dc3545;
}
```

Use design tokens:
```tsx
<button className="bg-primary text-white">Submit</button>
```

## 🔗 API Integration

### Using API Client
```tsx
import { apiClient } from '@/services/api';

// GET
const response = await apiClient.get<Project>('/projects/123');

// POST
const response = await apiClient.post<Project>('/projects', {
  title: 'My Project'
});

// File Upload
const response = await apiClient.uploadFile(
  '/submissions',
  file,
  { stage: 'SYNOPSIS' }
);
```

### Error Handling
```tsx
try {
  const response = await apiClient.post('/auth/verify-otp', { email, otp });
  if (response.success) {
    // Handle success
  } else {
    // Handle error
    console.error(response.error);
  }
} catch (error) {
  console.error('Request failed', error);
}
```

## 💬 Chatbot Integration

```tsx
import { chatbotService } from '@/services/chatbot';

async function sendMessage(message: string) {
  const response = await chatbotService.sendMessage(
    message,
    'STUDENT',
    chatHistory
  );
  
  if (response.success) {
    console.log(response.response);
  }
}
```

## 🧪 Testing

```bash
# Unit tests
npm run test

# Coverage report
npm run test:coverage

# E2E tests
npm run test:e2e
```

## 📦 Build & Deploy

### Vercel Deploy
```bash
vercel deploy
```

### Docker Build
```bash
docker build -t dpg-pms-frontend .
docker run -p 3000:3000 dpg-pms-frontend
```

### Environment Variables for Production
```env
NEXT_PUBLIC_API_BASE_URL=https://api.dpg-itm.edu.in
NEXT_PUBLIC_APP_NAME=DPG Project Management System
```

## 🔐 Security Best Practices

✅ Sensitive data in environment variables  
✅ JWT tokens stored in localStorage (with httpOnly consideration)  
✅ Protected routes with role checking  
✅ CSRF protection via SameSite cookies  
✅ Input validation with Zod  
✅ Sanitized API responses  

## 📱 Responsive Design

All components are mobile-first and responsive:
- Mobile: `< 640px`
- Tablet: `640px - 1024px`
- Desktop: `> 1024px`

Use Tailwind breakpoints:
```tsx
<div className="text-sm md:text-base lg:text-lg">
  Responsive text
</div>
```

## 🚀 Performance Optimization

- Image optimization with Next.js Image
- Code splitting with dynamic imports
- SWR caching
- Lazy loading components
- CSS minification
- Bundle analysis

```bash
npm run analyze
```

## 📚 Useful Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev)
- [Tailwind CSS](https://tailwindcss.com)
- [shadcn/ui](https://ui.shadcn.com)
- [TypeScript](https://www.typescriptlang.org)
- [Zustand](https://zustand-demo.vercel.app)
- [SWR](https://swr.vercel.app)

## 🤝 Contributing

1. Create a feature branch
2. Make changes
3. Test locally
4. Submit PR

## 📞 Support

For frontend-specific issues, contact the development team or check GitHub issues.

---

**Frontend for DPG Project Management System**
