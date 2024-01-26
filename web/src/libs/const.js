let baseUrl = "";
if (import.meta.env.NODE_ENV === "development") {
  baseUrl = "http://127.0.0.1:5000";
} else {
  // 你的 API 地址
  baseUrl = "http://127.0.0.1:5000";
}
export default {
  baseUrl,
};
