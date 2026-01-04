import createSClient from "openapi-fetch";
import createCClient from "openapi-react-query";
import type { paths } from "./schema";

const sclient = createSClient<paths>({
  baseUrl: `${process.env.NEXT_PUBLIC_SERVER_URL}:${process.env.NEXT_PUBLIC_BACKEND_PORT || "8000"}`,
});

const cclient = createCClient(sclient);

export { sclient, cclient };
