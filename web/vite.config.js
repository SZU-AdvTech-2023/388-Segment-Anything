import { fileURLToPath, URL } from "node:url";
import AutoImport from "unplugin-auto-import/vite";
import Components from "unplugin-vue-components/vite";
// import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { ElementPlusResolver } from "unplugin-vue-components/resolvers";
// icon 插件
import Icons from "unplugin-icons/vite";
// icon 自动引入解析器
import IconsResolver from "unplugin-icons/resolver";
// icon 加载 loader
import { FileSystemIconLoader } from "unplugin-icons/loaders";
import config from "./src/config/config";
import viteCompression from "vite-plugin-compression";
// import { loadEnv } from "vite";

// const CWD = process.cwd();
export default () => {
  // const { VITE_NODE_ENV } = loadEnv(mode, CWD);
  // const isProd = ["development", "test", "production"].includes(VITE_NODE_ENV);

  return {
    base: config.publicPath,
    plugins: [
      vue(),
      AutoImport({
        imports: ["vue", "vue-router"],
        resolvers: [
          ElementPlusResolver(), // Auto import icon components
          // 自动导入图标组件
          IconsResolver({
            prefix: "Icon",
          }),
        ],
        eslintrc: {
          // 启用
          enabled: true,
          // 生成自动导入json文件位置
          filepath: "./.eslintrc-auto-import.json",
          // 全局属性值
          globalsPropValue: true,
        },
      }),
      Components({
        dirs: ["src/components/", "src/views/", "src/layout"],
        include: [/\.vue$/, /\.vue\?vue/, /\.md$/],
        resolvers: [
          ElementPlusResolver(),
          IconsResolver({
            enabledCollections: ["ep"],
          }),
          // icon组件自动引入解析器使用
          IconsResolver({
            // icon自动引入的组件前缀 - 为了统一组件icon组件名称格式
            prefix: "icon",
            // 自定义的icon模块集合
            customCollections: ["user", "home"],
          }),
        ],
        extensions: ["vue"], //文件扩展
      }),
      // Icon 插件配置
      Icons({
        compiler: "vue3",
        customCollections: {
          // user图标集，给svg文件设置 fill="currentColor" 属性，使图标的颜色具有适应性
          user: FileSystemIconLoader("src/assets/svg/user", (svg) =>
            svg.replace(/^<svg /, '<svg fill="currentColor" ')
          ),
          // home 模块图标集
          home: FileSystemIconLoader("src/assets/svg/home", (svg) =>
            svg.replace(/^<svg /, '<svg fill="currentColor" ')
          ),
        },
        autoInstall: true,
      }),
      config.zip
        ? viteCompression({
            verbose: true,
            disable: false,
            threshold: 10240,
            algorithm: "gzip",
            ext: ".gz",
          })
        : {},
    ],
    resolve: {
      alias: {
        "@": fileURLToPath(new URL("./src", import.meta.url)),
      },
    },
    server: {
      proxy: {
        "/api": {
          target: "http://127.0.0.1:5000",
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, ""),
        },
      },
    },
    esbuild: {
      // pure: isProd ? ["console.log", "debugger"] : [],
      pure: ["console.log", "debugger"],
    },
    // 生产环境打包配置
    build: {
      target: "es2015", // 浏览器兼容性
      cssTarget: "chrome79", // 此选项允许用户为 CSS 的压缩设置一个不同的浏览器 target
      chunkSizeWarningLimit: 2000, // chunk 大小警告的限制（以 kbs 为单位）。
      outDir: config.outputDir || "dist", // 指定输出路径
      assetsDir: config.assetsDir || "static", // 指定生成静态资源的存放路径（相对于 build.outDir）。
      manifest: false, // 当设置为 true，构建后将会生成 manifest.json 文件，包含了没有被 hash 的资源文件名和 hash 后版本的映射。可以为一些服务器框架渲染时提供正确的资源引入链接。
    },
  };
};
