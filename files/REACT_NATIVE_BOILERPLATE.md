# React Native Frontend Boilerplate Documentation

This boilerplate provides a complete mobile app frontend setup with reusable UI components and RBAC integration for React Native.

## Features Included

1. **Button Component** - Customizable button with variants and loading states
2. **Input Component** - Form input with validation and icons
3. **Card Component** - Container component for content
4. **Table Component** - Data table with sorting and actions
5. **RBAC Integration** - Role-based access control service and hooks

---

## Installation

### Dependencies

```bash
npm install axios @react-native-async-storage/async-storage

# or with yarn
yarn add axios @react-native-async-storage/async-storage
```

---

## 1. Button Component

### Features
- Multiple variants (primary, secondary, outline, danger)
- Size options (small, medium, large)
- Loading state
- Icon support
- Disabled state

### Usage

```tsx
import { Button } from './components/Button';

// Basic button
<Button title="Click Me" onPress={() => console.log('Clicked')} />

// Primary button
<Button 
  title="Submit" 
  variant="primary" 
  size="large"
  onPress={handleSubmit} 
/>

// Button with loading state
<Button 
  title="Save" 
  variant="primary"
  loading={isLoading}
  onPress={handleSave} 
/>

// Outline button
<Button 
  title="Cancel" 
  variant="outline"
  onPress={handleCancel} 
/>

// Danger button
<Button 
  title="Delete" 
  variant="danger"
  onPress={handleDelete} 
/>

// Disabled button
<Button 
  title="Submit" 
  disabled={!isValid}
  onPress={handleSubmit} 
/>

// Button with icon
<Button 
  title="Add" 
  icon={<Icon name="plus" size={20} color="#fff" />}
  onPress={handleAdd} 
/>
```

### Custom Styling

```tsx
<Button 
  title="Custom" 
  style={{ marginTop: 20, borderRadius: 12 }}
  textStyle={{ fontSize: 18, fontWeight: 'bold' }}
  onPress={handlePress} 
/>
```

---

## 2. Input Component

### Features
- Label and helper text
- Error messages
- Left and right icons
- Multiple variants (outlined, filled, standard)
- Focus states

### Usage

```tsx
import { Input } from './components/Input';

// Basic input
<Input 
  placeholder="Enter your name"
  value={name}
  onChangeText={setName}
/>

// Input with label
<Input 
  label="Email"
  placeholder="email@example.com"
  value={email}
  onChangeText={setEmail}
  keyboardType="email-address"
/>

// Input with error
<Input 
  label="Password"
  placeholder="Enter password"
  value={password}
  onChangeText={setPassword}
  secureTextEntry
  error={passwordError}
/>

// Input with helper text
<Input 
  label="Username"
  placeholder="Choose a username"
  value={username}
  onChangeText={setUsername}
  helperText="Must be 3-20 characters"
/>

// Input with icons
<Input 
  label="Search"
  placeholder="Search..."
  value={search}
  onChangeText={setSearch}
  leftIcon={<Icon name="search" size={20} color="#8E8E93" />}
  rightIcon={
    search && (
      <TouchableOpacity onPress={() => setSearch('')}>
        <Icon name="close" size={20} color="#8E8E93" />
      </TouchableOpacity>
    )
  }
/>

// Filled variant
<Input 
  variant="filled"
  label="Address"
  placeholder="Enter your address"
  value={address}
  onChangeText={setAddress}
/>
```

### Complete Form Example

```tsx
import React, { useState } from 'react';
import { View } from 'react-native';
import { Input } from './components/Input';
import { Button } from './components/Button';

const LoginForm = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState({});

  const handleSubmit = () => {
    // Validate and submit
  };

  return (
    <View style={{ padding: 20 }}>
      <Input 
        label="Email"
        placeholder="email@example.com"
        value={email}
        onChangeText={setEmail}
        error={errors.email}
        keyboardType="email-address"
        autoCapitalize="none"
      />
      
      <Input 
        label="Password"
        placeholder="Enter password"
        value={password}
        onChangeText={setPassword}
        error={errors.password}
        secureTextEntry
      />
      
      <Button 
        title="Login"
        onPress={handleSubmit}
        style={{ marginTop: 20 }}
      />
    </View>
  );
};
```

---

## 3. Card Component

### Features
- Title and subtitle
- Header and footer sections
- Multiple variants (elevated, outlined, filled)
- Custom styling

### Usage

```tsx
import { Card } from './components/Card';

// Basic card
<Card>
  <Text>Card content goes here</Text>
</Card>

// Card with title
<Card title="User Profile">
  <Text>John Doe</Text>
  <Text>john@example.com</Text>
</Card>

// Card with title and subtitle
<Card 
  title="Order #12345"
  subtitle="Placed on Jan 1, 2024"
>
  <Text>Order details...</Text>
</Card>

// Elevated card (default)
<Card variant="elevated">
  <Text>This card has shadow</Text>
</Card>

// Outlined card
<Card variant="outlined">
  <Text>This card has border</Text>
</Card>

// Filled card
<Card variant="filled">
  <Text>This card has background</Text>
</Card>

// Card with header and footer
<Card
  header={
    <Image source={{ uri: 'https://...' }} style={{ height: 200 }} />
  }
  footer={
    <View style={{ flexDirection: 'row', justifyContent: 'space-between' }}>
      <Button title="Cancel" variant="outline" />
      <Button title="Confirm" />
    </View>
  }
>
  <Text>Card content</Text>
</Card>
```

### List of Cards Example

```tsx
import { FlatList } from 'react-native';

const ProductList = ({ products }) => {
  return (
    <FlatList
      data={products}
      renderItem={({ item }) => (
        <Card 
          title={item.name}
          subtitle={`$${item.price}`}
          style={{ marginBottom: 16 }}
        >
          <Text>{item.description}</Text>
          <Button 
            title="Add to Cart"
            onPress={() => handleAddToCart(item.id)}
            style={{ marginTop: 12 }}
          />
        </Card>
      )}
      keyExtractor={(item) => item.id.toString()}
    />
  );
};
```

---

## 4. Table Component

### Features
- Customizable columns
- Row click handler
- Empty state
- Custom cell rendering
- Loading state

### Usage

```tsx
import { Table } from './components/Table';

const columns = [
  { key: 'name', title: 'Name', width: '40%' },
  { key: 'email', title: 'Email', width: '40%' },
  { key: 'role', title: 'Role', width: '20%' },
];

const data = [
  { id: 1, name: 'John Doe', email: 'john@example.com', role: 'Admin' },
  { id: 2, name: 'Jane Smith', email: 'jane@example.com', role: 'User' },
];

<Table 
  columns={columns}
  data={data}
  onRowPress={(item) => console.log('Clicked:', item)}
/>
```

### Custom Cell Rendering

```tsx
const columns = [
  { 
    key: 'name', 
    title: 'Name',
    render: (item) => (
      <View style={{ flexDirection: 'row', alignItems: 'center' }}>
        <Image 
          source={{ uri: item.avatar }} 
          style={{ width: 30, height: 30, borderRadius: 15, marginRight: 8 }}
        />
        <Text style={{ fontWeight: 'bold' }}>{item.name}</Text>
      </View>
    )
  },
  { 
    key: 'status', 
    title: 'Status',
    render: (item) => (
      <View style={{ 
        backgroundColor: item.status === 'active' ? '#4CAF50' : '#F44336',
        paddingHorizontal: 8,
        paddingVertical: 4,
        borderRadius: 4,
      }}>
        <Text style={{ color: '#fff', fontSize: 12 }}>
          {item.status.toUpperCase()}
        </Text>
      </View>
    )
  },
  {
    key: 'actions',
    title: 'Actions',
    render: (item) => (
      <View style={{ flexDirection: 'row', gap: 8 }}>
        <TouchableOpacity onPress={() => handleEdit(item)}>
          <Icon name="edit" size={20} />
        </TouchableOpacity>
        <TouchableOpacity onPress={() => handleDelete(item)}>
          <Icon name="delete" size={20} />
        </TouchableOpacity>
      </View>
    )
  },
];
```

### With Loading State

```tsx
const [loading, setLoading] = useState(true);
const [data, setData] = useState([]);

useEffect(() => {
  fetchData().then(setData).finally(() => setLoading(false));
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

### Setup

1. Wrap your app with the RBAC provider:

```tsx
import { RBACProvider } from './services/RBACService';

function App() {
  return (
    <RBACProvider apiUrl="https://api.yourapp.com">
      <Navigation />
    </RBACProvider>
  );
}
```

### Using the Hook

```tsx
import { useRBAC, Role, Permission } from './services/RBACService';

function ProfileScreen() {
  const { user, logout, hasRole, hasPermission, isAdmin } = useRBAC();

  if (!user) {
    return <Text>Please login</Text>;
  }

  return (
    <View>
      <Text>Welcome, {user.name}!</Text>
      
      {isAdmin() && (
        <Button title="Admin Panel" onPress={navigateToAdmin} />
      )}
      
      {hasRole(Role.MODERATOR) && (
        <Button title="Moderate Content" onPress={navigateToModeration} />
      )}
      
      {hasPermission(Permission.CREATE_USER) && (
        <Button title="Create User" onPress={navigateToCreateUser} />
      )}
      
      <Button title="Logout" onPress={logout} variant="outline" />
    </View>
  );
}
```

### Login Flow

```tsx
import { useRBAC } from './services/RBACService';

function LoginScreen() {
  const { login, loading } = useRBAC();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async () => {
    try {
      await login(email, password);
      // Navigation will happen automatically if using auth navigation
    } catch (error) {
      Alert.alert('Error', 'Invalid credentials');
    }
  };

  return (
    <View style={{ padding: 20 }}>
      <Input 
        label="Email"
        value={email}
        onChangeText={setEmail}
        keyboardType="email-address"
      />
      
      <Input 
        label="Password"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
      />
      
      <Button 
        title="Login"
        onPress={handleLogin}
        loading={loading}
        style={{ marginTop: 20 }}
      />
    </View>
  );
}
```

### Protected Screens with HOC

```tsx
import { withRoles, Role } from './services/RBACService';

// Admin only screen
const AdminScreen = () => {
  return (
    <View>
      <Text>Admin Dashboard</Text>
    </View>
  );
};

export default withRoles([Role.ADMIN])(AdminScreen);

// Multiple roles allowed
const ModeratorScreen = () => {
  return (
    <View>
      <Text>Moderation Panel</Text>
    </View>
  );
};

export default withRoles([Role.ADMIN, Role.MODERATOR])(ModeratorScreen);
```

### Navigation Guard

```tsx
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { useRBAC } from './services/RBACService';

const Stack = createNativeStackNavigator();

function Navigation() {
  const { user, loading } = useRBAC();

  if (loading) {
    return <LoadingScreen />;
  }

  return (
    <NavigationContainer>
      <Stack.Navigator>
        {user ? (
          <>
            <Stack.Screen name="Home" component={HomeScreen} />
            <Stack.Screen name="Profile" component={ProfileScreen} />
            {user.roles.includes(Role.ADMIN) && (
              <Stack.Screen name="Admin" component={AdminScreen} />
            )}
          </>
        ) : (
          <>
            <Stack.Screen name="Login" component={LoginScreen} />
            <Stack.Screen name="Register" component={RegisterScreen} />
          </>
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
}
```

### Check Multiple Permissions

```tsx
const { hasAllPermissions, hasAnyPermission } = useRBAC();

// Check if user has all permissions
if (hasAllPermissions([Permission.CREATE_USER, Permission.DELETE_USER])) {
  // Show full user management
}

// Check if user has any of the permissions
if (hasAnyPermission([Permission.READ_USER, Permission.UPDATE_USER])) {
  // Show limited user management
}
```

---

## Complete App Example

```tsx
import React from 'react';
import { SafeAreaView, ScrollView, View } from 'react-native';
import { RBACProvider, useRBAC, Role } from './services/RBACService';
import { Button } from './components/Button';
import { Input } from './components/Input';
import { Card } from './components/Card';
import { Table } from './components/Table';

const App = () => {
  return (
    <RBACProvider apiUrl="https://api.yourapp.com">
      <SafeAreaView style={{ flex: 1 }}>
        <MainScreen />
      </SafeAreaView>
    </RBACProvider>
  );
};

const MainScreen = () => {
  const { user, isAdmin } = useRBAC();
  const [search, setSearch] = React.useState('');

  const columns = [
    { key: 'name', title: 'Name' },
    { key: 'email', title: 'Email' },
  ];

  const data = [
    { id: 1, name: 'John Doe', email: 'john@example.com' },
  ];

  return (
    <ScrollView style={{ padding: 16 }}>
      <Card title="Dashboard" subtitle={`Welcome, ${user?.name}`}>
        <Input 
          placeholder="Search..."
          value={search}
          onChangeText={setSearch}
        />
        
        <Table columns={columns} data={data} style={{ marginTop: 16 }} />
        
        {isAdmin() && (
          <Button 
            title="Admin Actions"
            variant="primary"
            style={{ marginTop: 16 }}
          />
        )}
      </Card>
    </ScrollView>
  );
};

export default App;
```

---

## Styling Tips

### Global Theme

Create a theme file:

```tsx
// theme.ts
export const colors = {
  primary: '#007AFF',
  secondary: '#5856D6',
  danger: '#FF3B30',
  success: '#4CAF50',
  text: '#000000',
  textSecondary: '#8E8E93',
  border: '#C7C7CC',
  background: '#FFFFFF',
};

export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
};
```

Use in components:

```tsx
import { colors, spacing } from './theme';

<Button 
  style={{ backgroundColor: colors.primary, margin: spacing.md }}
  title="Themed Button"
/>
```

### Custom Component Styles

```tsx
<Card 
  style={{
    backgroundColor: '#f5f5f5',
    borderRadius: 16,
    padding: 20,
  }}
  titleStyle={{
    fontSize: 24,
    color: '#333',
  }}
>
  <Text>Custom styled card</Text>
</Card>
```

---

## Testing

### Component Testing

```tsx
import { render, fireEvent } from '@testing-library/react-native';
import { Button } from './Button';

test('Button calls onPress when clicked', () => {
  const onPress = jest.fn();
  const { getByText } = render(<Button title="Click Me" onPress={onPress} />);
  
  fireEvent.press(getByText('Click Me'));
  expect(onPress).toHaveBeenCalledTimes(1);
});

test('Button shows loading state', () => {
  const { getByText } = render(<Button title="Submit" loading={true} />);
  expect(getByText('Loading...')).toBeTruthy();
});
```

### RBAC Testing

```tsx
import { RBACProvider } from './RBACService';
import { render } from '@testing-library/react-native';

test('Admin can see admin button', () => {
  const { getByText } = render(
    <RBACProvider apiUrl="https://api.test.com">
      <TestComponent />
    </RBACProvider>
  );
  
  // Test assertions
});
```
