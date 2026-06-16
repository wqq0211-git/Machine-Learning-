import matplotlib.pyplot as plt
import numpy as np
import os

# 添加Graphviz到PATH
graphviz_path = r"C:\Program Files\Graphviz\bin"
if os.path.exists(graphviz_path):
    os.environ["PATH"] = graphviz_path + ";" + os.environ.get("PATH", "")

from sklearn.tree import export_graphviz
import graphviz


class Visualizer:
    def __init__(self):
        plt.style.use('seaborn-v0_8' if 'seaborn-v0_8' in plt.style.available else 'default')
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False

    def plot_predictions(self, y_true, y_pred, title="预测值 vs 真实值"):
        """绘制预测值对比图"""
        fig, ax = plt.subplots(figsize=(8, 6))

        ax.scatter(y_true, y_pred, alpha=0.6, edgecolors='w', linewidth=0.5)

        # 绘制对角线
        min_val = min(min(y_true), min(y_pred))
        max_val = max(max(y_true), max(y_pred))
        ax.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='完美预测')

        ax.set_xlabel('真实值', fontsize=12)
        ax.set_ylabel('预测值', fontsize=12)
        ax.set_title(title, fontsize=14)
        ax.legend()
        ax.grid(True, alpha=0.3)

        return fig

    def plot_residuals(self, y_true, y_pred, title="残差分布"):
        """绘制残差分布图"""
        residuals = np.array(y_true) - np.array(y_pred)

        fig, axes = plt.subplots(1, 2, figsize=(12, 5))

        # 残差散点图
        axes[0].scatter(y_pred, residuals, alpha=0.6, edgecolors='w', linewidth=0.5)
        axes[0].axhline(y=0, color='r', linestyle='--', lw=2)
        axes[0].set_xlabel('预测值', fontsize=12)
        axes[0].set_ylabel('残差', fontsize=12)
        axes[0].set_title('残差 vs 预测值', fontsize=14)
        axes[0].grid(True, alpha=0.3)

        # 残差直方图
        axes[1].hist(residuals, bins=30, edgecolor='black', alpha=0.7)
        axes[1].set_xlabel('残差', fontsize=12)
        axes[1].set_ylabel('频数', fontsize=12)
        axes[1].set_title('残差分布直方图', fontsize=14)
        axes[1].grid(True, alpha=0.3)

        plt.tight_layout()
        return fig

    def plot_feature_importance(self, importance_dict, title="特征重要性"):
        """绘制特征重要性图"""
        features = list(importance_dict.keys())
        importance = list(importance_dict.values())

        # 排序
        indices = np.argsort(importance)[::-1]
        features = [features[i] for i in indices]
        importance = [importance[i] for i in indices]

        fig, ax = plt.subplots(figsize=(10, 6))

        bars = ax.bar(range(len(features)), importance, align='center', alpha=0.7)
        ax.set_xticks(range(len(features)))
        ax.set_xticklabels(features, rotation=45, ha='right')
        ax.set_xlabel('特征', fontsize=12)
        ax.set_ylabel('重要性', fontsize=12)
        ax.set_title(title, fontsize=14)
        ax.grid(True, alpha=0.3, axis='y')

        # 添加数值标签
        for bar, imp in zip(bars, importance):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{imp:.3f}', ha='center', va='bottom', fontsize=10)

        plt.tight_layout()
        return fig

    def plot_decision_tree(self, model, feature_names, title="决策树结构"):
        """绘制决策树结构图"""
        try:
            dot_data = export_graphviz(
                model,
                out_file=None,
                feature_names=feature_names,
                filled=True,
                rounded=True,
                special_characters=True
            )
            graph = graphviz.Source(dot_data)
            return graph
        except Exception as e:
            raise Exception(f"无法生成决策树图: {e}")

    def plot_metrics_comparison(self, metrics, title="模型评估指标"):
        """绘制评估指标对比图"""
        fig, ax = plt.subplots(figsize=(8, 6))

        names = list(metrics.keys())
        values = list(metrics.values())

        colors = plt.cm.Set2(np.linspace(0, 1, len(names)))
        bars = ax.bar(names, values, color=colors)
        ax.set_xlabel('指标', fontsize=12)
        ax.set_ylabel('数值', fontsize=12)
        ax.set_title(title, fontsize=14)
        ax.grid(True, alpha=0.3, axis='y')

        # 添加数值标签
        for bar, val in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{val:.4f}', ha='center', va='bottom', fontsize=10)

        plt.tight_layout()
        return fig
