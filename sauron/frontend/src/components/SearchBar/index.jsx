import React from "react";
import SearchIcon from "@mui/icons-material/Search";
import Input from "@mui/material/Input";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import SendIcon from "@mui/icons-material/Send";
import IconButton from "@mui/material/IconButton";

const SearchBar = ({ placeholder, onChange, onSubmit, searchBarWidth }) => {
  return (
    <Box sx={{ display: "flex", alignItems: "center" }}>
      <form onSubmit={onSubmit}>
        <IconButton aria-label="delete" type="submit">
          <SearchIcon />
        </IconButton>
        <Input
          id="search"
          placeholder={placeholder}
          onChange={onChange}
          sx={{
            width: searchBarWidth,
            color: "rgba(0, 0, 0, 0.6)",
            fontSize: "1.1rem",
          }}
          disableUnderline
        />
      </form>
    </Box>
  );
};

export default SearchBar;
