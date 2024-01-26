import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "./App.vue";
import router from "./router";
import "./assets/main.css";
// 这里
import "@/styles/normalize.css"
const app = createApp(App);

import Api from "./request/api";
app.config.globalProperties.$http = Api;
app.use(createPinia());
app.use(router);
app.mount("#app");
