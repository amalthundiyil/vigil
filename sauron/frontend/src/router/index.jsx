import { Suspense } from "react";
import { Routes, Route } from "react-router-dom";
import React from "react";
import Error from "../pages/Error";
import Home from "../pages/Home";
import Header from "../components/Header";
import Dashboard from "../pages/Dashboard";

const Router = () => {
  return (
    <Suspense fallback={null}>
      <Header />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="*" element={<Error />} />
      </Routes>
    </Suspense>
  );
};

export default Router;
