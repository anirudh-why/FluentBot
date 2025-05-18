import React from 'react';

function About() {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold text-center mb-8 text-indigo-600">About</h1>
      <div className="max-w-2xl mx-auto bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-semibold mb-4">Grammar Correction Assistant</h2>
        <p className="text-gray-700 mb-4">
          This application helps you improve your grammar by analyzing your speech and providing corrections.
          It uses advanced natural language processing techniques to identify and fix grammatical errors.
        </p>
        <h3 className="text-xl font-semibold mb-2">Features:</h3>
        <ul className="list-disc list-inside text-gray-700 space-y-2">
          <li>Record audio directly in your browser</li>
          <li>Upload audio files in various formats</li>
          <li>Get instant grammar corrections</li>
          <li>Listen to the corrected version</li>
        </ul>
      </div>
    </div>
  );
}

export default About; 