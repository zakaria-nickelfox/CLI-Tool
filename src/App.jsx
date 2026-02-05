import React, { useState } from 'react';
import Navbar from './components/Navbar/Navbar';
import Button from './components/Button/Button';
import Sidebar from './components/Sidebar/Sidebar';
import './App.css'; // For general app layout

function App() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const navItems = [
    { label: 'Home', href: '/' },
    { label: 'About', href: '/about' },
    { label: 'Services', href: '/services' },
    { label: 'Contact', href: '/contact' },
  ];

  const handleButtonClick = (componentName) => {
    alert(`Button clicked in ${componentName} context!`);
  };

  return (
    <div className="App">
      <Navbar brandName="My App" navItems={navItems} onMenuClick={() => setIsSidebarOpen(true)} />
      <Sidebar
        isOpen={isSidebarOpen}
        onClose={() => setIsSidebarOpen(false)}
        navItems={navItems}
      />

      <main className="App-content">
        <h1>Welcome to the Component Showcase!</h1>

        <section className="component-section">
          <h2>Buttons</h2>
          <div className="button-group">
            <Button onClick={() => handleButtonClick('Primary Button')} variant="primary">
              Primary Button
            </Button>
            <Button onClick={() => handleButtonClick('Secondary Button')} variant="secondary">
              Secondary Button
            </Button>
            <Button onClick={() => handleButtonClick('Disabled Button')} variant="primary" disabled>
              Disabled Button
            </Button>
          </div>
        </section>

        <section className="component-section">
          <h2>Sidebar Controls</h2>
          <p>Click the menu icon in the Navbar to open the sidebar, or use the button below:</p>
          <Button onClick={() => setIsSidebarOpen(true)} variant="secondary">
            Open Sidebar
          </Button>
        </section>
      </main>
    </div>
  );
}

export default App;
