# 波士顿房价预测系统

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-orange.svg)](https://scikit-learn.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

一个基于机器学习的波士顿房价预测系统，支持多种回归算法，提供可视化界面和模型评估功能。

## 功能特性

- **多种回归算法**：线性回归、决策树回归、随机森林回归
- **可视化界面**：基于 Tkinter 的图形用户界面
- **模型评估**：MAE、MSE、RMSE、R² 等评估指标
- **数据可视化**：预测对比图、残差分布图、特征重要性图
- **模型管理**：模型训练、保存、加载功能
- **决策树可视化**：生成决策树结构图（需要 Graphviz）

## 项目结构

```
回归算法/
├── app.py                    # 主程序入口
├── requirements.txt          # 依赖包列表
├── README.md                 # 项目说明
├── data/
│   └── boston_housing.csv    # 波士顿房价数据集
├── models/                   # 预训练模型
│   ├── Linear Regression.pkl
│   ├── Decision Tree Regression.pkl
│   └── Random forest regression.pkl
├── utils/
│   ├── data_loader.py        # 数据加载和预处理
│   ├── model.py              # 模型定义和训练
│   └── visualization.py      # 数据可视化
└── tests/                    # 单元测试
    ├── test_data_loader.py
    ├── test_model.py
    ├── test_visualization.py
    └── test_integration.py
```

## 安装

### 环境要求

- Python 3.8+
- pip

### 安装步骤

1. 克隆仓库

```bash
git clone https://github.com/123guoch/Machine-Learning-.git
cd Machine-Learning-/回归/回归算法
```

2. 创建虚拟环境（推荐）

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

3. 安装依赖

```bash
pip install -r requirements.txt
```

4. 安装 Graphviz（可选，用于决策树可视化）

- 下载并安装 [Graphviz](https://graphviz.org/download/)
- 将安装目录的 `bin` 文件夹添加到系统 PATH

## 使用方法

### 启动应用

```bash
python app.py
```

### 功能说明

1. **数据管理**
   - 点击「加载内置数据集」加载 Boston Housing 数据集
   - 点击「上传CSV文件」加载自定义数据（需包含 MEDV 列）

2. **算法选择**
   - 选择回归算法：线性回归、决策树回归、随机森林回归
   - 调整模型参数（决策树和随机森林支持）

3. **模型训练**
   - 点击「训练模型」开始训练
   - 训练完成后显示评估指标

4. **模型管理**
   - 点击「保存模型」保存训练好的模型
   - 点击「加载模型」加载之前保存的模型

5. **数据可视化**
   - 预测对比图：展示预测值与真实值的对比
   - 残差分布图：分析模型预测误差
   - 特征重要性图：查看各特征对预测的影响
   - 决策树结构：可视化决策树模型
   - 评估指标图：展示模型评估指标
   - 算法对比：比较不同算法的性能

## 数据集

本项目使用经典的 [Boston Housing Dataset](https://www.cs.toronto.edu/~delve/data/boston/bostonDetail.html)，包含 506 个样本，13 个特征：

| 特征 | 描述 |
|------|------|
| CRIM | 城镇人均犯罪率 |
| ZN | 占地面积超过25,000平方英尺的住宅用地比例 |
| INDUS | 非零售商业用地比例 |
| CHAS | 查尔斯河虚拟变量（1=临河，0=不临河） |
| NOX | 一氧化氮浓度 |
| RM | 平均房间数 |
| AGE | 1940年前建成的自住单位比例 |
| DIS | 到波士顿五个就业中心的加权距离 |
| RAD | 径向公路可达性指数 |
| TAX | 每10,000美元的全额物业税率 |
| PTRATIO | 城镇师生比例 |
| B | 1000(Bk - 0.63)²，其中 Bk 是城镇黑人比例 |
| LSTAT | 低收入人口比例 |
| MEDV | 自住房屋的中位数价值（目标变量，单位：$1000） |

## 测试

运行所有测试：

```bash
python -m pytest tests/ -v
```

运行特定测试：

```bash
python -m pytest tests/test_model.py -v
```

## 技术栈

- **Python 3.8+**
- **scikit-learn**：机器学习算法
- **pandas**：数据处理
- **numpy**：数值计算
- **matplotlib**：数据可视化
- **tkinter**：图形用户界面
- **graphviz**：决策树可视化

## 贡献指南

欢迎贡献！请遵循以下步骤：

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建一个 Pull Request

## 许可证

本项目使用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 致谢

- [Boston Housing Dataset](https://www.cs.toronto.edu/~delve/data/boston/bostonDetail.html)
- [scikit-learn](https://scikit-learn.org/)
- [Matplotlib](https://matplotlib.org/)

## 联系方式

项目链接：[https://github.com/123guoch/Machine-Learning-](https://github.com/123guoch/Machine-Learning-)
