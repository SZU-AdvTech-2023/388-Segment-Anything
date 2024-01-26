<template>
  <div class="box">
    <div class="left">
      <div class="content">
        <div class="img-box">
          <img :src="ctPic" ref="ctRef" onerror="this.classList.add('error');">
        </div>
        <!-- <p class="explain">原CT图片</p> -->
        <div class="btn">
          <el-button color="#626aef" size="large" @click="ctPicSub">上一张</el-button>
          <el-button color="#626aef" size="large" @click="ctPicAdd">下一张</el-button>
        </div>
      </div>
      <div class="content">
        <div class="img-box">
          <img :src="xrayPic" ref="xrayRef" onerror="this.classList.add('error');">
        </div>
        <div class="btn">
          <el-button color="#626aef" size="large" @click="xrayPicSub">上一张</el-button>
          <el-button color="#626aef" size="large" @click="xrayPicAdd">下一张</el-button>
        </div>
      </div>
    </div>

    <div class="right">
      <div class="result">
        <div class="img-box" style="height: calc(74vh + 65px);">
          <img :src="combineSrc" ref="combine" onerror="this.classList.add('error');">
        </div>
        <div style="width:100%;display: flex;justify-content: space-around;margin: 5px 0;">
          <el-button style="width: 80%;" color="#626aef" size="large" @click="uploadClick">上传</el-button>
        </div>
      </div>
    </div>

  </div>

</template>
<script setup>
const instance = getCurrentInstance();

const getPic = (files, index) => {
  return new URL(`../assets/images/${files[index]}`, import.meta.url).href
}

const ctPic = ref('')
const ctRef = ref()
const ctCount = ref(0)
const ctDirlength = ref(0)
const ctFiles = import.meta.glob('@/assets/images/ct/*.jpg')
const getCtPic = (index) => {
  if (index === 0) {
    ctDirlength.value = Object.keys(ctFiles).length
  }
  const imgPathArr = []
  Object.keys(ctFiles).forEach((item) => {
    imgPathArr.push(item.replace(/\/src\/assets\/images\//g, ''))
  })
  return getPic(imgPathArr, index)
}
const ctPicAdd = () => {
  if (ctCount.value >= ctDirlength.value - 1) {
    return ElMessage({
      message: '已经是最后一张了',
      type: 'warning'
    })
  }
  ctCount.value++
  ctPic.value = getCtPic(ctCount.value)
}
const ctPicSub = () => {
  if (ctCount.value === 0) {
    return ElMessage({
      message: '这里是第一张',
      type: 'warning'
    })
  }
  ctCount.value--
  ctPic.value = getCtPic(ctCount.value)
}

const xrayPic = ref('')
const xrayCount = ref(0)
const xrayDirlength = ref(0)
const xrayRef = ref()
const xrayFiles = import.meta.glob('@/assets/images/xray/*.jpg')
const getXrayPic = (index) => {
  if (index === 0) {
    xrayDirlength.value = Object.keys(xrayFiles).length
  }
  const imgPathArr = []
  Object.keys(xrayFiles).forEach((item) => {
    imgPathArr.push(item.replace(/\/src\/assets\/images\//g, ''))
  })
  return getPic(imgPathArr, index)
}
const xrayPicAdd = () => {
  if (xrayCount.value >= xrayDirlength.value - 1) {
    return ElMessage({
      message: '已经是最后一张了',
      type: 'warning'
    })
  }
  xrayCount.value++
  xrayPic.value = getXrayPic(xrayCount.value)
}
const xrayPicSub = () => {
  if (xrayCount.value === 0) {
    return ElMessage({
      message: '这里是第一张',
      type: 'warning'
    })
  }
  xrayCount.value--
  xrayPic.value = getXrayPic(xrayCount.value)
}


const combineSrc = ref('')

const uploadClick = async () => {
  const response = await fetch(ctPic.value)
  const ctData = await response.blob()

  const response2 = await fetch(xrayPic.value)
  const xrayData = await response2.blob()

  let formData = new FormData()
  formData.append('ct', ctData)
  formData.append('xray', xrayData)

  const res = await instance.proxy.$http.upload(formData)
  const url = URL.createObjectURL(res);
  combineSrc.value = url
}

onMounted(() => {
  ctPic.value = getCtPic(ctCount.value)
  xrayPic.value = getXrayPic(xrayCount.value)
})

</script>
<style scoped>
.box {
  width: 100%;
}

.left {
  float: left;
  width: 25%;
  overflow-y: scroll
}

.right {
  box-sizing: border-box;
  float: right;
  width: 75%;
}

.content {
  margin: 15px;
  border: 5px dashed #000;
}

.result {
  height: 100%;
  margin: 15px;
  border: 5px dashed #000;
}

.img-box {
  height: 37vh
}

.img-box img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  padding: 5px
}

/* 修改无图片默认样式 */
img.error::before {
  font-size: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 15px;
  color: #B7B8BC;
  content: '等待返回';
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background: #F6F7FA
}

.btn {
  margin-bottom: 5px;
  display: flex;
  justify-content: space-around
}

.explain {
  margin: 5px;
  margin-left: auto;
  margin-right: auto;
  text-align: center;
  width: 90%;
  background-color: #626aef;
  font-size: 20px;
  color: #fff;
  border-radius: 10px;
}
</style>
