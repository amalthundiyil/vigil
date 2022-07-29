import React, { useContext, createContext, useState } from "react";

const AppContext = createContext();

const AppProvider = ({ children }) => {
  const [loading, setLoading] = useState(false);
  const [metrics, setMetrics] = useState([]);
  return (
    <AppContext.Provider value={{ loading, setLoading, metrics, setMetrics }}>
      {children}
    </AppContext.Provider>
  );
};

const useGlobalContext = () => {
  return useContext(AppContext);
};

export { AppContext, AppProvider, useGlobalContext };
