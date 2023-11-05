import React, { useState } from "react";
import { Flex, Heading } from "@chakra-ui/react";
import { Outlet, Link } from "react-router-dom";
// import ImageUpload from "./ImageUpload";
import "./App.css";
// import MapExample from "./components/MapExample";

function App() {
  return (
    <>
      <Flex p={4}>
        <Heading as={Link} to="/">
          Platematch
        </Heading>
      </Flex>
      <Flex p={4}>
        <Outlet />
      </Flex>
    </>
  );
}

export default App;
