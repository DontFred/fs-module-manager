import { Button } from "@/components/ui/button";
import { logout } from "@/app/actions/auth";
import { verifySession } from "@/lib/dal";

export default async function Home() {
  const session = await verifySession();
  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
      <div className="text-center">
        <h1 className="mb-4 text-2xl font-bold text-zinc-900 dark:text-zinc-100">
          Willkommen zum Module Manager Frontend!
        </h1>
        <p className="mb-8 text-zinc-700 dark:text-zinc-300">
          Du bist eingeloggt als {session.name}.
        </p>
        <div className="text-zinc-800 dark:text-zinc-200">
          <Button onClick={logout}>Logout</Button>
        </div>
      </div>
    </div>
  );
}
