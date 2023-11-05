import React, { useState } from "react";
import { Flex, } from "@chakra-ui/react";
import { Outlet, Link } from "react-router-dom";
// import ImageUpload from "./ImageUpload";
// import StreetMap from "./components/StreetMap";
import "./App.css";
// import Map from "./components/Map";
// import SingleIncidentView from "./SingleIncidentView";

function App() {
  return (
    <>
      <Flex p={4}>
        <h1>
          <Link to="/">Platematch</Link>
        </h1>
      </Flex>
      <Flex p={4}>
        <Outlet />
      </Flex>
      {/* <ImageUpload></ImageUpload> */}
      {/* <StreetMap /> */}
      {/* <Map></Map> */}
    </>
  );
}

export default App;
