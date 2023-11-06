"use client";

import { Metadata } from "next";
import Image from "next/image";
import { Icons } from "@/components/icons";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { MainNav } from "@/components/main-nav";
import { CommitFrequency } from "@/app/dashboard/CommitFrequency";
import Search from "./Search";
import { UserNav } from "@/components/user-nav";
import type { GetServerSideProps } from "next";
import Link from "next/link";
import { useEffect } from "react";
import { RadialBarChart, RadialBar } from "recharts";
import Summary from "./Summary";
import Downloads from "./Downloads";
import Community from "./Community";
import Security from "./Security";
import { useRouter } from "next/navigation";

export default function DashboardPage() {
  const router = useRouter();
  if (typeof window === 'undefined') return null;

  const selectedSource: any = localStorage.getItem("selectedSource");
  const searchResults: any = localStorage.getItem("searchResults");
  const data = JSON.parse(searchResults);

  if (!selectedSource || selectedSource.length === 0 || !data || data === "") {
    router.push("/");
  }

  const repoData = data.data;

  const getIcon = (type: string) => {
    if (type === "github") {
      return <Icons.gitHub className="h-5 w-5" />;
    } else if (type === "npm") {
      return <Icons.npm className="h-5 w-5" />;
    } else if (type === "pypi") {
      return <Icons.pypi className="h-5 w-5" />;
    }
  };

  return (
    <>
      <div className="hidden flex-col md:flex">
        <div className="border-b">
          <div className="flex h-16 items-center px-4">
            <MainNav className="mx-6" />
            <div className="ml-auto flex items-center space-x-4">
              <Search />
              <UserNav />
            </div>
          </div>
        </div>
        <div className="flex-1 space-y-4 p-8 pt-6">
          <div className="flex items-center justify-between space-y-2">
            <div className="grid gap-3">
              <h2 className="text-3xl font-bold tracking-tight">
                {repoData.name}
              </h2>
              <div>{repoData.description}</div>
              <div className="flex justify-between">
                <Link
                  href={repoData.url}
                  className="text-small hover:underline capitalize flex gap-1"
                >
                  {getIcon(repoData.type)}
                  {repoData.type}
                </Link>
                <div className="font-medium text-xl">
                  Final Score - {repoData.final_score} / 10
                </div>
              </div>
            </div>
            <Summary data={repoData} />
          </div>
          <Tabs defaultValue="overview" className="space-y-4">
            {/* <TabsList>
              <TabsTrigger value="overview">Overview</TabsTrigger>
              <TabsTrigger value="readme" disabled>
                Versions
              </TabsTrigger>
              <TabsTrigger value="changelog" disabled>
                Code Examples
              </TabsTrigger>
            </TabsList> */}
            <TabsContent value="overview" className="space-y-4">
              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">Stars</CardTitle>
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="2"
                      className="h-4 w-4 text-muted-foreground"
                    >
                      <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" />
                    </svg>
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">
                      {repoData.popularity.score_data.score[1]}
                    </div>
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">
                      Downloads
                    </CardTitle>
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="2"
                      className="h-4 w-4 text-muted-foreground"
                    >
                      <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" />
                      <circle cx="9" cy="7" r="4" />
                      <path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75" />
                    </svg>
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">
                      {repoData.popularity.score_data.score[5]}
                    </div>
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">
                      Vulnerabilities
                    </CardTitle>
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="2"
                      className="h-4 w-4 text-muted-foreground"
                    >
                      <rect width="20" height="14" x="2" y="5" rx="2" />
                      <path d="M2 10h20" />
                    </svg>
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">
                      {repoData.security.score_data.score[17]}
                    </div>
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">
                      Last Updated
                    </CardTitle>
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="2"
                      className="h-4 w-4 text-muted-foreground"
                    >
                      <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
                    </svg>
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">
                      {repoData.maintainence.score_data.score[0]}
                    </div>
                  </CardContent>
                </Card>
              </div>
              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
                <Card className="col-span-4">
                  <CardHeader>
                    <CardTitle>Commit Frequency</CardTitle>
                  </CardHeader>
                  <CardContent className="pl-2">
                    <CommitFrequency data={repoData} />
                  </CardContent>
                </Card>
                <Card className="col-span-3">
                  <CardHeader>
                    <CardTitle>Community</CardTitle>
                  </CardHeader>
                  <CardContent className="pl-2">
                    <Community data={repoData} />
                  </CardContent>
                </Card>
              </div>
              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
                <Card className="col-span-3">
                  <CardHeader>
                    <CardTitle>Security</CardTitle>
                  </CardHeader>
                  <CardContent className="pl-2">
                    <Security data={repoData} />
                  </CardContent>
                </Card>
                <Card className="col-span-4">
                  <CardHeader>
                    <CardTitle>Downloads</CardTitle>
                  </CardHeader>
                  <CardContent className="pl-2">
                    <Downloads data={repoData} />
                  </CardContent>
                </Card>
              </div>
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </>
  );
}
