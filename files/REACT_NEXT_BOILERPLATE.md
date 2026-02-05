# React Next.js Frontend Boilerplate Documentation

This boilerplate provides a complete web frontend setup with reusable UI components and RBAC integration for Next.js with React.

## Features Included

1. **Button Component** - Customizable button with variants and loading states
2. **Input Component** - Form input with validation and icons
3. **Card Component** - Container component for content
4. **Table Component** - Data table with pagination
5. **RBAC Integration** - Role-based access control service and hooks

---

## Installation

### Dependencies

```bash
npm install axios

# or with yarn
yarn add axios
```

### Tailwind CSS Setup

Install Tailwind CSS (if not already installed):

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

Configure `tailwind.config.js`:

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

---

## 1. Button Component

### Features
- Multiple variants (primary, secondary, outline, danger, ghost)
- Size options (sm, md, lg)
- Loading state
- Icon support
- Disabled state

### Usage

```tsx
import { Button } from '@/components/Button';

// Basic button
<Button onClick={() => console.log('Clicked')}>
  Click Me
</Button>

// Primary button
<Button variant="primary" size="lg" onClick={handleSubmit}>
  Submit
</Button>

// Button with loading state
<Button variant="primary" loading={isLoading} onClick={handleSave}>
  Save
</Button>

// Outline button
<Button variant="outline" onClick={handleCancel}>
  Cancel
</Button>

// Danger button
<Button variant="danger" onClick={handleDelete}>
  Delete
</Button>

// Disabled button
<Button disabled={!isValid} onClick={handleSubmit}>
  Submit
</Button>

// Button with icon
<Button icon={<PlusIcon className="w-5 h-5" />} onClick={handleAdd}>
  Add Item
</Button>

// Ghost button
<Button variant="ghost" onClick={handleSecondary}>
  Secondary Action
</Button>
```

### Custom Styling

```tsx
<Button 
  className="mt-4 shadow-lg"
  onClick={handlePress}
>
  Custom Styled Button
</Button>
```

---

## 2. Input Component

### Features
- Label and helper text
- Error messages
- Left and right icons
- Multiple variants (outlined, filled, standard)
- Forward ref support

### Usage

```tsx
import { Input } from '@/components/Input';

// Basic input
<Input 
  placeholder="Enter your name"
  value={name}
  onChange={(e) => setName(e.target.value)}
/>

// Input with label
<Input 
  label="Email"
  placeholder="email@example.com"
  value={email}
  onChange={(e) => setEmail(e.target.value)}
  type="email"
/>

// Input with error
<Input 
  label="Password"
  placeholder="Enter password"
  value={password}
  onChange={(e) => setPassword(e.target.value)}
  type="password"
  error={passwordError}
/>

// Input with helper text
<Input 
  label="Username"
  placeholder="Choose a username"
  value={username}
  onChange={(e) => setUsername(e.target.value)}
  helperText="Must be 3-20 characters"
/>

// Input with icons
<Input 
  label="Search"
  placeholder="Search..."
  value={search}
  onChange={(e) => setSearch(e.target.value)}
  leftIcon={<SearchIcon className="w-5 h-5" />}
  rightIcon={
    search && (
      <button onClick={() => setSearch('')}>
        <XIcon className="w-5 h-5" />
      </button>
    )
  }
/>

// Filled variant
<Input 
  variant="filled"
  label="Address"
  placeholder="Enter your address"
  value={address}
  onChange={(e) => setAddress(e.target.value)}
/>

// Full width input
<Input 
  fullWidth
  label="Description"
  placeholder="Enter description"
  value={description}
  onChange={(e) => setDescription(e.target.value)}
/>
```

### With React Hook Form

```tsx
import { useForm } from 'react-hook-form';
import { Input } from '@/components/Input';

function LoginForm() {
  const { register, handleSubmit, formState: { errors } } = useForm();

  const onSubmit = (data) => {
    console.log(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <Input 
        label="Email"
        {...register('email', { required: 'Email is required' })}
        error={errors.email?.message}
        fullWidth
      />
      
      <Input 
        label="Password"
        type="password"
        {...register('password', { required: 'Password is required' })}
        error={errors.password?.message}
        fullWidth
      />
      
      <Button type="submit" className="mt-4">
        Login
      </Button>
    </form>
  );
}
```

---

## 3. Card Component

### Features
- Title and subtitle
- Header and footer sections
- Multiple variants (elevated, outlined, filled)
- Click handler for interactive cards
- Composable with CardHeader and CardFooter

### Usage

```tsx
import { Card, CardHeader, CardFooter } from '@/components/Card';

// Basic card
<Card>
  <p>Card content goes here</p>
</Card>

// Card with title
<Card title="User Profile">
  <p>John Doe</p>
  <p>john@example.com</p>
</Card>

// Card with title and subtitle
<Card 
  title="Order #12345"
  subtitle="Placed on Jan 1, 2024"
>
  <p>Order details...</p>
</Card>

// Elevated card (default)
<Card variant="elevated">
  <p>This card has shadow</p>
</Card>

// Outlined card
<Card variant="outlined">
  <p>This card has border</p>
</Card>

// Filled card
<Card variant="filled">
  <p>This card has background</p>
</Card>

// Card with custom header and footer
<Card>
  <CardHeader>
    <h3 className="text-xl font-bold">Custom Header</h3>
  </CardHeader>
  
  <p>Card content</p>
  
  <CardFooter className="flex justify-between">
    <Button variant="outline">Cancel</Button>
    <Button variant="primary">Confirm</Button>
  </CardFooter>
</Card>

// Interactive card
<Card onClick={() => navigate('/details')}>
  <h3>Click me!</h3>
  <p>This card is clickable</p>
</Card>
```

### Grid of Cards

```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {products.map((product) => (
    <Card 
      key={product.id}
      title={product.name}
      subtitle={`$${product.price}`}
    >
      <p>{product.description}</p>
      <Button 
        className="mt-4"
        onClick={() => handleAddToCart(product.id)}
      >
        Add to Cart
      </Button>
    </Card>
  ))}
</div>
```

---

## 4. Table Component

### Features
- Customizable columns
- Row click handler
- Empty state
- Custom cell rendering
- Loading state
- Striped rows
- Hoverable rows
- Built-in pagination component

### Usage

```tsx
import { Table, Pagination } from '@/components/Table';

const columns = [
  { key: 'name', title: 'Name', width: '30%' },
  { key: 'email', title: 'Email', width: '30%' },
  { key: 'role', title: 'Role', width: '20%', align: 'center' },
  { key: 'status', title: 'Status', width: '20%', align: 'right' },
];

const data = [
  { id: 1, name: 'John Doe', email: 'john@example.com', role: 'Admin', status: 'Active' },
  { id: 2, name: 'Jane Smith', email: 'jane@example.com', role: 'User', status: 'Active' },
];

<Table 
  columns={columns}
  data={data}
  onRowClick={(item) => navigate(`/users/${item.id}`)}
  striped
  hoverable
/>
```

### Custom Cell Rendering

```tsx
const columns = [
  { 
    key: 'name', 
    title: 'Name',
    render: (value, item) => (
      <div className="flex items-center gap-2">
        <img 
          src={item.avatar} 
          alt={value}
          className="w-8 h-8 rounded-full"
        />
        <span className="font-semibold">{value}</span>
      </div>
    )
  },
  { 
    key: 'status', 
    title: 'Status',
    render: (value) => (
      <span className={`px-2 py-1 rounded text-xs font-semibold ${
        value === 'active' 
          ? 'bg-green-100 text-green-800' 
          : 'bg-red-100 text-red-800'
      }`}>
        {value.toUpperCase()}
      </span>
    )
  },
  {
    key: 'actions',
    title: 'Actions',
    render: (value, item) => (
      <div className="flex gap-2">
        <button 
          onClick={(e) => {
            e.stopPropagation(); // Prevent row click
            handleEdit(item);
          }}
          className="text-blue-600 hover:text-blue-800"
        >
          Edit
        </button>
        <button 
          onClick={(e) => {
            e.stopPropagation();
            handleDelete(item);
          }}
          className="text-red-600 hover:text-red-800"
        >
          Delete
        </button>
      </div>
    )
  },
];
```

### With Pagination

```tsx
function UserTable() {
  const [currentPage, setCurrentPage] = useState(1);
  const [data, setData] = useState([]);
  const totalPages = 10;

  useEffect(() => {
    fetchUsers(currentPage).then(setData);
  }, [currentPage]);

  return (
    <>
      <Table 
        columns={columns}
        data={data}
        striped
        hoverable
      />
      
      <Pagination 
        currentPage={currentPage}
        totalPages={totalPages}
        onPageChange={setCurrentPage}
      />
    </>
  );
}
```

### With Loading State

```tsx
const [loading, setLoading] = useState(true);
const [data, setData] = useState([]);

useEffect(() => {
  fetchData()
    .then(setData)
    .finally(() => setLoading(false));
}, []);

<Table 
  columns={columns}
  data={data}
  loading={loading}
  emptyText="No users found"
/>
```

---

## 5. RBAC Integration

### Setup (App Router)

In `app/layout.tsx` or `app/providers.tsx`:

```tsx
'use client';

import { RBACProvider } from '@/services/RBACService';

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <RBACProvider apiUrl={process.env.NEXT_PUBLIC_API_URL || 'https://api.yourapp.com'}>
      {children}
    </RBACProvider>
  );
}
```

### Setup (Pages Router)

In `pages/_app.tsx`:

```tsx
import { RBACProvider } from '@/services/RBACService';

function MyApp({ Component, pageProps }) {
  return (
    <RBACProvider apiUrl={process.env.NEXT_PUBLIC_API_URL || 'https://api.yourapp.com'}>
      <Component {...pageProps} />
    </RBACProvider>
  );
}

export default MyApp;
```

### Using the Hook

```tsx
'use client';

import { useRBAC, Role, Permission } from '@/services/RBACService';

export default function ProfilePage() {
  const { user, logout, hasRole, hasPermission, isAdmin, isAuthenticated } = useRBAC();

  if (!isAuthenticated()) {
    return <div>Please login</div>;
  }

  return (
    <div>
      <h1>Welcome, {user?.name}!</h1>
      
      {isAdmin() && (
        <Button onClick={() => navigate('/admin')}>
          Admin Panel
        </Button>
      )}
      
      {hasRole(Role.MODERATOR) && (
        <Button onClick={() => navigate('/moderate')}>
          Moderate Content
        </Button>
      )}
      
      {hasPermission(Permission.CREATE_USER) && (
        <Button onClick={() => navigate('/users/create')}>
          Create User
        </Button>
      )}
      
      <Button variant="outline" onClick={logout}>
        Logout
      </Button>
    </div>
  );
}
```

### Login Page

```tsx
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useRBAC } from '@/services/RBACService';
import { Input } from '@/components/Input';
import { Button } from '@/components/Button';
import { Card } from '@/components/Card';

export default function LoginPage() {
  const { login, loading } = useRBAC();
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await login(email, password);
      router.push('/dashboard');
    } catch (err) {
      setError('Invalid credentials');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <Card className="w-full max-w-md">
        <form onSubmit={handleLogin} className="space-y-4">
          <h1 className="text-2xl font-bold text-center">Login</h1>
          
          {error && (
            <div className="bg-red-50 text-red-600 p-3 rounded">
              {error}
            </div>
          )}
          
          <Input 
            label="Email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            fullWidth
            required
          />
          
          <Input 
            label="Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            fullWidth
            required
          />
          
          <Button 
            type="submit"
            className="w-full"
            loading={loading}
          >
            Login
          </Button>
        </form>
      </Card>
    </div>
  );
}
```

### Protected Pages with HOC

```tsx
'use client';

import { withAuth, Role } from '@/services/RBACService';

function AdminDashboard() {
  return (
    <div>
      <h1>Admin Dashboard</h1>
      {/* Admin content */}
    </div>
  );
}

// Protect with admin role
export default withAuth(AdminDashboard, [Role.ADMIN]);

// Multiple roles allowed
function ModeratorPanel() {
  return (
    <div>
      <h1>Moderation Panel</h1>
    </div>
  );
}

export default withAuth(ModeratorPanel, [Role.ADMIN, Role.MODERATOR]);
```

### Conditional Rendering Component

```tsx
'use client';

import { Protected, Role, Permission } from '@/services/RBACService';

export default function Dashboard() {
  return (
    <div>
      <h1>Dashboard</h1>
      
      {/* Show only to admins */}
      <Protected roles={[Role.ADMIN]}>
        <div className="bg-red-100 p-4">
          <h2>Admin Section</h2>
        </div>
      </Protected>
      
      {/* Show to users with specific permission */}
      <Protected permissions={[Permission.CREATE_USER]}>
        <Button>Create New User</Button>
      </Protected>
      
      {/* Show fallback if no permission */}
      <Protected 
        roles={[Role.ADMIN]} 
        fallback={<p>You need admin access to view this.</p>}
      >
        <SecretComponent />
      </Protected>
    </div>
  );
}
```

### Middleware for Route Protection

Create `middleware.ts`:

```typescript
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const token = request.cookies.get('auth_token');
  
  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }
  
  return NextResponse.next();
}

export const config = {
  matcher: '/dashboard/:path*',
};
```

### API Route Integration

```typescript
// app/api/users/route.ts
import { NextResponse } from 'next/server';
import RBACService from '@/services/RBACService';

export async function GET(request: Request) {
  try {
    const rbacService = new RBACService(process.env.API_URL!);
    const users = await rbacService.getApi().get('/users');
    return NextResponse.json(users.data);
  } catch (error) {
    return NextResponse.json({ error: 'Failed to fetch users' }, { status: 500 });
  }
}
```

---

## Complete App Example

```tsx
'use client';

import { useRBAC, Role } from '@/services/RBACService';
import { Button } from '@/components/Button';
import { Input } from '@/components/Input';
import { Card } from '@/components/Card';
import { Table } from '@/components/Table';
import { useState } from 'react';

export default function Dashboard() {
  const { user, isAdmin } = useRBAC();
  const [search, setSearch] = useState('');

  const columns = [
    { key: 'name', title: 'Name' },
    { key: 'email', title: 'Email' },
  ];

  const data = [
    { id: 1, name: 'John Doe', email: 'john@example.com' },
  ];

  return (
    <div className="container mx-auto p-8">
      <Card title="Dashboard" subtitle={`Welcome, ${user?.name}`}>
        <div className="space-y-4">
          <Input 
            placeholder="Search..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            fullWidth
          />
          
          <Table columns={columns} data={data} striped hoverable />
          
          {isAdmin() && (
            <Button variant="primary" className="w-full">
              Admin Actions
            </Button>
          )}
        </div>
      </Card>
    </div>
  );
}
```

---

## Environment Variables

Create `.env.local`:

```env
NEXT_PUBLIC_API_URL=https://api.yourapp.com
```

---

## Testing

### Component Testing with Jest

```tsx
import { render, fireEvent } from '@testing-library/react';
import { Button } from '@/components/Button';

test('Button calls onClick when clicked', () => {
  const onClick = jest.fn();
  const { getByText } = render(<Button onClick={onClick}>Click Me</Button>);
  
  fireEvent.click(getByText('Click Me'));
  expect(onClick).toHaveBeenCalledTimes(1);
});

test('Button shows loading state', () => {
  const { getByText } = render(<Button loading>Submit</Button>);
  expect(getByText('Loading...')).toBeInTheDocument();
});
```

### RBAC Testing

```tsx
import { render } from '@testing-library/react';
import { RBACProvider } from '@/services/RBACService';

test('Admin can see admin button', () => {
  const { getByText } = render(
    <RBACProvider apiUrl="https://api.test.com">
      <TestComponent />
    </RBACProvider>
  );
  
  // Test assertions
});
```
