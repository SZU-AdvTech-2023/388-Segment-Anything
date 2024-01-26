<script setup>
import { menuRouterFormatList } from '@/router/menuRouter.js'

// 新增
const props = defineProps({
  mode: {
    type: String,
    default: 'horizontal'
  },
  collapsed: {
    type: Boolean,
    default: false
  }
})
// 菜单模式，horizontal 水平，vertical 垂直
const mode = toRef(props, 'mode')
const collapsed = toRef(props, 'collapsed')


// 菜单数据
const menuList = ref(menuRouterFormatList)


const handleOpen = (key, keyPath) => {
  console.log(key, keyPath)
}

</script>
<template>
  <el-menu class="menu" @open="handleOpen" :mode="mode" :collapse="collapsed">
    <MenuItem v-for="menu of menuList" :key="menu.path" :menu="menu" />
  </el-menu>
</template>

<style scoped>
.menu:not(.el-menu--collapse) {
  width: 200px;
  min-height: 400px;
}
</style>
