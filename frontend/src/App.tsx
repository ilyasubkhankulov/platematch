import React, { useState } from 'react'
import { Flex } from '@chakra-ui/react'
// import ImageUpload from './ImageUpload'
import SingleIncidentView from './SingleIncidentView'
import './App.css'


function App() {

  return (
    <>
      <Flex p={4}>
        <h1>Platematch</h1>
      </Flex>
      <Flex p={4}>
        <SingleIncidentView />
      </Flex>
    </>
  )
}

export default App
