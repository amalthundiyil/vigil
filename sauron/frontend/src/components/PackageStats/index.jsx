import React from "react";
import { userData } from "../../dummyData";
import Barchart from "../Charts/Barchart";
import Chart from "../Charts/Chart";
import Spinner from "../Spinner";
import "./styles.css";

function PackageStats({ metrics }) {
  const data = metrics["data"]["data"];
  console.log(data);
  return (
    <div>
      <div className="chart-container">
        <Chart
          data={data["popularity"]["ts_data"]}
          title="Popularity"
          grid
          dataKey="Downloads"
        />
        <Barchart data={data["maintainence"]["commit_frequency"]} />
      </div>
    </div>
  );
}

export default PackageStats;
