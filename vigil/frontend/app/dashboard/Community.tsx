"use client";

import * as React from "react";

import { Progress } from "@/components/ui/progress";

export default function Community(data: any) {
  let communityData = data["data"]["community"]["score_data"];
  console.log("communityData ", communityData);

  return (
    <>
      <div className="grid gap-7 grid-cols-3 ml-3">
        <div className="grid grid-rows-4 gap-6 col-span-2">
          <Progress
            value={communityData["score"][0] * 10}
            className="w-[100%]"
          />
          <Progress
            value={communityData["score"][5] * 10}
            className="w-[100%]"
          />
          <Progress
            value={communityData["score"][2] * 10}
            className="w-[100%]"
          />
          <Progress
            value={communityData["score"][3] * 10}
            className="w-[100%]"
          />
          <Progress
            value={communityData["score"][4] * 10}
            className="w-[100%]"
          />
        </div>
        <div className="grid grid-rows-4 gap-6">
          <h2 className="font-medium capitalize">
            {communityData["metrics"][0].replaceAll("_", " ")}
          </h2>
          <h2 className="font-medium capitalize">
            {communityData["metrics"][5].replaceAll("_", " ")}
          </h2>
          <h2 className="font-medium capitalize">
            {communityData["metrics"][2].replaceAll("_", " ")}
          </h2>
          <h2 className="font-medium capitalize">
            {communityData["metrics"][3].replaceAll("_", " ")}
          </h2>
          <h2 className="font-medium capitalize">
            {communityData["metrics"][4].replaceAll("_", " ")}
          </h2>
        </div>
      </div>
    </>
  );
}
