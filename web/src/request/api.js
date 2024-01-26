import request from "./http";

const upload = (file) => {
  return request({
    method: "post",
    url: "/cv",
    data: file,
    isFile: 1,
  });
};

const api = { upload };
export default api;
