import React from "react";
import "./styles.css";
import { ArrowDownward, ArrowUpward } from "@mui/icons-material";
import Spinner from "../Spinner";
import { capitalizeFirstLetter } from "../../utils/utils";
import ProgressBar from "../ProgressBar";

function PackageInfo({ metrics }) {
  const data = metrics.data.data;

  console.log(data);

  return (
    <div className="featured">
      <div className="featuredItem">
        <span className="featuredTitle">Package Info</span>
        <div className="featuredMoneyContainer">
          <span className="featuredMoney">{data["name"]}</span>
          {/* <span className="featuredMoneyRate">v2.0</span> */}
        </div>
        <span className="featuredSub">{data["description"]}</span>
      </div>
      <div className="featuredItem">
        <span className="featuredTitle">Health Score</span>
        <div className="featuredMoneyContainer">
          <span className="featuredMoney">{data["final_score"]} / 10</span>
          <ProgressBar value={data["final_score"]} />
        </div>
        <span className="featuredSub">{data["final_desc"]}</span>
      </div>
    </div>
  );
}

export default PackageInfo;
