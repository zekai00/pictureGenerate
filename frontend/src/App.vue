<template>
  <div id="app" class="site-container">
    <el-container>
      <!-- 顶部导航栏区域 -->
      <top-bar></top-bar>

      <!-- 主内容区域 -->
      <el-main>
        <div class="search-container">
          <el-row type="flex" justify="center">
            <el-col :span="12">
              <div class="search-box">
                <el-input
                  type="textarea"
                  v-model="inputText"
                  :rows="4"
                  placeholder="请输入您想生成图像的诗："
                  prefix-icon="el-icon-edit"
                  clearable
                  class="input-with-button"
                  @focus="placeholder = ''"
                  @blur="resetPlaceholder"
                >
                </el-input>
                <el-button type="primary" shape="circle" icon="el-icon-search" class="search-button" @click="generateImage">生成</el-button>
              </div>
              <!-- 加载进度条 -->
              <div v-if="loading" class="progress-container">
                <el-progress :percentage="progress"></el-progress>
              </div>
            </el-col>
          </el-row>
          <el-row type="flex" justify="center">
            <el-col :span="18">
              <div class="style-selector">
                <el-select v-model="selectedStyle" placeholder="请选择书法风格">
                  <el-option
                    v-for="style in calligraphyStyles"
                    :key="style"
                    :label="style"
                    :value="style">
                  </el-option>
                </el-select>
              </div>
            </el-col>
          </el-row>
          <el-row type="flex" justify="center" class="calligraphy-container">
            <el-col :span="10" v-for="(calligraphy, index) in generatedCalligraphies" :key="`calligraphy-${index}`">
              <el-image
                :src="calligraphy.url"
                fit="contain"
                class="generated-calligraphy"
                @click="selectCalligraphy(index)"
              ></el-image>
            </el-col>
          </el-row>
          <!-- 展示生成的图片 -->
          <el-row v-if="generatedImages.length > 0" type="flex" justify="center" class="image-container">
            <el-col :span="12" v-for="(image, index) in generatedImages" :key="index">
              <el-image
                :src="image.url"
                fit="contain"
                class="generated-image"
                @click="selectImage(index)"
              ></el-image>
            </el-col>
          </el-row>
        </div>
      </el-main>

      <!-- 页脚区域 -->
      <el-footer>
        <div class="site-footer">
          <h3>关于我们</h3>
          <p>我们是复旦大学计算机学院的IMC实验室。</p>
        </div>
      </el-footer>
    </el-container>
  </div>
</template>

<script>
// import Vue from 'vue'
import axios from 'axios'
import TopBar from './components/TopBar.vue'

// 解决ERROR ResizeObserver loop completed with undelivered notifications.

const debounce = (fn, delay) => {
  let timer = null;
  return function () {
    let context = this;
    let args = arguments;
    clearTimeout(timer);
    timer = setTimeout(function () {
      fn.apply(context, args);
    }, delay);
  }
}

// 解决ERROR ResizeObserver loop completed with undelivered notifications
const _ResizeObserver = window.ResizeObserver;
window.ResizeObserver = class ResizeObserver extends _ResizeObserver {
  constructor(callback) {
    callback = debounce(callback, 16);
    super(callback);
  }
}

export default {
  components: {
    TopBar // 注册组件
  },
  data() {
    return {
      bannerImage: './assets/fudan2.png', // 你的logo URL
      inputText: '',
      generatedImages: [],
      generatedCalligraphies: [], // 新增用于存储书法图像的数组
      calligraphyStyles: [], // 存储书法风格列表
      selectedStyle: '', // 存储所选的书法风格
      placeholder: '请输入您想生成的图像描述', // 默认占位符
      loading: false, //新增加载状态
      progress: 0, // 新增进度值
      intervalId: null, // 用于存储定时器ID
      selectedId: null, // 用于存储选中图片的ID
    };
  },
  methods: {
    created() {
      this.loadCalligraphyStyles();
    },
    startProgress() {
      this.progress = 0; // 初始化进度
      this.intervalId = setInterval(() => {
        if (this.progress < 100) {
          const randomIncrement = Math.floor(Math.random() * 3) + 4;
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
    },
    generateCalligraphy() {
      // 发送请求到书法生成接口
      axios.post('http://imc.v1.idcfengye.com/cn-calligraphy/api/generate', {
        style: '',
        characters: '中文内容'
      })
      .then(response => {
        // 请求成功,处理返回的书法图像数据
        this.generatedCalligraphies = response.data.images.map(image => ({
          url: `data:image/png;base64,${image}` // 转换base64编码为图片URL
        })); // 存储到数组中
      })
      .catch(error => {
        // 请求失败,处理错误
        console.error('Error generating calligraphy:', error);
      });
    },
    loadCalligraphyStyles() {
      // 发送请求到书法风格列表接口
      axios.post('http://imc.v1.idcfengye.com/cn-calligraphy/api/list-style', '{}', {
        headers: {
          'Content-Type': 'text/plain'
        }
      })
      .then(response => {
        console.log('Styles loaded:', response.data); // 输出返回的数据
        // 请求成功,处理返回的书法风格数据
        this.calligraphyStyles = response.data.styles; // 存储到数组中
      })
      .catch(error => {
        // 请求失败,处理错误
        console.error('Error loading calligraphy styles:', error);
      });
    },

  }
};
</script>

<style>
#app {
  font-family: 'Roboto', sans-serif;
}

body {
  background-image: url('/data/picgen/frontend/public/pics/back.jpg'); /* 这里的路径需要替换成您图片的实际存放路径 */
  background-size: cover; /* 确保图片覆盖整个页面 */
  background-position: center center; /* 图片居中显示 */
  background-repeat: no-repeat; /* 不重复图片 */
  background-attachment: fixed; /* 背景图片固定 */
}

.logo {
  width: 200px; /* 调整为适合的大小 */
  height: auto;
  display: block;
}

.search-box {
  display: flex; /* 使用flex布局 */
  align-items: center; /* 垂直居中 */
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
  flex: 1; /* 输入框占据剩余空间 */
  margin-right: 10px; /* 与按钮间距 */
}

.search-button {
  width: 50px; /* 按钮宽度 */
  height: 50px; /* 按钮高度，确保和宽度相同形成正方形 */
  line-height: 50px; /* 与高度相同，以便图标垂直居中 */
  padding: 0; /* 移除内边距，特别是如果按钮内包含文本的话 */
  border-radius: 50%; /* 创建圆形 */
  text-align: center; /* 确保文字水平居中 */
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

.calligraphy-container {
  margin-top: 20px; /* 根据需要调整间距 */
}

.style-selector {
  text-align: center; /* 让下拉条居中显示 */
  margin: 20px 0; /* 添加上下的边距 */
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

.el-header {
  display: flex;
  justify-content: space-between; /* 左右两侧对齐 */
  align-items: flex-start;
  flex-wrap: wrap; /* 允许元素换行 */
}

</style>
