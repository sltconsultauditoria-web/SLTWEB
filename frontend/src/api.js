import axios from "axios";

const API = axios.create({
  baseURL: "/api"
});

API.interceptors.response.use((response) => {
  const payload = response.data;
  if (
    payload &&
    typeof payload === "object" &&
    Object.prototype.hasOwnProperty.call(payload, "success") &&
    Object.prototype.hasOwnProperty.call(payload, "data")
  ) {
    response.data = payload.data;
  }
  return response;
});

export default API;
