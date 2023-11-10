import { formatDateToYYYYMMDD } from "@/lib/utils";
import React, { PureComponent } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

export default function Downloads(data: any) {
  let downloads = data["data"]["popularity"]["ts_data"]["downloads"];

  if (!downloads || downloads.length === 0) {
    const currentDate = new Date();
    downloads = [];

    // Push data for the past 5 days
    for (let i = 0; i < 5; i++) {
      const previousDate = new Date(currentDate);
      previousDate.setDate(currentDate.getDate() - 5 + i);
      downloads.push({
        downloads: 0,
        date: formatDateToYYYYMMDD(previousDate),
      });
    }
  }

  return (
    <ResponsiveContainer width="100%" height={200}>
      <LineChart width={300} height={100} data={downloads}>
        <XAxis dataKey="date" />
        <YAxis />
        <Tooltip />
        <Line
          type="monotone"
          dataKey="downloads"
          stroke="black"
          strokeWidth={2}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
