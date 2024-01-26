<script setup>
</script>
<template>
  <div class="main" @click="$router.push('/')">
    <div class="logo">
      <icon-fluent:doctor-28-regular style="font-size: 18px;" />
    </div>
  </div>
</template>


<style scoped>
.main {
  height: 100%;
  display: flex;
  align-items: center;
  font-size: 16px;
  cursor: pointer;
  font-weight: 700;
}

.logo {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-right: 2px;
  cursor: pointer;
}
</style>
