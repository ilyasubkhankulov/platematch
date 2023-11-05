import React, { useState } from 'react';
import { 
    Button, 
    Flex, 
    Spacer, 
    Table,
    Thead,
    Tbody,
    Tr,
    Th,
    Td,
    TableContainer,
    VStack,
    Image, } from '@chakra-ui/react';
import { CarMatch, MatchResult } from './types';
import axios from 'axios';

const url = 'http://localhost:8000/upload/';

// Function to get the enum name as a string
function getMatchResultName(value: number): string {
    return MatchResult[value] as string;
}

function getMatchResultColor(value: number): string {
    switch (value) {
        case MatchResult.MATCH:
            return "green";
        case MatchResult.MISMATCH:
            return "red";
        case MatchResult.INVALID_PLATE:
            return "red";
        case MatchResult.INDETERMINATE:
            return "yellow";
        default:
            return "white";
    }
}

const ImageUpload = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [matchResponse, setMatchResponse] = useState<CarMatch|null>(null);
  const [loading, setLoading] = useState(false);

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
    // formData.append('metadata', "test")
    setLoading(true);
    try {
        const response = await axios.post(url, formData, {
            headers: {
            'Content-Type': 'multipart/form-data'
            }
        });
        // Handle response here
        setLoading(false);
        setMatchResponse(response.data);
        console.log(response.data);
    } catch (error) {
        // Handle error here
        console.error(error);
        setLoading(false);
        alert('Error uploading image!');
    }
  }; 

  return (
    <VStack>
        <Flex p={4}>
        <input type="file" accept="*" onChange={handleFileSelect} />
        <Spacer p={8} />
        <Button onClick={handleUpload} isLoading={loading}>Assess Car Match</Button>
        <Spacer p={4} />
        </Flex>
        <Flex>
        {selectedFile ? 
            <Image src={URL.createObjectURL(selectedFile)} alt="Image Preview" boxSize="300px" />
        : null}
        </Flex>
        <Flex p={4}>
        {matchResponse ? 
            <TableContainer>
                <Table variant='simple'>
                    <Thead>
                    <Tr>
                        <Th>Attribute</Th>
                        <Th>Car Value</Th>
                        <Th>Plate Value</Th>
                        <Th>Status</Th>
                    </Tr>
                    </Thead>
                    <Tbody>
                    <Tr>
                        <Td>Make</Td>
                        <Td>{matchResponse.make_result.car_value}</Td>
                        <Td>{matchResponse.make_result.plate_value}</Td>
                        <Td bgColor={getMatchResultColor(matchResponse.make_result.match_result)}>{getMatchResultName(matchResponse.make_result.match_result)}</Td>
                    </Tr>
                    <Tr>
                        <Td>Model</Td>
                        <Td>{matchResponse.model_result.car_value}</Td>
                        <Td>{matchResponse.model_result.plate_value}</Td>
                        <Td bgColor={getMatchResultColor(matchResponse.model_result.match_result)}>{getMatchResultName(matchResponse.model_result.match_result)}</Td>
                    </Tr>
                    <Tr>
                        <Td>Year</Td>
                        <Td>{matchResponse.year_result.car_value}</Td>
                        <Td>{matchResponse.year_result.plate_value}</Td>
                        <Td bgColor={getMatchResultColor(matchResponse.year_result.match_result)}>{getMatchResultName(matchResponse.year_result.match_result)}</Td>
                    </Tr>
                    <Tr>
                        <Td>Color</Td>
                        <Td>{matchResponse.color_result.car_value}</Td>
                        <Td>{matchResponse.color_result.plate_value}</Td>
                        <Td bgColor={getMatchResultColor(matchResponse.color_result.match_result)}>{getMatchResultName(matchResponse.color_result.match_result)}</Td>
                    </Tr>
                    </Tbody>
                </Table>
            </TableContainer>
        : null}
        </Flex>
    </VStack>
  );
};

export default ImageUpload;