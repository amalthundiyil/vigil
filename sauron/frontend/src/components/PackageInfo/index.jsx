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
        <div className="featuredSub">{"Popularity score: "+data["popularity"]["summary"]["score"]}</div>
        <div className="featuredSub">{"Maintainance score: "+data["maintainence"]["summary"]["score"]}</div>
        <div className="featuredSub">{"Community score: "+data["community"]["summary"]["score"]}</div>
        <div className="featuredSub">{"Security score: "+data["security"]["summary"]["score"]}</div>
      </div>
    </div>
  );
}

export default PackageInfo;
