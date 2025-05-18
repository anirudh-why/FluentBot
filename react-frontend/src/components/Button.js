import React from 'react';
import { motion } from 'framer-motion';

function Button({ children, onClick, className = '', variant = 'primary' }) {
  const baseClasses = 'px-6 py-3 rounded-lg font-semibold transition-all duration-300';
  const variantClasses = {
    primary: 'bg-blue-500 hover:bg-blue-600 text-white',
    secondary: 'bg-gray-500 hover:bg-gray-600 text-white',
    danger: 'bg-red-500 hover:bg-red-600 text-white'
  };

  return (
    <motion.button
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      onClick={onClick}
      className={`${baseClasses} ${variantClasses[variant]} ${className}`}
    >
      {children}
    </motion.button>
  );
}

export default Button;