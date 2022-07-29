import axios from "axios";

const SCHEME =
  process.env.NODE_ENV == "development" ? "http" : process.env.REACT_APP_SCHEME;
const HOST =
  process.env.NODE_ENV == "development"
    ? "localhost"
    : process.env.REACT_APP_HOST;
const PORT =
  process.env.NODE_ENV == "development" ? "5000" : process.env.REACT_APP_PORT;

const instance = axios.create({
  baseURL: `${SCHEME}://${HOST}:${PORT}`,
});

export default instance;
