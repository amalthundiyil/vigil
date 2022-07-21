import React from 'react'
import './packageinfo.css'
import { ArrowDownward, ArrowUpward } from '@material-ui/icons'
function Packageinfo() {
    return (
        <div className='featured'>
            <div className="featuredItem">
                <span className="featuredTitle">Package Info</span>
                <div className="featuredMoneyContainer">
                    <span className="featuredMoney">NumPy</span>
                    <span className="featuredMoneyRate">v2.0</span>
                </div>
                <span className="featuredSub">Package info.........
                She considered the birds to be her friends. She'd put out food for them each morning and then she'd watch as they came to the feeders to gorge themselves for the day.</span>
            </div>
            <div className="featuredItem">
                <span className="featuredTitle">Health Score</span>
                <div className="featuredMoneyContainer">
                    <span className="featuredMoney">88 / 100</span>
                </div>
                <span className="featuredSub">Note: Package is in good health</span>
            </div>
        </div>
    )
}

export default Packageinfo
