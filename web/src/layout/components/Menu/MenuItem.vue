<script setup>
const props = defineProps({
  menu: {
    type: Object,
    required: true
  }
})
const { menu } = toRefs(props)
const router = useRouter()
const onClickMenuItem = key => {
  router.push(key)
}
onMounted(() => {
  // console.log(menu)
})
</script>

<template>

  <!-- 没有孩子节点 -->
  <template v-if="!menu.children">
    <el-menu-item :index="menu.path" @click="onClickMenuItem(menu.path)">
      <template #title>
        <el-icon v-if="menu?.icon">
          <component :is="menu?.icon"></component>
        </el-icon>
        <span>{{ menu.title }}</span>
      </template>
    </el-menu-item>
  </template>

  <template v-else>
    <el-sub-menu :index="menu.path">
      <template #title>
        <el-icon v-if="menu?.icon">
          <component :is="menu?.icon"></component>
        </el-icon>
        <span>{{ menu.title }}</span>
      </template>
      <MenuItem v-for="menuChild of menu.children" :key="menuChild.path" :menu="menuChild" />
    </el-sub-menu>
  </template>

</template>

<style scoped>

</style>


