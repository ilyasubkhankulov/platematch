import React, { useState } from "react";
import { Flex } from "@chakra-ui/react";
// import ImageUpload from "./ImageUpload";
import StreetMap from "./components/StreetMap";
import "./App.css";
// import MapExample from "./components/MapExample";
import SingleIncidentView from "./SingleIncidentView";

function App() {
  return (
    <>
      <Flex p={4}>
        <h1>Platematch</h1>
      </Flex>
      <Flex p={4}>
        <SingleIncidentView />
      </Flex>
      {/* <ImageUpload></ImageUpload> */}

      <StreetMap />
    </>
  );
}

export default App;
