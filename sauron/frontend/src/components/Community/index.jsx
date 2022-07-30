import React from "react";
import "./styles.css";
import { Block, Close, Done } from "@mui/icons-material";
import ProgressBar from "../ProgressBar";
function Community({ metrics }) {
  const data = metrics["data"]["data"]["community"];
  const securityData = metrics["data"]["data"]["security"];
  return (
    <div className="featured">
      <div className="featuredItem">
        <span className="featuredTitle">Community</span>
        <div className="comm-features">
          <span>Maintainer Count</span>
          <ProgressBar value={data.score_data.score[0]} />
        </div>
        <div className="comm-features">
          <span>Org count</span>
          <ProgressBar value={data.score_data.score[1]} />
        </div>
        <div className="comm-features">
          <span>Contributor count</span>
          <ProgressBar value={data.score_data.score[2]} />
        </div>
        <div className="comm-features">
          <span>License</span>
          <ProgressBar value={data.score_data.score[3]} />
        </div>
        <div className="comm-features">
          <span>Code of conduct</span>
          <ProgressBar value={data.score_data.score[4]} />
        </div>
        <div className="comm-features">
          <span>Bus factor</span>
          <ProgressBar value={data.score_data.score[5]} />
        </div>
      </div>
      <div className="featuredItem">
        <span className="featuredTitle">Security</span>
        <div className="comm-features">
          <span>Branch protection</span>
          <ProgressBar value={securityData.score_data.score[1]} />
        </div>
        <div className="comm-features">
          <span>Code review</span>
          <ProgressBar value={securityData.score_data.score[4]} />
        </div>
        <div className="comm-features">
          <span>Dangerous workflows</span>
          <ProgressBar value={securityData.score_data.score[6]} />
        </div>
        <div className="comm-features">
          <span>Security policy</span>
          <ProgressBar value={securityData.score_data.score[14]} />
        </div>
        <div className="comm-features">
          <span>Vulnerabilities</span>
          <ProgressBar value={securityData.score_data.score[17]} />
        </div>
      </div>
    </div>
  );
}

export default Community;
