import qs from "qs";
import axios from "axios";
import NProgress from "nprogress";
import "nprogress/nprogress.css";
NProgress.configure({ showSpinner: false });

const service = axios.create({
  baseURL: "/api",
  // withCredentials: true, // send cookies when cross-domain requests
  timeout: 20000, // request timeout
});
service.defaults.baseURL="http://127.0.0.1:5000"

service.interceptors.request.use(
  (config) => {
    NProgress.start();
    if (config.method == "post" && config?.isFile == 1) {
      config.headers = { "Content-Type": "multipart/form-data" };
      // config.responseType = "arraybuffer";
      config.responseType = 'blob';
    } else if (config.method == "post" && !config.isFile) {
      config.data = qs.stringify(config.data);
    } else {
      config.headers = {
        //表单格式
        "Content-Type": "application/x-www-form-urlencoded",
      };
    }

    return config;
  },
  (error) => {
    ElMessage({
      message: h("p", null, [
        h("span", null, "消息发送"),
        h("i", { style: "color: red" }, "失败"),
      ]),
    });
    return Promise.reject(error);
  }
);
service.interceptors.response.use(
  (response) => {
    NProgress.done();
    const res = response.data;
    // if (res?.data?.length === 0) {
    //   ElMessage({
    //     message: h("p", null, [h("span", null, "暂无数据")]),
    //     duration: 1000,
    //   });
    // }
    // if (res.code !== 200) {
    //   return Promise.reject(new Error(res.message || "Error"));
    // }
    return res;
  },
  (error) => {
    ElMessage.error(error);
    return Promise.reject(error);
  }
);

export default service;
