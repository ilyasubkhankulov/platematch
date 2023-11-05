import React, { useState } from 'react';
import { Button, Flex, Spacer } from '@chakra-ui/react';
import axios from 'axios';

const url = 'http://localhost:8000/license-plate-ocr/';

const ImageUpload = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [licensePlate, setLicensePlate] = useState("");

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
        setLicensePlate(response.data);
      console.log(response.data);
    } catch (error) {
      // Handle error here
      console.error(error);
      alert('Error uploading image!');
    }
  };

  return (
    <Flex p={4}>
      <input type="file" accept="*" onChange={handleFileSelect} />
      <Button onClick={handleUpload}>Extract License Plate #</Button>
      <Spacer p={4} />
      {licensePlate ? <p>{licensePlate.toUpperCase()}</p> : null}
    </Flex>
  );
};

export default ImageUpload;