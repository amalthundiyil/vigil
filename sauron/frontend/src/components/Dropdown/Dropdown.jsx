import React from "react";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select, { SelectChangeEvent } from "@mui/material/Select";
import { useGlobalContext } from "../../context";

export default function Dropdown() {
  const { backend, setBackend } = useGlobalContext();

  const handleChange = (event) => {
    setBackend(event.target.value);
  };

  return (
    <FormControl sx={{ minWidth: 120 }} size="small">
      <InputLabel id="demo-select-small">Select</InputLabel>
      <Select
        labelId="demo-select-small"
        id="demo-select-small"
        value={backend}
        label="Backend"
        onChange={handleChange}
      >
        <MenuItem value="github">Github</MenuItem>
        <MenuItem value="npm">NPM</MenuItem>
        <MenuItem value="pypi">PyPi</MenuItem>
      </Select>
    </FormControl>
  );
}
