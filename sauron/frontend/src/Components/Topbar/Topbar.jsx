import React from 'react'
import './topbar.css'
import { Search } from '@material-ui/icons';
// import { NotificationsNone, Language, Settings, Search } from "@material-ui/icons";

function Topbar() {
    return (
        <div className='topbar'>
            <div className='topbarWrapper'>
                <div className="topLeft">
                    <img src='https://raw.githubusercontent.com/amal-thundiyil/sauron/main/docs/images/logo.png?token=GHSAT0AAAAAABU7CTQNIRCFBE3VOQSCOHR6YWZND7A' className='topAvatar'></img>
                </div>
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
