import * as React from "react";
import { styled } from "@mui/material/styles";
import Paper from "@mui/material/Paper";
import Grid from "@mui/material/Grid";
import Spinner from "../../components/Spinner";
import Box from "@mui/material/Box";
import { useGlobalContext } from "../../context";
import { useNavigate } from "react-router-dom";
import { useEffect } from "react";
import { NavLink } from "react-router-dom";
import axios from "../../utils/axios";
import PackageStats from "../../components/PackageStats";
import PackageInfo from "../../components/PackageInfo";
import Community from "../../components/Community";
// import metrics from "../../data.json";

const Item = styled(Paper)(({ theme }) => ({
  backgroundColor: theme.palette.mode === "dark" ? "#1A2027" : "#fff",
  ...theme.typography.body2,
  padding: theme.spacing(1),
  textAlign: "center",
  color: theme.palette.text.secondary,
}));

export default function Dashboard() {
  const { loading, setLoading, metrics, setMetrics } = useGlobalContext();
  const navigate = useNavigate();

  useEffect(() => {
    if (loading || metrics.length <= 0) {
      navigate("/");
    }
  }, []);

  if (!loading && !metrics.length > 0) {
    navigate("/");
  }

  if (metrics.length <= 0) {
    return <Spinner open={true} />;
  }

  return (
    <Box sx={{ flexGrow: 1 }}>
      <PackageInfo metrics={metrics} />
      <PackageStats metrics={metrics} />
      <Community metrics={metrics} />
    </Box>
  );
}
