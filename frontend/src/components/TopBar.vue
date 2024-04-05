<template>
  <el-header>
    <!-- 左上角Logo -->
    <div class="logo-container left">
      <el-image class="logo logo-left" :src="require('@/assets/suishiling.png')" fit="cover"></el-image>
    </div>

    <!-- 右上角和右下角的Logo -->
    <div class="logo-container right">
      <el-image class="logo logo-right-top" :src="require('@/assets/kaiying.png')" fit="cover"></el-image>
      <el-image class="logo logo-right-bottom" :src="require('@/assets/kingnet.png')" fit="cover"></el-image>
    </div>
  </el-header>
</template>

<style>
.el-header {
  display: flex;
  justify-content: space-between; /* 左右两侧对齐 */
  align-items: flex-start;
  flex-wrap: wrap; /* 允许元素换行 */
}

.logo-container {
  display: flex;
  flex-direction: column; /* 让logo垂直排列 */
}

.logo-container.left {
  align-items: flex-start; /* 左侧logo容器对齐到左边 */
  margin-top: 0; /* 根据需要调整到适当的值 */
  margin-left: 0; /* 根据需要调整到适当的值 */
}

.logo-right-top {
  /* 如果需要调整右上角logo的位置，可以在这里添加样式 */
}

.logo-right-bottom {
  margin-top: 20px; /* 如果需要更大的间隔，增加这个值 */
}

</style>
