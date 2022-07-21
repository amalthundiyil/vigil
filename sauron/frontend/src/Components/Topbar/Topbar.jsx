import React from 'react'
import './topbar.css'
import { Search } from '@material-ui/icons';
// import { NotificationsNone, Language, Settings, Search } from "@material-ui/icons";

function Topbar() {
    return (
        <div className='topbar'>
            <div className='topbarWrapper'>
                <div className="topLeft">
                    <img src='https://raw.githubusercontent.com/amal-thundiyil/sauron/frontend/docs/images/logo.png?token=GHSAT0AAAAAABU7CTQM3E5YFDC4X7INUZYWYWZS37A' className='topAvatar'></img>
                    
                </div>
                <h1>Sauron</h1>
                <div className='topRight'>
                <div class="search-box">
                    <input type="text" class="search-input" placeholder="Search.."/>

                    <button class="search-button">
                        <Search/>
                    </button>
                </div>
                </div>
            </div>
        </div>
    )
}

export default Topbar