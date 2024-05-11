<template>
  <el-header>
    <div class="centered-container">
<!--      <h3>请手动保存作品，可参与三月三诗歌，AI创作大赛。<a href="https://www.aitop100.cn/circle/index.html?circleId=23">点击此处投稿。</a></h3>-->
      <div class="logo-container">
        <el-image class="logo" :src="require('@/assets/shiyuanshuban.png')" fit="cover"></el-image>
        <el-image class="logo  logo-maliang" :src="require('@/assets/maliangLOGO/mlblack.png')" fit="cover"></el-image>
        <el-image class="logo" :src="require('@/assets/fudanvertical.png')" fit="cover"></el-image>
        <el-image class="logo" :src="require('@/assets/kaiyingshuban.png')" fit="cover"></el-image>
        <el-image class="logo  logo-suishi" :src="require('@/assets/suishilinghengban.png')" fit="cover"></el-image>
        <el-image class="logo" :src="require('@/assets/aitop100.png')" fit="cover"></el-image>
      </div>
      <h3>书画数字化生成应用服务文化和旅游部技术创新中心（筹）</h3>
    </div>
  </el-header>
</template>

<script>
export default {
  name: 'AppTopBar', // 使用多个单词的命名
  // ...
}
</script>

<style>
.el-header {
  display: flex;
  justify-content: center; /* 水平居中对齐 */
  align-items: center;
  flex-wrap: nowrap; /* 防止元素换行 */
}

/* 新增的居中容器样式 */
.centered-container {
  text-align: center;
  flex-direction: column; /* 子项垂直排列 */
}

.logo-container {
  display: flex;
  flex-direction: row; /* logo横向排列 */
  justify-content: space-around; /* logo水平居中 */
  align-items: center; /* logo垂直居中 */
}

.logo {
  max-width: 100px; /* 设置最大宽度，按需调整 */
  max-height: 150px; /* 设置最大高度，按需调整 */
  width: auto; /* 保持图像原始宽高比 */
  height: auto; /* 保持图像原始宽高比 */
  object-fit: contain; /* 图像等比例填充 */
  margin: 0 20px; /* logo之间的水平间隔 */
}

.logo-maliang{
  max-width: 330px;
}

.logo-suishi{
  max-height: 130px;
  max-width: 230px;
}
</style>
