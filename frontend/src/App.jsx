import React, { useState } from "react";
import { Flex, } from "@chakra-ui/react";
import { Outlet, Link } from "react-router-dom";
// import ImageUpload from "./ImageUpload";
import "./App.css";
// import MapExample from "./components/MapExample";

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
    </>
  );
}

export default App;
