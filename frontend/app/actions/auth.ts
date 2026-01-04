"use server";

import { createSession, deleteSession } from "@/lib/session";
import { redirect } from "next/navigation";

export async function login(token: string) {
  await createSession(token);
  redirect("/");
}

export async function logout() {
  await deleteSession();
  redirect("/login");
}
