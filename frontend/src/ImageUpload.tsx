import React, { useState } from 'react';
import { Button } from '@chakra-ui/react';
import axios from 'axios';

const url = 'http://localhost:8000/upload/';

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
    formData.append('image', selectedFile);
    formData.append('metadata', "test")

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
      <input type="file" accept="*" onChange={handleFileSelect} />
      <Button onClick={handleUpload}>Upload Image</Button>
    </div>
  );
};

export default ImageUpload;