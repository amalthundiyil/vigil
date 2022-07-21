import React from 'react'
import {userData} from '../../dummydata'
import Barchart from '../Charts/Barchart'
import Chart from '../Charts/Chart'
import './packagestats.css'

function PackageStats() {
  return (
    <div>
        <div className='chart-container'>
            <Chart data={userData} title='Popularity' grid dataKey='Downloads'/>
            <Barchart></Barchart>
        </div>
    </div>
  )
}

export default PackageStats