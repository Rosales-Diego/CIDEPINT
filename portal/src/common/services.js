import axios from "axios";

const axiosInstance = axios.create({
  baseURL: "http://127.0.0.1:5000",
  headers: {
    "Content-Type": "application/json",
    // 'Access-Control-Allow-Origin':'*',
    // 'Accept': '*/*',
}
});


axiosInstance.interceptors.request.use(
  (config) => {
    const token = window.localStorage.getItem("token");
    if(token) {
      config.headers["Authorization"] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default axiosInstance;