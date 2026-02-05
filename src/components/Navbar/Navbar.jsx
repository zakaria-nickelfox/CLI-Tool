import React from 'react';
import styles from './Navbar.module.css';

/**
 * A responsive Navbar component.
 * @param {object} props - The component props.
 * @param {string} props.brandName - The brand name or logo text to display.
 * @param {Array<object>} props.navItems - An array of navigation items, e.g., [{ label: 'Home', href: '/' }].
 * @param {function} [props.onMenuClick] - Optional click handler for a mobile menu button.
 */
const Navbar = ({ brandName, navItems, onMenuClick }) => {
  return (
    <nav className={styles.navbar}>
      <div className={styles.brand}>
        <a href="/" className={styles.brandLink}>{brandName}</a>
      </div>
      <ul className={styles.navList}>
        {navItems.map((item, index) => (
          <li key={index} className={styles.navItem}>
            <a href={item.href} className={styles.navLink}>{item.label}</a>
          </li>
        ))}
      </ul>
      <button className={styles.menuButton} onClick={onMenuClick} aria-label="Open menu">
        &#9776;
      </button>
    </nav>
  );
};

export default Navbar;
