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
          <span className="info">{data.score_data.description[0]}</span>
          <ProgressBar value={data.score_data.score[0]} />
        </div>
        <div className="comm-features">
          <span>Org count</span>
          <span className="info">{data.score_data.description[1]}</span>
          <ProgressBar value={data.score_data.score[1]} />
        </div>
        <div className="comm-features">
          <span>Contributor count</span>
          <span className="info">{data.score_data.description[2]}</span>
          <ProgressBar value={data.score_data.score[2]} />
        </div>
        <div className="comm-features">
          <span>License</span>
          <span className="info">{data.score_data.description[3]}</span>
          <ProgressBar value={data.score_data.score[3]} />
        </div>
        <div className="comm-features">
          <span>Code of conduct</span>
          <span className="info">{data.score_data.description[4]}</span>
          <ProgressBar value={data.score_data.score[4]} />
        </div>
        <div className="comm-features">
          <span>Bus factor</span>
          <span className="info">{data.score_data.description[5]}</span>
          <ProgressBar value={data.score_data.score[5]} />
        </div>
      </div>
      <div className="featuredItem">
        <span className="featuredTitle">Security</span>
        <div className="comm-features">
          <span>Branch protection</span>
          <span className="info">{securityData.score_data.description[1]}</span>
          <ProgressBar value={securityData.score_data.score[1]} />
        </div>
        <div className="comm-features">
          <span>Code review</span>
          <span className="info">{securityData.score_data.description[4]}</span>
          <ProgressBar value={securityData.score_data.score[4]} />
        </div>
        <div className="comm-features">
          <span>Dangerous workflows</span>
          <span className="info">{securityData.score_data.description[6]}</span>
          <ProgressBar value={securityData.score_data.score[6]} />
        </div>
        <div className="comm-features">
          <span>Security policy</span>
          <span className="info">{securityData.score_data.description[14]}</span>
          <ProgressBar value={securityData.score_data.score[14]} />
        </div>
        <div className="comm-features">
          <span>Vulnerabilities</span>
          <span className="info">{securityData.score_data.description[17]}</span>
          <ProgressBar value={securityData.score_data.score[17]} />
          
        </div>
      </div>
    </div>
  );
}

export default Community;
