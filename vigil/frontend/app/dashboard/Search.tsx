import React, { useState } from "react";
import { instance as axios } from "@/lib/utils";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Icons } from "@/components/icons";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useRouter } from "next/navigation";

export default function Search() {
  const router = useRouter();
  const [search, setSearch] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [selectedSource, setSelectedSource] = useState(""); // to store the selected source

  const handleSearch = async () => {
    if (selectedSource && search) {
      try {
        const payload = {
          type: selectedSource,
          name: search,
          github_token: process.env.NEXT_PUBLIC_GITHUB_TOKEN,
        };
        const response = await axios.post("/api/dashboard/", payload);
        setSearchResults(response.data);
        localStorage.setItem("selectedSource", selectedSource);
        localStorage.setItem("searchResults", JSON.stringify(response.data));
        router.push("/dashboard");
      } catch (error) {
        console.error("Error searching:", error);
      }
    } else {
      console.log("Please select a source and enter a search query.");
    }
  };

  return (
    <div className="flex items-center justify-center">
      <Select onValueChange={(field: any) => setSelectedSource(field)}>
        <SelectTrigger className="w-[120px]">
          <SelectValue placeholder="Choose 🎱" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="github">
            <div className="flex gap-3 justify-end">
              <Icons.gitHub className="h-5 w-5" />
              <div>GitHub</div>
            </div>
          </SelectItem>
          <SelectItem value="npm">
            <div className="flex gap-3 justify-end">
              <Icons.npm className="h-5 w-5" />
              <div>npm</div>
            </div>
          </SelectItem>
          <SelectItem value="pypi">
            <div className="flex gap-3 justify-end">
              <Icons.pypi className="h-5 w-5" />
              <div>PyPI</div>
            </div>
          </SelectItem>
        </SelectContent>
      </Select>
      <Input
        type="search"
        className="md:w-[300px] lg:w-[500px] mx-2"
        placeholder="Search for packages"
        value={search}
        onChange={(event) => setSearch(event.target.value)}
      />
      <Button onClick={handleSearch}>Search</Button>
    </div>
  );
}
