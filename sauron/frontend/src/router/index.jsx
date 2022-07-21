import { Suspense } from "react";
import { Routes, Route } from "react-router-dom";
import React from "react";
import Error from "../pages/Error";
import Home from "../pages/Home";

const Router = () => {
  return (
    <Suspense fallback={null}>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="*" element={<Error />} />
      </Routes>
    </Suspense>
  );
};

export default Router;
