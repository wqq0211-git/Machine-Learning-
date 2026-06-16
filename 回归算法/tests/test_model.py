# tests/test_model.py
import pytest
import pandas as pd
import numpy as np
from utils.data_loader import DataLoader
from utils.model import LinearRegressionModel, DecisionTreeModel, RandomForestModel

class TestLinearRegressionModel:
    def setup_method(self):
        self.loader = DataLoader()
        self.model = LinearRegressionModel()

        # 加载测试数据
        df = self.loader.load_builtin_dataset()
        self.X, self.y = self.loader.preprocess_data(df)
        self.X_train, self.X_test, self.y_train, self.y_test = \
            self.loader.split_data(self.X, self.y)

    def test_create_model(self):
        """测试创建模型"""
        model = self.model.create_model()
        assert model is not None
        assert hasattr(model, 'fit')
        assert hasattr(model, 'predict')

    def test_train_model(self):
        """测试训练模型"""
        self.model.create_model()
        self.model.train(self.X_train, self.y_train)

        assert self.model.is_trained

    def test_predict(self):
        """测试预测"""
        self.model.create_model()
        self.model.train(self.X_train, self.y_train)

        predictions = self.model.predict(self.X_test)
        assert isinstance(predictions, np.ndarray)
        assert len(predictions) == len(self.X_test)

    def test_evaluate(self):
        """测试评估"""
        self.model.create_model()
        self.model.train(self.X_train, self.y_train)

        metrics = self.model.evaluate(self.X_test, self.y_test)
        assert 'mae' in metrics
        assert 'mse' in metrics
        assert 'rmse' in metrics
        assert 'r2' in metrics
        assert all(isinstance(v, (int, float)) for v in metrics.values())

    def test_save_and_load_model(self, tmp_path):
        """测试模型保存和加载"""
        self.model.create_model()
        self.model.train(self.X_train, self.y_train)

        model_path = tmp_path / "test_linear.pkl"
        self.model.save_model(str(model_path))

        new_model = LinearRegressionModel()
        new_model.load_model(str(model_path))

        assert new_model.is_trained
        predictions = new_model.predict(self.X_test)
        assert len(predictions) == len(self.X_test)

class TestDecisionTreeModel:
    def setup_method(self):
        self.loader = DataLoader()
        self.model = DecisionTreeModel()

        # 加载测试数据
        df = self.loader.load_builtin_dataset()
        self.X, self.y = self.loader.preprocess_data(df)
        self.X_train, self.X_test, self.y_train, self.y_test = \
            self.loader.split_data(self.X, self.y)

    def test_create_model(self):
        """测试创建模型"""
        model = self.model.create_model()
        assert model is not None
        assert hasattr(model, 'fit')
        assert hasattr(model, 'predict')

    def test_train_model(self):
        """测试训练模型"""
        self.model.create_model()
        self.model.train(self.X_train, self.y_train)

        assert self.model.is_trained

    def test_predict(self):
        """测试预测"""
        self.model.create_model()
        self.model.train(self.X_train, self.y_train)

        predictions = self.model.predict(self.X_test)
        assert isinstance(predictions, np.ndarray)
        assert len(predictions) == len(self.X_test)

    def test_evaluate(self):
        """测试评估"""
        self.model.create_model()
        self.model.train(self.X_train, self.y_train)

        metrics = self.model.evaluate(self.X_test, self.y_test)
        assert 'mae' in metrics
        assert 'mse' in metrics
        assert 'rmse' in metrics
        assert 'r2' in metrics
        assert all(isinstance(v, (int, float)) for v in metrics.values())

    def test_save_and_load_model(self, tmp_path):
        """测试模型保存和加载"""
        self.model.create_model()
        self.model.train(self.X_train, self.y_train)

        model_path = tmp_path / "test_decision_tree.pkl"
        self.model.save_model(str(model_path))

        new_model = DecisionTreeModel()
        new_model.load_model(str(model_path))

        assert new_model.is_trained
        predictions = new_model.predict(self.X_test)
        assert len(predictions) == len(self.X_test)

class TestRandomForestModel:
    def setup_method(self):
        self.loader = DataLoader()
        self.model = RandomForestModel()

        # 加载测试数据
        df = self.loader.load_builtin_dataset()
        self.X, self.y = self.loader.preprocess_data(df)
        self.X_train, self.X_test, self.y_train, self.y_test = \
            self.loader.split_data(self.X, self.y)

    def test_create_model(self):
        """测试创建模型"""
        model = self.model.create_model()
        assert model is not None
        assert hasattr(model, 'fit')
        assert hasattr(model, 'predict')

    def test_train_model(self):
        """测试训练模型"""
        self.model.create_model()
        self.model.train(self.X_train, self.y_train)

        assert self.model.is_trained

    def test_predict(self):
        """测试预测"""
        self.model.create_model()
        self.model.train(self.X_train, self.y_train)

        predictions = self.model.predict(self.X_test)
        assert isinstance(predictions, np.ndarray)
        assert len(predictions) == len(self.X_test)

    def test_evaluate(self):
        """测试评估"""
        self.model.create_model()
        self.model.train(self.X_train, self.y_train)

        metrics = self.model.evaluate(self.X_test, self.y_test)
        assert 'mae' in metrics
        assert 'mse' in metrics
        assert 'rmse' in metrics
        assert 'r2' in metrics
        assert all(isinstance(v, (int, float)) for v in metrics.values())

    def test_save_and_load_model(self, tmp_path):
        """测试模型保存和加载"""
        self.model.create_model()
        self.model.train(self.X_train, self.y_train)

        model_path = tmp_path / "test_random_forest.pkl"
        self.model.save_model(str(model_path))

        new_model = RandomForestModel()
        new_model.load_model(str(model_path))

        assert new_model.is_trained
        predictions = new_model.predict(self.X_test)
        assert len(predictions) == len(self.X_test)

    def test_feature_importance(self):
        """测试特征重要性"""
        self.model.create_model()
        self.model.train(self.X_train, self.y_train)

        importance = self.model.get_feature_importance(self.X_train.columns.tolist())
        assert isinstance(importance, dict)
        assert len(importance) == len(self.X_train.columns)
