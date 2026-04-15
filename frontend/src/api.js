import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost/SLTWEB/api" // ajustado para seu backend
});

export default API;
