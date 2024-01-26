import { createRouter, createWebHashHistory } from "vue-router";
import { menuRouter } from "./menuRouter";
const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "Layout",
      component: () => import("@/layout/SwitchIndex.vue"),
      redirect: "/",
      children: [
        {
          path: "/",
          name: "HomeView",
          meta: {
            title: "HomeView",
          },
          component: () => import("@/views/HomePage.vue"),
        },
        // 使用菜单路由
        ...menuRouter,
      ],
    },
  ],
});

export default router;
