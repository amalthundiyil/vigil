import React from 'react'
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select, { SelectChangeEvent } from '@mui/material/Select';

function Dropdown() {
  return (
    <div>
    <FormControl sx={{ m: 1, minWidth: 120 }} size="small">
      <InputLabel id="demo-select-small">Select</InputLabel>
      <Select
        labelId="demo-select-small"
        id="demo-select-small"
        label="Type"
      >
        <MenuItem>Github</MenuItem>
        <MenuItem>NPM</MenuItem>
        <MenuItem>PyPi</MenuItem>
      </Select>
    </FormControl>
    </div>
  )
}

export default Dropdown