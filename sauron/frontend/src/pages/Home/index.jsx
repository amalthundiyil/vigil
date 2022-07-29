import React from "react";
import BasicCard from "../../components/BasicCard";
import SearchBar from "../../components/SearchBar";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import GridWrapper from "../../components/GridWrapper";
import { cardHeaderStyles } from "./styles";
import { useState } from "react";
import { NavLink } from "react-router-dom";
import axios from "../../utils/axios";

const filterData = (query, data) => {
  if (!query) {
    return [{ slug: "no-packages-found", title: "No packages found" }];
  } else {
    return data.filter((d) =>
      d.title.toLowerCase().includes(query.toLowerCase())
    );
  }
};

const Home = ({ data }) => {
  const [searchQuery, setSearchQuery] = useState("");
  const dataFiltered = filterData(searchQuery, data);

  const getHeader = () => {
    const handleChange = (value) => {
      console.log(value);
      setSearchQuery(value);
    };

    const handleSubmit = (e) => {
      e.preventDefault();
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
      };
      fetchData(formData).catch(console.error);
    };

    return (
      <Box sx={cardHeaderStyles.wrapper}>
        <SearchBar
          placeholder="Search by package title"
          onChange={(event) => handleChange(event.target.value)}
          onSubmit={(event) => handleSubmit(event)}
          searchBarWidth="720px"
        />
      </Box>
    );
  };

  const getContent = () =>
    dataFiltered.map((d) => {
      if (d.slug === "no-packages-found") {
        return (
          <Typography
            key={d.slug}
            align="center"
            sx={{
              margin: "40px 16px",
              color: "rgba(0, 0, 0, 0.6)",
              fontSize: "1.3rem",
            }}
          >
            {d.title}
          </Typography>
        );
      }

      return (
        <NavLink to={`/packages/${d.slug}`} key={d.slug}>
          <Typography
            key={d.slug}
            align="center"
            sx={{
              margin: "40px 16px",
              color: "rgba(0, 0, 0, 0.6)",
              fontSize: "1.3rem",
            }}
          >
            {d.title}
          </Typography>
        </NavLink>
      );
    });

  return (
    <GridWrapper>
      <BasicCard header={getHeader()} content={getContent()} />
    </GridWrapper>
  );
};

export default Home;
