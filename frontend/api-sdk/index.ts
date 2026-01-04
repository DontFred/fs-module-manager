import createSClient from "openapi-fetch";
import createCClient from "openapi-react-query";
import type { paths } from "./schema";

const sclient = createSClient<paths>({
  baseUrl: `http://127.0.0.1:${process.env.BACKEND_PORT || "8000"}`,
});

const cclient = createCClient(sclient);

export { sclient, cclient };
