import React from "react";
import { userData } from "../../dummyData";
import Barchart from "../Charts/Barchart";
import Chart from "../Charts/Chart";
import "./styles.css";

function PackageStats() {
  return (
    <div>
      <div className="chart-container">
        <Chart data={userData} title="Popularity" grid dataKey="Downloads" />
        <Barchart></Barchart>
      </div>
    </div>
  );
}

export default PackageStats;
