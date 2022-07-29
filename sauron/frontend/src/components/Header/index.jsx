import * as React from "react";
import { styled, alpha } from "@mui/material/styles";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import { Link } from "react-router-dom";
import logo from "../../assets/logo.png";
import Toolbar from "@mui/material/Toolbar";
import IconButton from "@mui/material/IconButton";
import Typography from "@mui/material/Typography";
import InputBase from "@mui/material/InputBase";
import MenuIcon from "@mui/icons-material/Menu";
import SearchIcon from "@mui/icons-material/Search";
import { CssBaseline } from "@mui/material";
import { useLocation, useNavigate } from "react-router-dom";
import { useGlobalContext } from "../../context";
import { useState } from "react";
import axios from "../../utils/axios";

const Search = styled("div")(({ theme }) => ({
  position: "relative",
  borderRadius: theme.shape.borderRadius,
  backgroundColor: alpha(theme.palette.common.white, 0.15),
  "&:hover": {
    backgroundColor: alpha(theme.palette.common.white, 0.25),
  },
  marginLeft: 0,
  width: "100%",
  [theme.breakpoints.up("sm")]: {
    marginLeft: theme.spacing(1),
    width: "auto",
  },
}));

const SearchIconWrapper = styled("div")(({ theme }) => ({
  padding: theme.spacing(0, 2),
  height: "100%",
  position: "absolute",
  pointerEvents: "none",
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
}));

const StyledInputBase = styled(InputBase)(({ theme }) => ({
  color: "inherit",
  "& .MuiInputBase-input": {
    padding: theme.spacing(1, 1, 1, 0),
    // vertical padding + font size from searchIcon
    paddingLeft: `calc(1em + ${theme.spacing(4)})`,
    transition: theme.transitions.create("width"),
    width: "100%",
    [theme.breakpoints.up("sm")]: {
      width: "12ch",
      "&:focus": {
        width: "20ch",
      },
    },
  },
}));

export default function Header() {
  const [searchQuery, setSearchQuery] = useState("");
  const { loading, setLoading, setMetrics } = useGlobalContext();
  const navigate = useNavigate();

  const handleChange = (value) => {
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
      setLoading(false);
      setMetrics(data);
      navigate("/dashboard");
    };
    fetchData(formData).catch(console.error);
  };

  const location = useLocation();
  return (
    <>
      <CssBaseline />
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="sticky" sx={{ bgcolor: "#1c1c44", mb: 3 }}>
          <Toolbar>
            <Toolbar component={Link} to="/home">
              <img src={logo} alt="logo" width={60} />
            </Toolbar>
            <Typography
              variant="h6"
              noWrap
              component="div"
              sx={{ flexGrow: 1, display: { xs: "none", sm: "block" } }}
            >
              Sauron
            </Typography>
            {!(location.pathname === "/home" || location.pathname === "/") && (
              <form onSubmit={(e) => handleSubmit(e)}>
                <Search>
                  <SearchIconWrapper>
                    <SearchIcon />
                  </SearchIconWrapper>
                  <StyledInputBase
                    placeholder="Search…"
                    onChange={(event) => handleChange(event.target.value)}
                    inputProps={{ "aria-label": "search" }}
                  />
                </Search>
              </form>
            )}
          </Toolbar>
        </AppBar>
      </Box>
    </>
  );
}
