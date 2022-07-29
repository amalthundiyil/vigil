import * as React from "react";
import { styled } from "@mui/material/styles";
import Paper from "@mui/material/Paper";
import Grid from "@mui/material/Grid";
import Spinner from "../../components/Spinner";
import Box from "@mui/material/Box";
import { useGlobalContext } from "../../context";
import { useNavigate } from "react-router-dom";
import { NavLink } from "react-router-dom";
import axios from "../../utils/axios";

const Item = styled(Paper)(({ theme }) => ({
  backgroundColor: theme.palette.mode === "dark" ? "#1A2027" : "#fff",
  ...theme.typography.body2,
  padding: theme.spacing(1),
  textAlign: "center",
  color: theme.palette.text.secondary,
}));

export default function Dashboard() {
  const { loading, setLoading, metrics, setMetrics } = useGlobalContext();

  console.log(metrics);

  if (loading) {
    return <Spinner open={true} />;
  }

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Grid container spacing={2}>
        <Grid item xs={8}>
          <Item>xs=8</Item>
        </Grid>
        <Grid item xs={4}>
          <Item>xs=4</Item>
        </Grid>
      </Grid>
    </Box>
  );
}
