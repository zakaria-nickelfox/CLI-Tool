import React from 'react';
import styles from './Sidebar.module.css';

/**
 * A customizable Sidebar component.
 * @param {object} props - The component props.
 * @param {boolean} props.isOpen - Controls the visibility of the sidebar.
 * @param {function} props.onClose - Function to call when the sidebar needs to be closed.
 * @param {Array<object>} props.navItems - An array of navigation items, e.g., [{ label: 'Dashboard', href: '/dashboard' }].
 */
const Sidebar = ({ isOpen, onClose, navItems }) => {
  return (
    <>
      <div className={`${styles.sidebar} ${isOpen ? styles.open : ''}`}>
        <button className={styles.closeButton} onClick={onClose} aria-label="Close sidebar">
          &times;
        </button>
        <ul className={styles.sidebarNavList}>
          {navItems.map((item, index) => (
            <li key={index} className={styles.sidebarNavItem}>
              <a href={item.href} className={styles.sidebarNavLink} onClick={onClose}>
                {item.label}
              </a>
            </li>
          ))}
        </ul>
      </div>
      {isOpen && <div className={styles.backdrop} onClick={onClose}></div>}
    </>
  );
};

export default Sidebar;
