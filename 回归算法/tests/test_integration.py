# tests/test_integration.py
import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端，避免测试时弹出GUI窗口

import pytest
import pandas as pd
import numpy as np
from utils.data_loader import DataLoader
from utils.model import LinearRegressionModel, DecisionTreeModel, RandomForestModel
from utils.visualization import Visualizer


class TestIntegration:
    def setup_method(self):
        self.loader = DataLoader()
        self.visualizer = Visualizer()

    def test_full_pipeline_linear(self):
        """测试线性回归完整流程"""
        # 1. 加载数据
        df = self.loader.load_builtin_dataset()
        assert df is not None
        assert len(df) > 0

        # 2. 预处理
        X, y = self.loader.preprocess_data(df)
        X_train, X_test, y_train, y_test = self.loader.split_data(X, y)
        assert len(X_train) > 0
        assert len(X_test) > 0

        # 3. 训练模型
        model = LinearRegressionModel()
        model.create_model()
        model.train(X_train, y_train)
        assert model.is_trained

        # 4. 预测
        predictions = model.predict(X_test)
        assert len(predictions) == len(X_test)

        # 5. 评估
        metrics = model.evaluate(X_test, y_test)
        assert 'r2' in metrics
        assert metrics['r2'] > 0  # R²应该大于0

        # 6. 可视化
        fig = self.visualizer.plot_predictions(y_test.values, predictions)
        assert fig is not None

    def test_full_pipeline_decision_tree(self):
        """测试决策树回归完整流程"""
        # 1. 加载数据
        df = self.loader.load_builtin_dataset()
        assert df is not None
        assert len(df) > 0

        # 2. 预处理
        X, y = self.loader.preprocess_data(df)
        X_train, X_test, y_train, y_test = self.loader.split_data(X, y)

        # 3. 训练模型
        model = DecisionTreeModel()
        model.create_model(max_depth=5)
        model.train(X_train, y_train)
        assert model.is_trained

        # 4. 预测
        predictions = model.predict(X_test)
        assert len(predictions) == len(X_test)

        # 5. 评估
        metrics = model.evaluate(X_test, y_test)
        assert 'r2' in metrics
        assert metrics['r2'] > 0  # R²应该大于0

        # 6. 可视化
        fig = self.visualizer.plot_predictions(y_test.values, predictions)
        assert fig is not None

    def test_full_pipeline_random_forest(self):
        """测试随机森林回归完整流程"""
        # 1. 加载数据
        df = self.loader.load_builtin_dataset()
        assert df is not None
        assert len(df) > 0

        # 2. 预处理
        X, y = self.loader.preprocess_data(df)
        X_train, X_test, y_train, y_test = self.loader.split_data(X, y)

        # 3. 训练模型
        model = RandomForestModel()
        model.create_model(n_estimators=100)
        model.train(X_train, y_train)
        assert model.is_trained

        # 4. 预测
        predictions = model.predict(X_test)
        assert len(predictions) == len(X_test)

        # 5. 评估
        metrics = model.evaluate(X_test, y_test)
        assert 'r2' in metrics
        assert metrics['r2'] > 0  # R²应该大于0

        # 6. 可视化
        fig = self.visualizer.plot_predictions(y_test.values, predictions)
        assert fig is not None

    def test_algorithm_comparison(self):
        """测试三种算法对比"""
        # 1. 加载数据
        df = self.loader.load_builtin_dataset()
        X, y = self.loader.preprocess_data(df)
        X_train, X_test, y_train, y_test = self.loader.split_data(X, y)

        # 2. 训练三种模型
        models = {
            "线性回归": LinearRegressionModel(),
            "决策树回归": DecisionTreeModel(),
            "随机森林回归": RandomForestModel()
        }

        all_metrics = {}
        for name, model in models.items():
            model.create_model()
            model.train(X_train, y_train)
            metrics = model.evaluate(X_test, y_test)
            all_metrics[name] = metrics

        # 3. 验证所有模型都训练成功
        assert len(all_metrics) == 3

        # 4. 验证所有模型的R²都大于0
        for name, metrics in all_metrics.items():
            assert metrics['r2'] > 0, f"{name}的R²小于0"

    def test_data_consistency(self):
        """测试数据加载的一致性"""
        df1 = self.loader.load_builtin_dataset()
        df2 = self.loader.load_builtin_dataset()
        assert df1.equals(df2)

    def test_model_save_and_load(self, tmp_path):
        """测试模型保存和加载"""
        # 加载和预处理数据
        df = self.loader.load_builtin_dataset()
        X, y = self.loader.preprocess_data(df)
        X_train, X_test, y_train, y_test = self.loader.split_data(X, y)

        # 训练模型
        model = LinearRegressionModel()
        model.create_model()
        model.train(X_train, y_train)

        # 保存模型
        model_path = str(tmp_path / "test_model.pkl")
        model.save_model(model_path)

        # 加载模型
        loaded_model = LinearRegressionModel()
        loaded_model.load_model(model_path)
        assert loaded_model.is_trained

        # 验证预测结果一致
        original_pred = model.predict(X_test)
        loaded_pred = loaded_model.predict(X_test)
        np.testing.assert_array_almost_equal(original_pred, loaded_pred)
