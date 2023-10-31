"use client";

import React from "react";
import { RadialBarChart, RadialBar, PolarAngleAxis } from "recharts";
import { useEffect, useState } from "react";

const categories = ["security", "maintainence", "popularity", "community"];

export default function Summary({ data }: { data: any }) {
  // https://stackoverflow.com/a/76742741/17297103
  const [isMounted, setIsMounted] = useState(false);
  useEffect(() => {
    setIsMounted(true);
  }, []);

  if (!isMounted) {
    return null;
  }
  return (
    <div className="grid">
      <div className="flex justify-around">
        {categories.map((category: any) => {
          return (
            <RadialBarChart
              width={150}
              key={category}
              height={100}
              data={data}
              innerRadius={30}
              outerRadius={40}
            >
              <PolarAngleAxis
                key={category}
                type="number"
                domain={[0, 10]}
                angleAxisId={0}
                tick={false}
              />
              <RadialBar
                key={category}
                background
                dataKey="score"
                angleAxisId={0}
                data={[data[category].summary]}
              />
            </RadialBarChart>
          );
        })}
      </div>
      <div className="flex justify-around">
        {categories.map((category) => {
          return (
            <div className="capitalize" key={category}>
              {category}
            </div>
          );
        })}
      </div>
    </div>
  );
}
