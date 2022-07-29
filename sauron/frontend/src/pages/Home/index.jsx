import React from "react";
import BasicCard from "../../components/BasicCard";
import SearchBar from "../../components/SearchBar";
import Spinner from "../../components/Spinner";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import GridWrapper from "../../components/GridWrapper";
import { cardHeaderStyles } from "./styles";
import { useState } from "react";
import { useGlobalContext } from "../../context";
import { useNavigate } from "react-router-dom";
import { NavLink } from "react-router-dom";
import axios from "../../utils/axios";

const Home = ({ data }) => {
  const [searchQuery, setSearchQuery] = useState("");
  const { loading, setLoading, setMetrics } = useGlobalContext();
  const navigate = useNavigate();

  const getHeader = () => {
    const handleChange = (value) => {
      console.log(value);
      setSearchQuery(value);
    };

    const handleSubmit = (e) => {
      e.preventDefault();
      setLoading(true);
      let formData = new FormData(e.target);
      formData.append("search", searchQuery);
      const fetchData = async (formData) => {
        const payload = {
          url: formData.get("search"),
          github_token: formData.get("github_token"),
        };
        const data = await axios.post("/api/dashboard/", payload, {
          "Content-Type": "application/json",
        });
        console.log(data);
        setLoading(false);
        setMetrics(data);
        navigate("/dashboard");
      };
      fetchData(formData).catch(console.error);
    };
    console.log(loading);

    return (
      <>
        {loading && <Spinner open={true} />}
        <Box sx={cardHeaderStyles.wrapper}>
          <SearchBar
            placeholder="Search by package title"
            onChange={(event) => handleChange(event.target.value)}
            onSubmit={(event) => handleSubmit(event)}
            searchBarWidth="720px"
          />
        </Box>
      </>
    );
  };

  return (
    <GridWrapper>
      <BasicCard header={getHeader()} />
    </GridWrapper>
  );
};

export default Home;
