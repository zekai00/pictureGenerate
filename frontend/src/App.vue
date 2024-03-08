<template>
  <div id="app">
    <el-container>
      <el-header>
        <!-- 可以将bannerImage换成你的logo -->
        <el-image :src="bannerImage" fit="cover" class="logo"></el-image>
      </el-header>
      <el-main>
        <el-row type="flex" justify="center">
          <el-col :span="12">
            <div class="search-box">
              <el-input
                v-model="inputText"
                placeholder="请输入您想生成的图像描述"
                prefix-icon="el-icon-edit"
                clearable
                class="input-with-button"
                @focus="placeholder = ''"
                @blur="resetPlaceholder"
              >
                <template #append>
                  <el-button type="primary" icon="el-icon-picture" @click="generateImage">生成图片</el-button>
                </template>
              </el-input>
            </div>
          </el-col>
        </el-row>
        <!-- 展示生成的图片 -->
        <el-row v-if="generatedImage" type="flex" justify="center" style="margin-top: 20px;">
          <el-col :span="18">
            <el-image
              :src="generatedImage"
              fit="contain"
              style="max-height: 60vh; max-width: 100%;"
              class="generated-image"
            ></el-image>
            <el-loading v-model="loading" :text="loading ? '正在生成图片...' : ''" />
          </el-col>
        </el-row>
      </el-main>
    </el-container>
  </div>
</template>

<script>
// import Vue from 'vue'
import axios from 'axios'

export default {
  data() {
    return {
      bannerImage: '/pics/logo.png', // 你的logo URL
      inputText: '',
      generatedImage: '',
      placeholder: '请输入您想生成的图像描述', // 默认占位符
      loading: false //新增加载状态
    };
  },
  methods: {
    generateImage() {
      // 在这里添加你的图像生成逻辑
      // 设置加载状态为 true
      this.loading = true;

      // 构造请求体
      const requestData = {
        description: this.inputText
      };

          // 发送 POST 请求到后端 API
      axios.post('http://127.0.0.1:8000/api/generate-image/', requestData)
        .then(response => {
          // 请求成功,更新生成的图片 URL
          this.generatedImage = response.data.url;
        })
        .catch(error => {
          // 请求失败,处理错误
          console.error(error);
        })
        .finally(() => {
          // 无论成功或失败,都设置加载状态为 false
          this.loading = false;
        });

      // this.generatedImage = 'https://via.placeholder.com/500x300'; // 替换为实际生成的图像URL
    },
    resetPlaceholder() {
      if (!this.inputText) {
        this.placeholder = '请输入您想生成的图像描述';
      }
    }
  }
};
</script>

<style scoped>
#app {
  font-family: 'Roboto', sans-serif;
}
.logo {
  width: 100px; /* 调整为适合的大小 */
  height: auto;
  margin: 0 auto;
  display: block;
}
.el-header {
  padding: 30px 0;
  background-color: #f8f8f8;
}
.search-box {
  margin-top: 50px; /* 根据需要调整 */
}
.input-with-button {
  border-radius: 22px;
  padding: 10px 20px;
}
.input-with-button .el-input__inner {
  border-radius: 22px;
  transition: all 0.3s;
}
.input-with-button .el-input__inner:focus {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.25), 0 1px 3px -1px rgba(0, 0, 0, 0.3);
}
.input-with-button .el-button {
  border-radius: 22px;
}
.generated-image {
  box-shadow: 0 4px 6px -1px rgba(50, 50, 93, 0.25), 0 1px 3px -1px rgba(0, 0, 0, 0.3);
  border-radius: 8px;
}
</style>
