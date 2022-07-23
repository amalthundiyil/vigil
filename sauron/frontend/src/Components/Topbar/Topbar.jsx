import React from "react";
import "./topbar.css";
import { Search } from "@mui/icons-material";
import logo from "./logo.png";
// import { NotificationsNone, Language, Settings, Search } from "@mui/icons-material";

function Topbar() {
  return (
    <div className="topbar">
      <div className="topbarWrapper">
        <div className="topLeft">
          <img src={logo} className="topAvatar"></img>
        </div>
        <h1>Sauron</h1>
        <div className="topRight">
          <div class="search-box">
            <input type="text" class="search-input" placeholder="Search.." />

            <button class="search-button">
              <Search />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Topbar;
