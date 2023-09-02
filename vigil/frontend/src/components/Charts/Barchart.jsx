import React from 'react';
import { BarChart, Bar, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './chart.css'


function Barchart({data}) {
    return (
      <div className='chart'>
        <h3 className="chartTitle">Maintenance</h3>
          <ResponsiveContainer width='100%' aspect={4/1}>
              <BarChart width={300} height={150} data={data}>
                  <XAxis dataKey="name" stroke="#8884d8" />
                  <YAxis />
                  <Tooltip wrapperStyle={{ width: 100, backgroundColor: '#ccc' }} />
                  <Legend width={100} wrapperStyle={{ top: 40, right: 20, backgroundColor: '#f5f5f5', border: '1px solid #d5d5d5', borderRadius: 3, lineHeight: '40px' }} />
                  <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
                  <Bar dataKey="uv" fill="#8884d8" barSize={30} />
              </BarChart>
          </ResponsiveContainer>
      </div>
    )
}

export default Barchart
