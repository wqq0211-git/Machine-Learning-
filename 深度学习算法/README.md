# 基于 CNN 与 ResNet-18 的 CIFAR-10 图像分类对比系统

本项目是机器学习课程项目中的“深度学习算法”模块，完成 CIFAR-10 图像分类任务的训练、评估、后端推理接口和前端可视化展示。

系统包含两个模型：

- 自定义卷积神经网络 CNN
- 基于 torchvision 的 ResNet-18 迁移学习模型

前后端分离：

- 后端：FastAPI + PyTorch
- 前端：Vue 3 + Vite + Element Plus + ECharts
- 数据集：CIFAR-10
- 操作系统：Windows

## 1. 项目功能

- 自动下载并读取 CIFAR-10 数据集
- CNN 与 ResNet-18 两种模型训练
- 训练集、验证集、测试集划分
- 训练历史 JSON 保存
- 测试集 Accuracy、Precision、Recall、F1、AUC、混淆矩阵评估
- 单张图片预测
- CNN 与 ResNet-18 双模型预测对比
- 批量图片预测
- 前端图表展示训练曲线、模型指标和混淆矩阵
- 权重不存在时后端仍可正常启动
- Windows 一键启动脚本

## 2. 目录结构

```text
深度学习算法/
├─ README.md
├─ .gitignore
├─ start_backend.bat
├─ start_frontend.bat
├─ start_all.bat
├─ backend/
│  ├─ main.py
│  ├─ requirements.txt
│  ├─ app/
│  │  ├─ config.py
│  │  ├─ model_manager.py
│  │  ├─ preprocessing.py
│  │  ├─ prediction.py
│  │  ├─ schemas.py
│  │  └─ routers/
│  ├─ training/
│  │  ├─ dataset.py
│  │  ├─ models.py
│  │  ├─ train.py
│  │  ├─ evaluate.py
│  │  ├─ visualize.py
│  │  └─ utils.py
│  ├─ models/
│  ├─ results/
│  └─ tests/
├─ frontend/
│  ├─ package.json
│  ├─ vite.config.js
│  ├─ index.html
│  └─ src/
└─ docs/
```

## 3. 环境要求

推荐环境：

- Python 3.10 或 3.11
- Node.js 18 或更高版本
- Conda
- NVIDIA GPU 可选

本项目已经在以下环境验证过：

- Python 3.11
- PyTorch CUDA 12.8
- NVIDIA GeForce RTX 5060
- Node.js 24

## 4. 创建后端环境

推荐使用 conda 环境：

```powershell
cd D:\作业\机器学习\深度学习算法\backend

conda create -n ml-cifar python=3.11 -y
conda activate ml-cifar

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

如果你使用 RTX 50 系列显卡，例如 RTX 5060，并看到 `sm_120 is not compatible` 警告，需要安装支持 CUDA 12.8 的 PyTorch：

```powershell
pip uninstall torch torchvision torchaudio -y
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
```

验证 GPU：

```powershell
python -c "import torch; print(torch.__version__); print(torch.version.cuda); print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0)); print(torch.cuda.get_device_capability(0))"
```

正常情况下应看到：

```text
True
NVIDIA GeForce RTX 5060
(12, 0)
```

## 5. 安装前端依赖

```powershell
cd D:\作业\机器学习\深度学习算法\frontend
npm install
```

## 6. 启动后端

```powershell
cd D:\作业\机器学习\深度学习算法\backend
conda activate ml-cifar
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

启动成功后会看到：

```text
Uvicorn running on http://127.0.0.1:8000
Application startup complete.
```

后端地址：

- 接口文档：http://127.0.0.1:8000/docs
- 健康检查：http://127.0.0.1:8000/api/health

注意：`http://127.0.0.1:8000/` 返回 `{"detail":"Not Found"}` 是正常的，因为后端根路径没有做首页。

## 7. 启动前端

另开一个 PowerShell：

```powershell
cd D:\作业\机器学习\深度学习算法\frontend
npm run dev
```

前端页面：

```text
http://127.0.0.1:5173/
```

前端默认通过 `.env.development` 连接后端：

```text
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

## 8. 一键启动脚本

也可以在项目根目录运行：

```powershell
cd D:\作业\机器学习\深度学习算法
.\start_all.bat
```

脚本会分别打开后端和前端命令行窗口。

## 9. 训练模型

### 训练 CNN

```powershell
cd D:\作业\机器学习\深度学习算法\backend
conda activate ml-cifar
python -m training.train --model cnn --device cuda --batch-size 128
```

如果没有 GPU：

```powershell
python -m training.train --model cnn --device cpu --epochs 3
```

### 训练 ResNet-18

```powershell
python -m training.train --model resnet18 --pretrained --device cuda --batch-size 64
```

如果显存不够，把 batch size 调小：

```powershell
python -m training.train --model resnet18 --pretrained --device cuda --batch-size 32
```

如果只是快速演示，可以冻结 backbone 并减少 epoch：

```powershell
python -m training.train --model resnet18 --pretrained --freeze-backbone --epochs 2 --batch-size 64 --device cuda
```

训练完成后会生成：

```text
backend/models/cnn_best.pth
backend/models/resnet18_best.pth
backend/models/model_info.json
backend/results/training_history.json
```

## 10. 评估模型

两个模型都训练完成后运行：

```powershell
cd D:\作业\机器学习\深度学习算法\backend
conda activate ml-cifar
python -m training.evaluate --model all --device cuda
```

生成结果：

```text
backend/results/metrics.json
backend/results/class_metrics.json
backend/results/confusion_matrix_cnn.json
backend/results/confusion_matrix_resnet18.json
```

生成可视化图片：

```powershell
python -m training.visualize
```

图片输出目录：

```text
backend/results/figures/
```

## 11. 后端接口

统一前缀：

```text
/api
```

主要接口：

```text
GET  /api/health
GET  /api/models
POST /api/predict
POST /api/predict/compare
POST /api/predict/batch
GET  /api/metrics
GET  /api/training-history
GET  /api/confusion-matrix/{model_name}
GET  /api/class-metrics/{model_name}
GET  /api/dataset
```

详细接口说明见：

```text
docs/接口文档.md
```

## 12. 前端页面

```text
/               首页
/predict        单张图像识别
/batch-predict  批量预测
/compare        模型对比
/dataset        数据集分析
/about          项目说明
```

当前页面支持：

- 上传 JPG、JPEG、PNG 图片
- CNN 单模型预测
- ResNet-18 单模型预测
- 双模型对比预测
- Top-3 类别展示
- 十分类概率图
- 训练指标和混淆矩阵展示

## 13. 测试与构建

后端编译检查：

```powershell
cd D:\作业\机器学习\深度学习算法\backend
conda activate ml-cifar
python -m compileall .
```

后端测试：

```powershell
pytest
```

前端生产构建：

```powershell
cd D:\作业\机器学习\深度学习算法\frontend
npm run build
```

当前已验证：

```text
python -m compileall . 通过
pytest 通过
npm run build 通过
后端 /api/health 返回 200
前端 http://127.0.0.1:5173/ 可访问
```

## 14. 常见问题

### 14.1 打开 http://127.0.0.1:8000 显示 Not Found

正常。后端根路径没有首页。请打开：

```text
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/api/health
```

真正的网页界面是：

```text
http://127.0.0.1:5173/
```

### 14.2 前端显示 Network Error

通常是后端没启动、端口不对，或后端接口报错。

检查：

```powershell
Invoke-WebRequest http://127.0.0.1:8000/api/health
```

如果后端终端有报错，先看 traceback。

本项目已修复 CNN 上传大图预测时的尺寸问题：CNN 推理会自动将上传图片缩放到 `32x32`，ResNet-18 会缩放到 `224x224`。

### 14.3 端口 8000 被占用

查看占用：

```powershell
netstat -ano | findstr :8000
```

结束进程：

```powershell
Stop-Process -Id 进程ID -Force
```

或改用 8001：

```powershell
python -m uvicorn main:app --host 127.0.0.1 --port 8001 --reload
```

如果后端端口改成 8001，前端 `.env.development` 也要改成：

```text
VITE_API_BASE_URL=http://127.0.0.1:8001/api
```

### 14.4 模型权重不存在

没有权重时后端可以启动，但预测接口会返回 503。请先训练：

```powershell
python -m training.train --model cnn --device cuda
python -m training.train --model resnet18 --pretrained --device cuda
```

训练后重启后端，让 `ModelManager` 重新加载权重。

### 14.5 ResNet-18 训练很慢

CPU 训练会很慢。建议使用 CUDA：

```powershell
python -m training.train --model resnet18 --pretrained --device cuda --batch-size 64
```

如果 GPU 是 RTX 50 系列，请确认 PyTorch 是 CUDA 12.8 版本。

## 15. Git 提交注意事项

`.gitignore` 已排除：

- `node_modules`
- `dist`
- Python 缓存
- pytest 缓存
- 虚拟环境
- CIFAR-10 原始数据
- 训练权重 `.pth`
- 结果图片
- 日志文件

正式提交时建议提交：

- 源代码
- 配置文件
- 文档
- 初始 JSON 文件

不要提交：

- `backend/data/`
- `backend/models/*.pth`
- `frontend/node_modules/`
- `frontend/dist/`
- `.venv/`

