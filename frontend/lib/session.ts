// eslint-disable-next-line import-x/no-unresolved
import "server-only";
import { jwtVerify } from "jose";
import { cookies } from "next/headers";

const jwtSecretKey = process.env.JWT_SECRET_KEY || "please1change1me";
const jwtAlgorithm = process.env.JWT_ALGORITHM || "HS256";
const encodedKey = new TextEncoder().encode(jwtSecretKey);

interface Token {
  id: string;
  name: string;
  scope: string;
  exp: number;
}

export async function decrypt(
  session: string | undefined = "",
): Promise<Token> {
  try {
    const { payload } = await jwtVerify(session, encodedKey, {
      algorithms: [jwtAlgorithm],
    });
    return payload as unknown as Token;
  } catch (error) {
    return error as Token;
  }
}

const jwtAccessTokenExpireMinutes = Number(
  process.env.JWT_ACCESS_TOKEN_EXPIRE_MINUTES || "240",
);

export async function createSession(token: string) {
  const expiresAt = new Date(
    Date.now() + jwtAccessTokenExpireMinutes * 60 * 1000,
  );
  const cookieStore = await cookies();

  cookieStore.set("session", token, {
    httpOnly: true,
    secure: true,
    expires: expiresAt,
    sameSite: "lax",
    path: "/",
  });
}

export async function deleteSession() {
  const cookieStore = await cookies();
  cookieStore.delete("session");
}
