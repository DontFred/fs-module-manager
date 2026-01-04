"use client";

import { cclient } from "@/api-sdk";

export default function Health() {
  const {
    data: runningResponse,
    error: runningError,
    isLoading: runningLoading,
  } = cclient.useQuery("get", "/v0/health/running");

  const {
    data: readyResponse,
    error: readyError,
    isLoading: readyLoading,
  } = cclient.useQuery("get", "/v0/health/ready");

  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
      <div className="text-center">
        <h1 className="mb-4 text-2xl font-bold text-zinc-900 dark:text-zinc-100">
          Welcome to the Module Manager Frontend!
        </h1>
        <p className="mb-8 text-zinc-700 dark:text-zinc-300">
          This is the health page of the frontend application.
        </p>
        <div className="mb-6 text-zinc-800 dark:text-zinc-200">
          {runningLoading && <p>Loading running status...</p>}
          {runningError && (
            <p className="text-red-600">Error: {String(runningError)}</p>
          )}
          {runningResponse && <p>Running Status: {runningResponse.status}</p>}
        </div>
        <div className="text-zinc-800 dark:text-zinc-200">
          {readyLoading && <p>Loading ready status...</p>}
          {readyError && (
            <p className="text-red-600">Error: {String(readyError)}</p>
          )}
          {readyResponse && <p>Ready Status: {readyResponse.status}</p>}
        </div>
      </div>
    </div>
  );
}
