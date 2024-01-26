import MakiDoctor from "~icons/maki/doctor";
import MapDoctor from "~icons/map/doctor";
import Fa6SolidUserDoctor from "~icons/fa6-solid/user-doctor";
export const menuRouter = [
  {
    path: "combine",
    name: "combine",
    meta: {
      title: "图像",
      icon: markRaw(MakiDoctor),
    },
    redirect: { name: "pic" },
    children: [
      {
        path: "pic",
        name: "pic",
        meta: {
          title: "图像融合",
        },
        component: () => import("@/views/HomeView.vue"),
      },
      {
        path: "test",
        name: "test",
        meta: {
          title: "测试1",
        },
        component: () => import("@/views/HomePage.vue"),
      },
    ],
  },
  {
    path: "test2",
    name: "test2",
    meta: {
      title: "test",
      //将一个对象标记为不可被转为代理。返回该对象本身。
      icon: markRaw(MapDoctor),
    },
    redirect: { name: "test3" },
    children: [
      {
        path: "test3",
        name: "test3",
        meta: {
          title: "测试3",
        },
        component: () => import("@/views/HomePage.vue"),
      },
      {
        path: "test4",
        name: "test4",
        meta: {
          title: "测试4",
        },
        component: () => import("@/views/HomePage.vue"),
      },
    ],
  },
  {
    path: "test5",
    name: "test5",
    meta: {
      title: "test5",
      //将一个对象标记为不可被转为代理。返回该对象本身。
      icon: markRaw(Fa6SolidUserDoctor),
    },
    redirect: { name: "test3" },
    children: [
      {
        path: "test6",
        name: "test6",
        meta: {
          title: "测试3",
        },
        component: () => import("@/views/HomePage.vue"),
      },
      {
        path: "test7",
        name: "test8",
        meta: {
          title: "测试4",
        },
        component: () => import("@/views/HomePage.vue"),
      },
    ],
  },
];

/**
 * @description 菜单路由数组 format
 * @param { Array } router 路由数组
 * @param { String } parentPath 父级路由 path
 * @return { Array }
 */
export const menuRouterFormat = (router, parentPath) => {
  return router.map((item) => {
    // 拼接路由，例：'devtools' -> '/devtools'  'regular' -> '/devtools/regular'
    item.path = parentPath ? `${parentPath}/${item.path}` : `/${item.path}`;

    // 存在 children 属性，且 children 数组长度大于 0，开始递归
    if (item.children && item.children.length > 0) {
      item.children = menuRouterFormat(item.children, item.path);
    }

    return Object.assign({}, item, item.meta || {});
  });
};

// 解析后 路由菜单列表
export const menuRouterFormatList = menuRouterFormat([...menuRouter]);
