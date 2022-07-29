import axios from "axios";

// const instance = axios.create({
//   baseURL: `${process.env.REACT_APP_SCHEME}://${process.env.REACT_APP_HOST}:${process.env.REACT_APP_PORT}`,
// });

const instance = axios.create({
  baseURL: `http://localhost:5000`,
});

export default instance;
