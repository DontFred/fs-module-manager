// eslint-disable-next-line import-x/no-unresolved
import "server-only";
import { cookies } from "next/headers";
import { decrypt } from "@/lib/session";
import { redirect } from "next/navigation";
import { cache } from "react";

// eslint-disable-next-line import-x/prefer-default-export
export const verifySession = cache(async () => {
  const cookie = (await cookies()).get("session")?.value;
  const session = await decrypt(cookie);

  if (!session?.id) {
    redirect("/login");
  }

  return {
    isAuth: true,
    id: session.id,
    name: session.name,
    scope: session.scope,
  };
});
