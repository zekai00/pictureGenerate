<template>
  <div id="app">
    <el-container>
      <el-header>图像生成器</el-header>
      <el-main>
        <el-input v-model="inputText" placeholder="请输入图像描述"></el-input>
        <el-button type="primary" @click="generateImage">生成图像</el-button>
        <el-image :src="generatedImage" fit="contain"></el-image>
      </el-main>
    </el-container>
  </div>
</template>

<script>
export default {
  data() {
    return {
      inputText: '',
      generatedImage: '',
    };
  },
  methods: {
    generateImage() {
      // 这里编写将inputText发送到后端并接收生成图像的代码
      // 现在,我们只是将generatedImage设置为一个占位符图像
      this.generatedImage = 'https://via.placeholder.com/350x150';
    },
  },
};
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>