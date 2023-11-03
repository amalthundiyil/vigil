"use client";

import * as React from "react";

import { Progress } from "@/components/ui/progress";

export default function Security(data: any) {
  let securityData = data["data"]["security"]["score_data"];
  console.log(securityData["score"][11]);

  return (
    <>
      <div className="grid gap-7 grid-cols-3 ml-3">
        <div className="grid grid-rows-4 gap-1 col-span-2">
          <Progress
            value={securityData["score"][17] * 10}
            className="w-[100%]"
          />
          <Progress
            value={securityData["score"][12] * 10}
            className="w-[100%]"
          />
          <Progress
            value={securityData["score"][13] * 10}
            className="w-[100%]"
          />
          <Progress
            value={securityData["score"][1] * 10}
            className="w-[100%]"
          />
        </div>
        <div className="grid grid-rows-4 gap-2">
          <h2 className="font-medium capitalize">
            {(securityData["metrics"][17] || "").replaceAll("_", " ")}
          </h2>
          <h2 className="font-medium capitalize">
            {(securityData["metrics"][12] || "").replaceAll("_", " ")}
          </h2>
          <h2 className="font-medium uppercase">
            {(securityData["metrics"][13] || "").replaceAll("-", " ")}
          </h2>
          <h2 className="font-medium capitalize">
            {(securityData["metrics"][1] || "").replaceAll("_", " ")}
          </h2>
        </div>
      </div>
    </>
  );
}
