import React, { useState } from 'react';
import axios from 'axios';

const url = 'http://localhost:8000/upload';

const ImageUpload = () => {
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileSelect = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert('Please select a file first!');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await axios.post(url, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      // Handle response here
      console.log(response.data);
      alert('Image uploaded successfully!');
    } catch (error) {
      // Handle error here
      console.error(error);
      alert('Error uploading image!');
    }
  };

  return (
    <div>
      <input type="file" accept="image/*" onChange={handleFileSelect} />
      <button onClick={handleUpload}>Upload Image</button>
    </div>
  );
};

export default ImageUpload;