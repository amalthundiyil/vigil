import React from "react";
import { userData } from "../../dummyData";
import Barchart from "../Charts/Barchart";
import Chart from "../Charts/Chart";
import Spinner from "../Spinner";
import "./styles.css";
import { LineChart, Line, BarChart, Bar, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';


function PackageStats({ metrics }) {
  const data = metrics["data"]["data"]
  console.log(data);
  return (
    <div>
      <div className="chart-container">
          <ResponsiveContainer width='100%' aspect={4/1}>
            <LineChart labelLine={false} label="Popularity" data={data["popularity"]["ts_data"]["downloads"]}>
                <XAxis dataKey='day' stroke="#5550bd"/>
                <Line type='monotone' stroke="#5550bd" dataKey='downloads'/>
                <Tooltip/>
                {<CartesianGrid stroke="#e0dfdf" strokeDasharray='5 5'/>}
            </LineChart>
          </ResponsiveContainer>
          <ResponsiveContainer width='100%' aspect={4/1}>
            <BarChart label="Maintenance" widhth='100%' data={data["maintainence"]["ts_data"]["commit_frequency"]}>
              <XAxis dataKey="day" stroke="#8884d8" />
              <YAxis />
              <Tooltip wrapperStyle={{ width: 100, backgroundColor: '#ccc' }} />
              <Legend width={100} wrapperStyle={{ top: 40, right: 20, backgroundColor: '#f5f5f5', border: '1px solid #d5d5d5', borderRadius: 3, lineHeight: '40px' }} />
              {/* <CartesianGrid stroke="#ccc" strokeDasharray="5 5" /> */}
              <Bar dataKey="commits" fill="#8884d8" barSize={30} />
            </BarChart>
          </ResponsiveContainer>
        </div>
    </div>
  );
}

export default PackageStats;
