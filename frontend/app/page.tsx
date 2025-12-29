import {
  checkReadyV0HealthReadyGet,
  checkRunningV0HealthRunningGet,
} from "@/api-sdk";

export default async function Home() {
  try {
    const { data, error } = await checkReadyV0HealthReadyGet({
      cache: "no-store",
    });
    const { data: data2, error: error2 } = await checkRunningV0HealthRunningGet(
      {
        cache: "no-store",
      },
    );
    return (
      <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
        <div className="text-center">
          <h1 className="mb-4 text-4xl font-bold text-zinc-800 dark:text-zinc-200">
            {data
              ? `API is ready: ${JSON.stringify(data)}`
              : `Error: ${JSON.stringify(error)}`}
          </h1>
          <h1 className="mb-4 text-4xl font-bold text-zinc-800 dark:text-zinc-200">
            {data
              ? `API is running: ${JSON.stringify(data2)}`
              : `Error: ${JSON.stringify(error2)}`}
          </h1>
        </div>
      </div>
    );
  } catch (error) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
        <div className="text-center">
          <h1 className="mb-4 text-4xl font-bold text-zinc-800 dark:text-zinc-200">
            Backend not working: {String(error)}
          </h1>
        </div>
      </div>
    );
  }
}
