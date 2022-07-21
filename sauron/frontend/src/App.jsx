import React from "react";
import { makeStyles, ThemeProvider } from "@mui/material/styles";
import theme from "./theme";
import "typeface-roboto";
import { Container } from "@mui/material";
import { BrowserRouter } from "react-router-dom";
import Router from "./router";

const useStyles = makeStyles((theme) => ({
  root: {
    padding: 32,
  },
}));

const AppLayout = ({ children }) => {
  const classes = useStyles();
  return (
    <ThemeProvider theme={theme}>
      <Container>
        <div className={classes.root}>
          <div>{children}</div>
        </div>
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
