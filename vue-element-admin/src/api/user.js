import request from "@/utils/request";

export function login(data) {
  console.log("``````````````````````````````````````````````````````````````");
  console.log(data);
  var _data = request({
    url: "/vue-element-admin/user/login",
    method: "post",
    data
  });
  console.log(_data);
  return _data;
}

export function getInfo(token) {
  return request({
    url: "/vue-element-admin/user/info",
    method: "get",
    params: { token }
  });
}

export function logout() {
  return request({
    url: "/vue-element-admin/user/logout",
    method: "post"
  });
}
