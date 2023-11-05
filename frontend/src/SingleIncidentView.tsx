import React, { useState, useEffect } from 'react';
import { 
    Spinner, 
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
import { useParams } from 'react-router-dom';
import { CarMatch, MatchResult } from './types';
import axios from 'axios';

const url = 'http://localhost:8000/incident-report/';

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

const SingleIncidentView = () => {
  const [matchResponse, setMatchResponse] = useState<CarMatch|null>(null);
  const [carImageSrc, setCarImageSrc] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const { id } = useParams();

  const handleLoad = async () => {

    const formData = new FormData();
    formData.append("id", id!)
    setLoading(true);
    try {
        const response = await axios.post(url, formData, {
            headers: {
            'Content-Type': 'multipart/form-data'
            },
        });
        const imageData = response.data.image;
        const matchData = response.data.info;
        // Handle response here
        setLoading(false);
        // setMatchResponse(response.data);
        console.log(response.data);
        setCarImageSrc(`data:image/jpeg;base64,${imageData}`);
        setMatchResponse(matchData);
    } catch (error) {
        // Handle error here
        console.error(error);
        setLoading(false);
    }
  }; 

  useEffect(()=> {
    if (id) {
        handleLoad();
    }
  }, [id])

  return (
    <VStack>
        <Flex p={4}>
        <Spacer p={4} />
        </Flex>
        <Flex>
        {loading ? 
            <Spinner size="xl" /> : null
        }
        {carImageSrc ? 
            <Image src={carImageSrc} alt="Image Preview" boxSize="300px" />
        : null}
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
                    </Tbody>
                </Table>
            </TableContainer>
        : null}
        </Flex>
    </VStack>
  );
};

export default SingleIncidentView;