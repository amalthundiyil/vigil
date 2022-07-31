import React, { useContext, createContext, useState } from "react";

const AppContext = createContext();

const AppProvider = ({ children }) => {
  const [loading, setLoading] = useState(false);
  const [metrics, setMetrics] = useState([]);
  const [backend, setBackend] = useState("");
  return (
    <AppContext.Provider
      value={{ loading, setLoading, metrics, setMetrics, backend, setBackend }}
    >
      {children}
    </AppContext.Provider>
  );
};

const useGlobalContext = () => {
  return useContext(AppContext);
};

export { AppContext, AppProvider, useGlobalContext };
