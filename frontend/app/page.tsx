"use client";

import { useEffect, useState } from "react";

export default function Home() {
  const [apiState, setApiState] = useState<boolean>(false);
  useEffect(() => {
    async function fetchApiState() {
      const response = await fetch("http://127.0.0.1:8000/v0/health/running");
      const data = await response.json();
      setApiState(data.status === "pass");
    }
    fetchApiState();
  }, []);
  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
      <div className="text-center">
        <h1 className="mb-4 text-4xl font-bold text-zinc-800 dark:text-zinc-200">
          Server is {apiState ? "Running" : "Down"}
        </h1>
      </div>
    </div>
  );
}
