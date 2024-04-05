# 使用带有预安装 Nginx 的官方基础镜像
FROM nginx:alpine

# 将 dist 目录中的文件复制到 Nginx 用来提供静态文件的目录中
COPY dist/ /usr/share/nginx/html/

# 复制自定义的 Nginx 配置文件到配置目录中
COPY default.conf /etc/nginx/conf.d/default.conf

## 启动 Nginx 服务器
#CMD ["nginx", "-g", "daemon off;"]