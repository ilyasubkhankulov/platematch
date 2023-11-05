import React from "react";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import App from "./App";
import { ChakraProvider } from "@chakra-ui/react";
import SingleIncidentView from "./SingleIncidentView";
import StreetMap from "./components/StreetMap";
import "./index.css";

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children:[
      { path: "/",
        element: <StreetMap />
      },
      {
        path: "/incident/:id",
        element: <SingleIncidentView />
      }
    ]
  }
])


ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <ChakraProvider>
      <RouterProvider router={router}/>
    </ChakraProvider>
  </React.StrictMode>
);
