export default {
  input: "http://127.0.0.1:8000/v0/openapi.json",
  output: {
    path: "api-sdk",
    lint: "eslint",
    format: "prettier",
  },
  plugins: ["@hey-api/client-next"],
};
