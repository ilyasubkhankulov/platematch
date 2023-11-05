import React, { useState } from "react";
import { Flex, Heading, Image } from "@chakra-ui/react";
import { Outlet, Link } from "react-router-dom";
// import ImageUpload from "./ImageUpload";
import "./App.css";
// import MapExample from "./components/MapExample";

function App() {
  return (
    <>
      <Flex p={4}>
        <Heading as={Link} to="/">
          <Image src="/public/logo.svg" />
        </Heading>
      </Flex>
      <Flex p={4}>
        <Outlet />
      </Flex>
    </>
  );
}

export default App;
