import axios from "axios";
import {
  getToken,
  getRefreshToken,
  saveTokens,
  removeToken,
  isTokenExpired,
} from "./auth";

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "/api/v1",
  headers: {
    "Content-Type": "application/json",
  },
});

let isRefreshing = false;
let failedQueue = [];

const processQueue = (error, token = null) => {
  failedQueue.forEach((prom) => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });
  failedQueue = [];
};

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

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        })
          .then((token) => {
            originalRequest.headers.Authorization = `Bearer ${token}`;
            return apiClient(originalRequest);
          })
          .catch((err) => Promise.reject(err));
      }

      originalRequest._retry = true;
      isRefreshing = true;

      const refreshToken = getRefreshToken();
      if (refreshToken && !isTokenExpired(refreshToken)) {
        try {
          const response = await axios.post(
            `${apiClient.defaults.baseURL}/auth/refresh`,
            { refresh_token: refreshToken }
          );
          const { access_token, refresh_token } = response.data;
          saveTokens(access_token, refresh_token);
          processQueue(null, access_token);
          originalRequest.headers.Authorization = `Bearer ${access_token}`;
          return apiClient(originalRequest);
        } catch (refreshError) {
          processQueue(refreshError, null);
          removeToken();
          window.location.href = "/login";
          return Promise.reject(refreshError);
        } finally {
          isRefreshing = false;
        }
      } else {
        removeToken();
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

export default {
  // Auth
  login(email, password) {
    const formData = new URLSearchParams();
    formData.append("username", email);
    formData.append("password", password);
    return apiClient.post("/auth/login", formData, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    });
  },

  register(email, password, fullName = null) {
    return apiClient.post("/auth/register", {
      email,
      password,
      full_name: fullName,
    });
  },

  refreshToken(refreshToken) {
    return apiClient.post("/auth/refresh", { refresh_token: refreshToken });
  },

  getCurrentUser() {
    return apiClient.get("/auth/me");
  },

  updateCurrentUser(data) {
    return apiClient.put("/auth/me", data);
  },

  // Clients
  getClients(params = {}) {
    return apiClient.get("/clients/", { params });
  },

  getClientsCount(params = {}) {
    return apiClient.get("/clients/count", { params });
  },

  getClient(clientId) {
    return apiClient.get(`/clients/${clientId}`);
  },

  createClient(data) {
    return apiClient.post("/clients/", data);
  },

  updateClient(clientId, data) {
    return apiClient.put(`/clients/${clientId}`, data);
  },

  deleteClient(clientId) {
    return apiClient.delete(`/clients/${clientId}`);
  },

  // Properties
  getProperties(params = {}) {
    return apiClient.get("/properties/", { params });
  },

  getPropertiesCount(params = {}) {
    return apiClient.get("/properties/count", { params });
  },

  getProperty(propertyId) {
    return apiClient.get(`/properties/${propertyId}`);
  },

  createProperty(data) {
    return apiClient.post("/properties/", data);
  },

  updateProperty(propertyId, data) {
    return apiClient.put(`/properties/${propertyId}`, data);
  },

  deleteProperty(propertyId) {
    return apiClient.delete(`/properties/${propertyId}`);
  },

  // Analysis
  analyzeArea(geojson, propertyId = null) {
    const data = { ...geojson };
    if (propertyId) {
      data.property_id = propertyId;
    }
    return apiClient.post("/analysis/", data);
  },

  getAnalysisReports(params = {}) {
    return apiClient.get("/analysis/", { params });
  },

  getAnalysisReport(reportId) {
    return apiClient.get(`/analysis/${reportId}`);
  },

  deleteAnalysisReport(reportId) {
    return apiClient.delete(`/analysis/${reportId}`);
  },

  downloadReportUrl(reportId) {
    return `${apiClient.defaults.baseURL}/analysis/${reportId}/download?token=${getToken()}`;
  },
};
