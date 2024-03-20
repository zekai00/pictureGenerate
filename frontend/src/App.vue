<template>
  <div id="app" class="site-container">
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
            <div v-if="loading" style="margin-top: 20px;">
              <el-progress :percentage="progress"></el-progress>
            </div>
          </el-col>
        </el-row>
        <!-- 展示生成的图片 -->
        <el-row v-if="generatedImages.length > 0" type="flex" justify="center" style="margin-top: 20px;">
          <el-col :span="12" v-for="(image, index) in generatedImages" :key="index">
            <el-image
              :src="image.url"
              fit="contain"
              style="max-height: 60vh; max-width: 100%; cursor: pointer;"
              :class="{
                'selected-image':  selectedId === null || selectedId === image.id,
                'unselected-image': selectedId !== null && selectedId !== image.id
              }"
              @click="selectImage(index)"
            ></el-image>
          </el-col>
        </el-row>
      </el-main>
    </el-container>
    <el-footer>
      <div class="site-footer">
        <h3>关于我们</h3>
        <p>这里是联系方式。</p>
      </div>
    </el-footer>
  </div>
</template>

<script>
// import Vue from 'vue'
import axios from 'axios'

export default {
  data() {
    return {
      bannerImage: '/pics/1.jpg', // 你的logo URL
      inputText: '',
      generatedImages: [],
      placeholder: '请输入您想生成的图像描述', // 默认占位符
      loading: false, //新增加载状态
      progress: 0, // 新增进度值
      intervalId: null, // 用于存储定时器ID
      selectedId: null, // 用于存储选中图片的ID
    };
  },
  methods: {
    startProgress() {
      this.progress = 0; // 初始化进度
      this.intervalId = setInterval(() => {
        if (this.progress < 100) {
          const randomIncrement = Math.floor(Math.random() * 4) + 5;
          this.progress += randomIncrement;
          if (this.progress > 100) {
            this.progress = 100; // 确保进度不会超过100%
          }
        }
      }, 1000);
    },
    stopProgress() {
      if (this.intervalId) {
        clearInterval(this.intervalId); // 清除定时器
        this.progress = 100; // 将进度设置为100%
      }
    },
    generateImage() {
      // 在这里添加图像生成逻辑
      // 设置加载状态为 true
      this.loading = true;
      this.selectedId = null;
      this.startProgress(); // 开始进度更新
      // 构造请求体
      const requestData = {
        description: this.inputText
      };

      // 发送 POST 请求到后端 API
      axios.post('http://10.177.58.143:8000/api/generate-image/', requestData)
        .then(response => {
          // // 请求成功,更新生成的图片 URL
          // this.generatedImages = response.data.urls;
          // 假设后端响应中包含图片的ID和URL
          this.generatedImages = response.data.images; // 更新为保存完整的图片对象数组
        })
        .catch(error => {
          // 请求失败,处理错误
          console.error(error);
        })
          .finally(() => {
            // 无论成功或失败,都设置加载状态为 false
            this.loading = false;
            this.stopProgress(); // 不管成功还是失败，停止进度并将其设置为100%
          });

      // this.generatedImage = 'https://via.placeholder.com/500x300'; // 替换为实际生成的图像URL
    },
    resetPlaceholder() {
      if (!this.inputText) {
        this.placeholder = '请输入您想生成的图像描述';
      }
    },
    selectImage(index){
      // 在这里添加逻辑，例如发送选中的图片信息到后端
      const selectedImageId = parseInt(this.generatedImages[index].id) // 使用图片ID

      this.selectedId = selectedImageId

      axios.post('http://10.177.58.143:8000/api/select-image/', {
        image_id: selectedImageId // 确保与后端接口期望的字段名一致
      })
      .then(response => {
        // 处理响应
        console.log('Image selected:', response.data);
      })
      .catch(error => {
        console.error('Error selecting image:', error);
      })
    }
  }
};
</script>

<style scoped>
#app {
  font-family: 'Roboto', sans-serif;
}

.logo {
  width: 200px; /* 调整为适合的大小 */
  height: auto;
  margin: 0 auto;
  display: block;
}

.search-box {
  margin-top: 50px; /* 根据需要调整 */
}

.el-row {
  flex-wrap: nowrap; /* 确保flex项不换行 */
}

.el-col {
  flex: 0 0 50%; /* 每个图像占据50%的宽度 */
  max-width: 50%; /* 最大宽度也是50% */
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

.generated-image:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 12px rgba(0,0,0,0.2);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.site-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh; /* 设置最小高度为视口高度 */
}

.site-footer {
  margin-top: auto; /* 将页脚推到底部 */
  background-color: transparent; /* 移除背景色 */
  padding: 40px 0;
  text-align: center;
}

.about-section h3 {
  margin-bottom: 20px; /* 为标题和段落之间添加一些间隔 */
}

.about-section p {
  color: #666; /* 设定段落文字颜色 */
  margin-bottom: 20px; /* 为段落和链接之间添加一些间隔 */
}

.about-section a {
  color: #337ab7; /* 设定链接颜色，您可以选择一个更符合您网站配色的颜色 */
  text-decoration: none; /* 去掉下划线 */
  transition: color 0.3s ease; /* 添加颜色渐变效果 */
}

.about-section a:hover {
  color: #23527c; /* 鼠标悬停时颜色变深 */
}

.selected-image {
  filter: none; /* 没有滤镜，显示正常亮度 */
  border: 2px solid #42b983; /* 可以用一个边框来突出显示 */
  transition: filter 0.3s ease, border-color 0.3s ease; /* 确保过渡效果适用于选中状态的变化 */
}

.unselected-image {
  filter: brightness(50%); /* 灰度加亮度滤镜 */
  cursor: pointer; /* 可以选择的光标样式 */
  transition: filter 0.3s ease; /* 应用过渡效果使变化更平滑 */
}


</style>


.el-header {
  padding: 30px 0;
  background-color: #f8f8f8;
  box-shadow: none; /* 去除阴影 */
  border: none;
}
