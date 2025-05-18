import React from 'react';

function FileUploader({ onResults, setLoading }) {
  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('audio', file);

    try {
      const response = await fetch('http://localhost:8000/process-audio', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      onResults(data);
    } catch (error) {
      console.error('Error processing file:', error);
      setLoading(false);
    }
  };

  return (
    <div className="text-center">
      <label className="block">
        <span className="sr-only">Choose audio file</span>
        <input
          type="file"
          accept="audio/*"
          onChange={handleFileUpload}
          className="block w-full text-sm text-gray-500
            file:mr-4 file:py-2 file:px-4
            file:rounded-full file:border-0
            file:text-sm file:font-semibold
            file:bg-indigo-50 file:text-indigo-700
            hover:file:bg-indigo-100"
        />
      </label>
    </div>
  );
}

export default FileUploader; 