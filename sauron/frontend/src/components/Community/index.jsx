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
          <div className="desc">
            <span>Maintainer Count</span>
            <span className="info">{data.score_data.description[0]}</span>
          </div>
          <ProgressBar value={data.score_data.score[0]} />
        </div>
        <div className="comm-features">
          <div className="desc">
            <span>Org count</span>
            <span className="info">{data.score_data.description[1]}</span>
          </div>
          <ProgressBar value={data.score_data.score[1]} />
        </div>
        <div className="comm-features">
          <div className="desc">
            <span>Contributor count</span>
            <span className="info">{data.score_data.description[2]}</span>
          </div>
          <ProgressBar value={data.score_data.score[2]} />
        </div>
        <div className="comm-features">
          <div className="desc">
            <span>License</span>
            <span className="info">{data.score_data.description[3]}</span>
          </div>
          <ProgressBar value={data.score_data.score[3]} />
        </div>
        <div className="comm-features">
          <div className="desc">
          <span>Code of conduct</span>
          <span className="info">{data.score_data.description[4]}</span>
          </div>
          <ProgressBar value={data.score_data.score[4]} />
        </div>
        <div className="comm-features">
          <div className="desc">
            <span>Bus factor</span>
            <span className="info">{data.score_data.description[5]}</span>
          </div>
          <ProgressBar value={data.score_data.score[5]} />
        </div>
      </div>
      <div className="featuredItem">
        <span className="featuredTitle">Security</span>
        <div className="comm-features">
          <div className="desc">
            <span>Branch protection</span>
            <span className="info">{securityData.score_data.description[1]}</span>
          </div>
          <ProgressBar value={securityData.score_data.score[1]} />
        </div>
        <div className="comm-features">
          <div className="desc">
            <span>Code review</span>
            <span className="info">{securityData.score_data.description[4]}</span>
          </div>
          <ProgressBar value={securityData.score_data.score[4]} />
        </div>
        <div className="comm-features">
          <div className="desc">
            <span>Dangerous workflows</span>
            <span className="info">{securityData.score_data.description[6]}</span>
          </div>
          <ProgressBar value={securityData.score_data.score[6]} />
        </div>
        <div className="comm-features">
          <div className="desc">
            <span>Security policy</span>
            <span className="info">{securityData.score_data.description[14]}</span>  
          </div>
          <ProgressBar value={securityData.score_data.score[14]} />
        </div>
        <div className="comm-features">
          <div className="desc">
            <span>Vulnerabilities</span>
            <span className="info">{securityData.score_data.description[17]}</span>
          </div>
          <ProgressBar value={securityData.score_data.score[17]} />
        </div>
      </div>
    </div>
  );
}

export default Community;
