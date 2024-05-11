<template>
  <div id="app" class="site-container">
    <el-container>
      <!-- 主内容区域 -->
      <el-main>
        <div class="search-container">
          <el-row type="flex" justify="center">
            <el-col :span="3">
              <div class="style-selector">
                <el-select v-model="selectedStyle" placeholder="书法风格加载中...">
                  <el-option
                    v-for="style in calligraphyStyles"
                    :key="style"
                    :label="style"
                    :value="style">
                  </el-option>
                </el-select>
              </div>
            </el-col>
            <el-col :span="3">
              <div class="direction-selector">
                  <el-select v-model="generationDirection" placeholder="请选择生成方向">
                    <el-option label="书法横向生成" value="horizontal"></el-option>
                    <el-option label="书法纵向生成" value="vertical"></el-option>
                  </el-select>
                </div>
            </el-col>
            <el-col :span="10">
              <div class="search-box">
                <el-input
                  type="textarea"
                  v-model="inputText"
                  :rows="2"
                  placeholder="请在此处输入诗文，点击右侧按钮即可生成："
                  prefix-icon="el-icon-edit"
                  clearable
                  class="input-with-button"
                  @focus="placeholder = ''"
                  @blur="resetPlaceholder"
                >
                </el-input>
                <el-button
                  shape="circle"
                  style="padding:25px 25px"
                  class="search-button"
                  @click="generateAll1"
                  :style="backgroundImageStyle"
                ></el-button>
              </div>
              <!-- 加载进度条 -->
              <div v-if="loading" class="progress-container">
                <el-progress :percentage="progress"></el-progress>
              </div>
            </el-col>
          </el-row>
          <!-- 展示生成的书法 -->
          <el-row type="flex" justify="center" class="calligraphy-container" :class="{'text-align-right': appliedGenerationDirection === 'vertical'}" style="margin: 10px 20px;" :gutter="20">
            <el-col :span="12" v-for="(calligraphy, index) in generatedCalligraphies" :key="`calligraphy-${index}`">
              <el-image
                :src="calligraphy.url"
                fit="contain"
                :class="{'horizontal-calligraphy': appliedGenerationDirection === 'horizontal',
                         'vertical-calligraphy': appliedGenerationDirection === 'vertical'}"
              ></el-image>
            </el-col>
          </el-row>
          <!-- 展示生成的图片 -->
          <el-row v-if="generatedImages.length > 0" type="flex" justify="center" class="image-container" style="margin: 10px 20px;" :gutter="20">
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
          <AppTopBar></AppTopBar>
        </div>
      </el-footer>
    </el-container>
  </div>
</template>

<script>
// import Vue from 'vue'
import axios from 'axios'
import AppTopBar from './components/Topbar.vue'

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
    AppTopBar // 注册组件
  },
  computed: {
    backgroundImageStyle() {
      // 需要正确配置webpack以解析@别名
      return `background-image: url('${require('@/assets/maliangLOGO/iconwhite.png')}'); background-size: cover;`;
    }
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
      historicalImages: [],
      historicalCalligraphies: [],
      generationDirection: 'horizontal', // 默认为横向生成
      appliedGenerationDirection: 'horizontal',
    };
  },
  mounted() {
    this.loadCalligraphyStyles();
  },
  methods: {
    startProgress() {
      this.progress = 0; // 初始化进度
      this.intervalId = setInterval(() => {
        if (this.progress < 100) {
          const randomIncrement = Math.floor(Math.random() * 3) + 3;
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


    generateAll1() {
      this.generatedImages = [];
      this.generatedCalligraphies = [];
      this.generateImage();

      if (this.generationDirection === 'horizontal') {
        Promise.all([
          this.generateHorizontalCalligraphy(),
          this.generateHorizontalCalligraphy()
        ])
        .then(calligraphyUrls => {
          this.generatedCalligraphies = calligraphyUrls.map(url => ({url}));
          this.appliedGenerationDirection = this.generationDirection;
        })
        .catch(error => {
          console.error('Error generating calligraphies:', error);
        });
      } else if (this.generationDirection === 'vertical') {
        Promise.all([
          this.generateVerticalCalligraphy(),
          this.generateVerticalCalligraphy()
        ])
        .then(calligraphyUrls => {
          this.generatedCalligraphies = calligraphyUrls.map(url => ({url}));
          this.appliedGenerationDirection = this.generationDirection;
        })
        .catch(error => {
          console.error('Error generating calligraphies:', error);
        });
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
          this.generatedImages = response.data.images.map(img => ({
            url: `data:image/png;base64,${img.base64}`
          }));
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

    // generateCalligraphy() {
    //   // 发送请求到书法生成接口
    //   axios.post('http://imc.v1.idcfengye.com/cn-calligraphy/api/generate', {
    //     style: this.selectedStyle,
    //     characters: this.inputText
    //   })
    //   .then(response => {
    //     // 请求成功,处理返回的书法图像数据
    //     this.generatedCalligraphies = response.data.images.map(image => ({
    //       url: `data:image/png;base64,${image}` // 转换base64编码为图片URL
    //     })); // 存储到数组中
    //   })
    //   .catch(error => {
    //     // 请求失败,处理错误
    //     console.error('Error generating calligraphy:', error);
    //   });
    // },

    // generateCalligraphy() {
    //   // 分割输入文本为多行
    //   const lines = this.inputText.split('\n');
    //
    //   // 初始化一个空数组，用于存放每行书法图片的数组
    //   let allLinesPromises = [];
    //
    //   // 处理每一行文本
    //   lines.forEach(line => {
    //     // 对于每一行文本，发送请求到书法生成接口
    //     let linePromise = axios.post('http://imc.v1.idcfengye.com/cn-calligraphy/api/generate', {
    //       style: this.selectedStyle,
    //       characters: line
    //     }).then(response => {
    //       // 对于这一行返回的每个字的书法图像，创建一个加载它们的Promise数组
    //       let charImagePromises = response.data.images.map(base64Image => {
    //         return new Promise((resolve, reject) => {
    //           let img = new Image();
    //           img.onload = () => resolve(img);
    //           img.onerror = () => reject(new Error('Image load failed'));
    //           img.src = `data:image/png;base64,${base64Image}`;
    //         });
    //       });
    //       // 等待这一行中所有字的书法图像加载完成
    //       return Promise.all(charImagePromises);
    //     });
    //     // 将每一行的Promise添加到数组中
    //     allLinesPromises.push(linePromise);
    //   });
    //
    //   // 当所有行的Promise都完成后
    //   Promise.all(allLinesPromises).then(linesImages => {
    //     // 创建一个画布元素
    //     let canvas = document.createElement('canvas');
    //     let ctx = canvas.getContext('2d');
    //
    //     // 计算画布的总高度和最大宽度
    //     let totalHeight = 0;
    //     let maxWidth = 0;
    //     linesImages.forEach(images => {
    //       // 叠加每一行的高度
    //       totalHeight += images[0].height;
    //       // 找到最宽的行的宽度
    //       let lineWidth = images.reduce((sum, img) => sum + img.width, 0);
    //       maxWidth = Math.max(maxWidth, lineWidth);
    //     });
    //
    //     // 设置画布尺寸
    //     canvas.width = maxWidth;
    //     canvas.height = totalHeight;
    //
    //     // 将每行图片绘制到画布上
    //     let currentHeight = 0;
    //     linesImages.forEach(images => {
    //       let currentWidth = 0;
    //       images.forEach(img => {
    //         ctx.drawImage(img, currentWidth, currentHeight);
    //         currentWidth += img.width;
    //       });
    //       currentHeight += images[0].height;
    //     });
    //
    //     // 将最终的书法图像添加到数组中
    //     let imageUrl = canvas.toDataURL('image/png');
    //     this.generatedCalligraphies.push({ url: imageUrl });
    //   })
    //   .catch(error => {
    //     // 处理错误
    //     console.error('Error generating calligraphy lines:', error);
    //   });
    // },

    generateHorizontalCalligraphy() {
      return new Promise((resolve, reject) => {
        // 分割输入文本为多行并处理每行
        const lines = this.inputText.split('\n').map(line => {
          // 移除句尾的标点
          line = line.replace(/[，。！？]$/, '');
          // 处理空格和内部标点为特定的占位符，这里我们用特殊字符表示空隙
          return line.replace(/\s+/g, '').replace(/[，。！？]/g, '');
        });
        let allLinesPromises = lines.map(line => {
          return axios.post('http://imc.v1.idcfengye.com/cn-calligraphy/api/generate', {
            style: this.selectedStyle,
            characters: line
          }).then(response => {
            let charImagePromises = response.data.images.map(base64Image => {
              return new Promise((resolve, reject) => {
                let img = new Image();
                img.onload = () => resolve(img);
                img.onerror = reject;
                img.src = `data:image/png;base64,${base64Image}`;
              });
            });
            return Promise.all(charImagePromises);
          });
        });

        Promise.all(allLinesPromises).then(linesImages => {
          let canvas = document.createElement('canvas');
          let ctx = canvas.getContext('2d');
          let totalHeight = 0, maxWidth = 0;
          linesImages.forEach(images => {
            totalHeight += images[0].height;
            let lineWidth = images.reduce((sum, img) => sum + img.width, 0);
            maxWidth = Math.max(maxWidth, lineWidth);
          });

          // 设置画布尺寸
          canvas.width = maxWidth;
          canvas.height = totalHeight;

          let currentHeight = 0;
          linesImages.forEach(images => {
            let currentWidth = 0;
            images.forEach(img => {
              ctx.drawImage(img, currentWidth, currentHeight);
              currentWidth += img.width;
            });
            currentHeight += images[0].height;
          });

          resolve(canvas.toDataURL('image/png')); // 将最终的书法图像作为Promise的结果返回
        }).catch(reject);
      });
    },

    generateVerticalCalligraphy() {
      return new Promise((resolve, reject) => {
        // 分割输入文本为多行并处理每行
        const lines = this.inputText.split('\n').map(line => {
          // 移除句尾的标点
          line = line.replace(/[，。！？]$/, '');
          // 处理空格和内部标点为特定的占位符，这里我们用特殊字符表示空隙
          return line.replace(/\s+/g, '').replace(/[，。！？]/g, '');
        });

        let allLinesPromises = lines.map(line => {
          return axios.post('http://imc.v1.idcfengye.com/cn-calligraphy/api/generate', {
            style: this.selectedStyle,
            characters: line
          }).then(response => {
            let charImagePromises = response.data.images.map(base64Image => {
              return new Promise((resolve, reject) => {
                let img = new Image();
                img.onload = () => resolve(img);
                img.onerror = reject;
                img.src = `data:image/png;base64,${base64Image}`;
              });
            });
            return Promise.all(charImagePromises);
          });
        });

        Promise.all(allLinesPromises).then(linesImages => {
          let canvas = document.createElement('canvas');
          let ctx = canvas.getContext('2d');

          // 确定画布的宽度和高度
          let canvasWidth = linesImages.reduce((width, images) => width + images[0].width, 0);
          let canvasHeight = Math.max(...linesImages.map(images => images.reduce((sum, img) => sum + img.height, 0)));

          canvas.width = canvasWidth;
          canvas.height = canvasHeight;

          let currentX = canvasWidth; // 从画布的最右侧开始绘制

          // 从右向左绘制每一列
          linesImages.forEach(images => {
            let columnWidth = images[0].width; // 假设每一列的宽度都一样
            currentX -= columnWidth; // 更新绘制列的X坐标
            let currentY = 0; // 从画布的最上方开始绘制

            images.forEach(img => {
              ctx.drawImage(img, currentX, currentY); // 绘制图片
              currentY += img.height; // 更新Y坐标，以绘制下一个字符
            });
          });

          resolve(canvas.toDataURL('image/png')); // 返回绘制完成的书法图像
        }).catch(reject);
      });
    },

    loadCalligraphyStyles() {
      // 发送请求到书法风格列表接口
      axios.post('http://imc.v1.idcfengye.com/cn-calligraphy/api/list-style', '{}', {
        headers: {
          'Content-Type': 'application/json'
        }
      })
      .then(response => {
        console.log('Styles loaded:', response.data); // 输出返回的数据
        // 请求成功,处理返回的书法风格数据
        this.calligraphyStyles = response.data.styles; // 存储到数组中
        if (this.calligraphyStyles.length > 0) {
          this.selectedStyle = this.calligraphyStyles[0];
        }
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
  min-height: 80vh;
  display: flex;
  flex-direction: column;
}

body {
  background-image: url('D:/FDUGRAGUATE/picgen/frontend/public/pics/back.jpg'); /* 这里的路径需要替换成您图片的实际存放路径 */
  background-size: cover; /* 确保图片覆盖整个页面 */
  background-position: center center; /* 图片居中显示 */
  background-repeat: no-repeat; /* 不重复图片 */
  background-attachment: fixed; /* 背景图片固定 */
}

.logo-top {
  width: 300px; /* 或其他宽度，根据需要调整 */
  height: auto; /* 保持图片的原始宽高比 */
  display: block; /* 这将使元素呈现为块级 */
  margin-top: 20px;
  margin-left: auto; /* 水平居中的关键 */
  margin-right: auto; /* 水平居中的关键 */
}

.search-container{
  margin-top: 30px; /* 根据需要调整 */
  align-items: flex-start;
}

.search-box {
  display: flex; /* 使用flex布局 */
  align-items: flex-start; /* 垂直居中 */
}

/* 自定义按钮样式 */
.search-button {
  background-color: transparent; /* 设置按钮背景透明 */
  border: none; /* 移除边框 */
  align-items: flex-start;
  padding: 25px 25px;
  /* 其他必要的样式调整... */
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

.generated-image:hover {
  margin: 0 10px;
  transform: scale(1.05);
  box-shadow: 0 6px 12px rgba(0,0,0,0.2);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.site-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh; /* 设置最小高度为视口高度 */
}

.el-main {
  overflow-y: auto; /* 如果内容过多，允许在el-main内部滚动 */
  flex: 1; /* 让el-main占据除了头部和尾部之外的所有空间 */
}

.site-footer {
  flex-shrink: 0; /* 确保页脚不会因为容器的缩放而隐藏 */
}

.calligraphy-container {
  max-width: 100%; /* 容器宽度不超过其父元素 */
  max-height: 100vh; /* 高度不超过视口高度 */
  margin-top: 20px; /* 根据需要调整间距 */
}

.text-align-right {
  text-align: right;
}

/* 横向生成的样式 */
.horizontal-calligraphy {
  /* ... */
}

/* 纵向生成的样式 */
.vertical-calligraphy {
  height: 600px;
  width: fit-content;
  /* ... */
}

.direction-selector{
  margin-right: 20px;
}

.style-selector {
  text-align: center; /* 让下拉条居中显示 */
  margin-right: 20px;
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
  justify-content: space-around; /* 左右两侧对齐 */
  align-items: center;
  flex-wrap: wrap; /* 允许元素换行 */
}

</style>
