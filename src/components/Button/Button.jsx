import React from 'react';
import styles from './Button.module.css';

/**
 * A reusable Button component.
 * @param {object} props - The component props.
 * @param {function} props.onClick - Function to call on button click.
 * @param {'primary' | 'secondary'} [props.variant='primary'] - The visual style variant of the button.
 * @param {boolean} [props.disabled=false] - If true, the button will be disabled.
 * @param {React.ReactNode} props.children - The content to display inside the button.
 */
const Button = ({ onClick, children, variant = 'primary', disabled = false }) => {
  const buttonClassName = `${styles.button} ${styles[variant]} ${disabled ? styles.disabled : ''}`;

  return (
    <button className={buttonClassName} onClick={onClick} disabled={disabled}>
      {children}
    </button>
  );
};

export default Button;
