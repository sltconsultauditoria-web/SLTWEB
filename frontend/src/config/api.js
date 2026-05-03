import axios from "axios";

const getApiUrl = () => {
  const envUrl = process.env.REACT_APP_API_URL || process.env.REACT_APP_BACKEND_URL;
  if (!envUrl) return "/api";
  const cleanUrl = envUrl.replace(/\/+$/, "");
  return cleanUrl.endsWith("/api") ? cleanUrl : `${cleanUrl}/api`;
};

export const API = axios.create({
  baseURL: getApiUrl()
});
