import React from 'react';
import { motion } from 'framer-motion';
import { DocumentTextIcon, SpeakerWaveIcon } from '@heroicons/react/24/outline';

function Results({ results }) {
  if (!results) return null;

  const { original_text, corrected_text, audio_path } = results;

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 }
  };

  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="mt-8 space-y-6"
    >
      <motion.div
        variants={itemVariants}
        className="bg-gray-800/50 backdrop-blur-sm p-6 rounded-xl border border-gray-700/50"
      >
        <div className="flex items-center space-x-2 mb-3">
          <DocumentTextIcon className="w-5 h-5 text-blue-400" />
          <h3 className="text-lg font-semibold text-gray-200">Original Text</h3>
        </div>
        <p className="text-gray-300 leading-relaxed">{original_text}</p>
      </motion.div>

      <motion.div
        variants={itemVariants}
        className="bg-purple-900/30 backdrop-blur-sm p-6 rounded-xl border border-purple-700/50"
      >
        <div className="flex items-center space-x-2 mb-3">
          <DocumentTextIcon className="w-5 h-5 text-purple-400" />
          <h3 className="text-lg font-semibold text-gray-200">Corrected Text</h3>
        </div>
        <p className="text-gray-300 leading-relaxed">{corrected_text}</p>
      </motion.div>

      {audio_path && (
        <motion.div
          variants={itemVariants}
          className="bg-gray-800/50 backdrop-blur-sm p-6 rounded-xl border border-gray-700/50"
        >
          <div className="flex items-center space-x-2 mb-4">
            <SpeakerWaveIcon className="w-5 h-5 text-green-400" />
            <h3 className="text-lg font-semibold text-gray-200">Corrected Audio</h3>
          </div>
          <audio 
            controls 
            className="w-full rounded-lg bg-gray-700/50"
            src={`http://localhost:8000/static/${audio_path}`}
          >
            Your browser does not support the audio element.
          </audio>
        </motion.div>
      )}
    </motion.div>
  );
}

export default Results; 