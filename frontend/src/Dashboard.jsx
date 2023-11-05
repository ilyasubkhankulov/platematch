import React, { useState, useEffect } from "react";
import StreetMap from "./components/StreetMap";
import IncidentTable from "./components/IncidentTable";
import axios from "axios";

const API_HOST = "http://localhost:8000";

const url = `${API_HOST}/incidents`;

const Dashboard = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const result = await axios(url);
      setData(result.data);
    };
    fetchData();
  }, []);

  return (
    <div className="flex flex-col">
      <StreetMap data={data} />
      <IncidentTable data={data} />
    </div>
  );
};

export default Dashboard;
