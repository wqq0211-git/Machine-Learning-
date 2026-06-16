import pytest
import matplotlib.pyplot as plt
from utils.visualization import Visualizer


class TestVisualizer:
    def setup_method(self):
        self.viz = Visualizer()
        plt.switch_backend('Agg')  # 使用非交互后端

    def test_plot_predictions(self):
        """测试预测对比图"""
        y_true = [1, 2, 3, 4, 5]
        y_pred = [1.1, 2.2, 2.8, 4.1, 5.2]

        fig = self.viz.plot_predictions(y_true, y_pred)
        assert fig is not None
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_plot_residuals(self):
        """测试残差分布图"""
        y_true = [1, 2, 3, 4, 5]
        y_pred = [1.1, 2.2, 2.8, 4.1, 5.2]

        fig = self.viz.plot_residuals(y_true, y_pred)
        assert fig is not None
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_plot_feature_importance(self):
        """测试特征重要性图"""
        importance = {'feature1': 0.3, 'feature2': 0.5, 'feature3': 0.2}

        fig = self.viz.plot_feature_importance(importance)
        assert fig is not None
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_plot_decision_tree(self):
        """测试决策树结构图"""
        # 这个测试需要实际的模型，这里只测试函数存在
        assert hasattr(self.viz, 'plot_decision_tree')
