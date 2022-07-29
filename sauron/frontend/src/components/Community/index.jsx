import React from "react";
import "./styles.css";
import { Block, Close, Done } from "@mui/icons-material";
function Community() {
  return (
    <div className="featured">
      <div className="featuredItem">
        <span className="featuredTitle">Community</span>
        <div className="comm-features">
          <span>README</span>
          <Done></Done>
        </div>
        <div className="comm-features">
          <span>CODE OF CONDUCT</span>
          <Done></Done>
        </div>
        <div className="comm-features">
          <span>FUNDING</span>
          <Done></Done>
        </div>
        <div className="comm-features">
          <span>CONTRIBUTORS.MD</span>
          <Close></Close>
        </div>
        <div className="comm-features">
          <span>CONTRIBUTORS</span>
          <span>200</span>
        </div>
      </div>
      <div className="welcomingness">
        <span className="featuredTitle">Welcomingness</span>
        <span className="sentiment">
          {/* Categorized as Friendly⭐/ Helpful😀/ Not Responsive😶 */}
          Sentimental analysis concludes commuity is :
          <span className="bold"> Friendly⭐</span>
        </span>
      </div>
    </div>
  );
}

export default Community;
