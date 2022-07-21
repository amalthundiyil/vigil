import React from "react";
import { ThemeProvider } from "@mui/material/styles";
import theme from "./theme";
import "typeface-roboto";
import { Container } from "@mui/material";
import { BrowserRouter } from "react-router-dom";
import Router from "./router";

const AppLayout = ({ children }) => {
  return (
    <ThemeProvider theme={theme}>
      <Container>
        <div>{children}</div>
      </Container>
    </ThemeProvider>
  );
};

const App = () => {
  return (
    <BrowserRouter>
      <Router />
    </BrowserRouter>
  );
};

export default App;
