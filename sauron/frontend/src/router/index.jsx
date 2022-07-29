import { Routes, Route } from "react-router-dom";
import { Suspense, useState, useEffect } from "react";
import React from "react";
import Error from "../pages/Error";
import Home from "../pages/Home";
import Header from "../components/Header";
import Dashboard from "../pages/Dashboard";
import axios from "../utils/axios";

const Router = () => {
  const [allPackages, setAllPackages] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const data = await axios.get("/api/home");
    };
    fetchData().catch(console.error);
  }, []);

  return (
    <Suspense fallback={null}>
      <Header />
      <Routes>
        {/* <Route path="/" element={<Home data={allPackages} />} /> */}
        {/* <Route path="/dashboard" element={<Dashboard />} /> */}
        <Route path="*" element={<Error />} />
      </Routes>
    </Suspense>
  );
};

export default Router;
