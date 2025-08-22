import axios from "axios";
import { getToken } from "./auth";

const apiClient = axios.create({
  baseURL: "http://127.0.0.1:8000/api/v1",
  headers: {
    "Content-Type": "application/json",
  },
});

apiClient.interceptors.request.use(
  (config) => {
    const token = getToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default {
  login(email, password) {
    const formData = new URLSearchParams();
    formData.append("username", email);
    formData.append("password", password);
    return apiClient.post("/auth/login", formData, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    });
  },

  analyzeArea(geojson) {
    return apiClient.post("/analysis/", geojson);
  },

  getAnalysisReport(reportId) {
    return apiClient.get(`/analysis/${reportId}`);
  },

  downloadReportUrl(reportId) {
    return `${
      apiClient.defaults.baseURL
    }/analysis/${reportId}/download?token=${getToken()}`;
  },
};
