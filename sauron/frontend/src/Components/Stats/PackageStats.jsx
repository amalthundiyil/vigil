import React from 'react'
import {userData} from '../../dummydata'
import Barchart from '../Charts/Barchart'
import Chart from '../Charts/Chart'
import './packagestats.css'

function PackageStats() {
  return (
    <div>
        <Chart data={userData} title='Popularity' grid dataKey='Downloads'/>
        <Barchart></Barchart>
    </div>
  )
}

export default PackageStats