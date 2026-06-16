# 波士顿房价预测系统

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-orange.svg)](https://scikit-learn.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

基于机器学习的波士顿房价预测系统，使用 Tkinter 构建图形用户界面，支持多种回归算法的训练、评估和可视化。

## 功能特性

### 核心功能
- **数据管理**：内置 Boston Housing 数据集，支持上传自定义 CSV 文件
- **算法选择**：线性回归、决策树回归、随机森林回归三种算法
- **参数调优**：可调整决策树深度、随机森林树数量等超参数
- **模型训练**：一键训练模型，实时显示评估指标
- **模型管理**：支持保存和加载训练好的模型
- **单条预测**：输入特征值预测房价

### 可视化功能
- **预测对比图**：真实值 vs 预测值散点图
- **残差分布图**：残差散点图 + 直方图
- **特征重要性图**：各特征对预测的贡献度
- **决策树结构图**：可视化决策树模型（需安装 Graphviz）
- **评估指标图**：MAE、MSE、RMSE、R² 指标展示
- **算法对比图**：三种算法性能对比

## 项目结构

```
回归算法/
├── app.py                    # 主程序（Tkinter GUI）
├── requirements.txt          # Python 依赖包
├── README.md                 # 项目说明文档
├── .gitignore                # Git 忽略规则
├── data/
│   └── boston_housing.csv    # 波士顿房价数据集（506条记录）
├── models/                   # 预训练模型
│   ├── Linear Regression.pkl
│   ├── Decision Tree Regression.pkl
│   └── Random forest regression.pkl
├── utils/
│   ├── __init__.py
│   ├── data_loader.py        # 数据加载、预处理、标准化
│   ├── model.py              # 三种回归模型定义
│   └── visualization.py      # 数据可视化模块
└── tests/                    # 单元测试（30个测试用例）
    ├── __init__.py
    ├── test_data_loader.py   # 数据加载测试
    ├── test_model.py         # 模型测试
    ├── test_visualization.py # 可视化测试
    └── test_integration.py   # 集成测试
```

## 环境要求

- Python 3.8 或更高版本
- Windows / macOS / Linux

## 安装步骤

### 1. 克隆仓库

```bash
git clone https://github.com/123guoch/Machine-Learning-.git
cd Machine-Learning-/回归算法
```

### 2. 创建虚拟环境（推荐）

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 安装 Graphviz（可选）

如需使用决策树可视化功能，需要安装 Graphviz 系统软件：

1. 下载安装 [Graphviz](https://graphviz.org/download/)
2. 将安装目录的 `bin` 文件夹添加到系统 PATH
3. 重启应用

## 使用方法

### 启动应用

```bash
python app.py
```

### 操作流程

```
加载数据 → 选择算法 → 调整参数 → 训练模型 → 查看结果 → 可视化分析
```

### 详细说明

#### 1. 数据管理
- **加载内置数据集**：一键加载 Boston Housing 数据集
- **上传 CSV 文件**：加载自定义数据（需包含 `MEDV` 列作为目标变量）

#### 2. 算法选择
| 算法 | 可调参数 | 适用场景 |
|------|----------|----------|
| 线性回归 | 无 | 线性关系数据，快速基线模型 |
| 决策树回归 | 最大深度、最小样本分裂数 | 非线性关系，需要可解释性 |
| 随机森林回归 | 树的数量 | 高精度预测，减少过拟合 |

#### 3. 模型训练
- 点击「训练模型」开始训练
- 训练完成后自动显示评估指标：
  - **MAE**（平均绝对误差）
  - **MSE**（均方误差）
  - **RMSE**（均方根误差）
  - **R²**（决定系数）

#### 4. 模型管理
- **保存模型**：将训练好的模型保存为 `.pkl` 文件
- **加载模型**：加载之前保存的模型文件

#### 5. 单条预测
- 在左侧输入 13 个特征值
- 点击「预测房价」获取预测结果

## 数据集说明

本项目使用经典的 [Boston Housing Dataset](https://www.cs.toronto.edu/~delve/data/boston/bostonDetail.html)：

- **样本数量**：506 条
- **特征数量**：13 个
- **目标变量**：MEDV（房屋中位数价格，单位：$1000）

| 特征 | 描述 |
|------|------|
| CRIM | 城镇人均犯罪率 |
| ZN | 占地面积超过 25,000 平方英尺的住宅用地比例 |
| INDUS | 非零售商业用地比例 |
| CHAS | 查尔斯河虚拟变量（1=临河，0=不临河） |
| NOX | 一氧化氮浓度 |
| RM | 平均房间数 |
| AGE | 1940 年前建成的自住单位比例 |
| DIS | 到波士顿五个就业中心的加权距离 |
| RAD | 径向公路可达性指数 |
| TAX | 每 $10,000 的全额物业税率 |
| PTRATIO | 城镇师生比例 |
| B | 1000(Bk - 0.63)²，Bk 为城镇黑人比例 |
| LSTAT | 低收入人口比例 |
| MEDV | 自住房屋中位数价值（目标变量） |

```

## 技术栈

| 技术 | 用途 |
|------|------|
| Python 3.8+ | 编程语言 |
| scikit-learn | 机器学习算法（线性回归、决策树、随机森林） |
| pandas | 数据处理和分析 |
| numpy | 数值计算 |
| matplotlib | 数据可视化 |
| tkinter | 图形用户界面 |
| graphviz | 决策树结构可视化（可选） |
| pytest | 单元测试框架 |
