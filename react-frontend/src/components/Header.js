import React from 'react';
import { motion } from 'framer-motion';

function Header() {
    return (
        <motion.header
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-gray-800/50 backdrop-blur-lg border-b border-gray-700/50"
        >
            <div className="container mx-auto px-4 py-4">
                <h1 className="text-2xl font-bold text-white">AI Grammar Assistant</h1>
            </div>
        </motion.header>
    );
}

export default Header;