# tests/test_data_loader.py
import pytest
import pandas as pd
import numpy as np
from utils.data_loader import DataLoader

class TestDataLoader:
    def setup_method(self):
        self.loader = DataLoader()

    def test_load_builtin_dataset(self):
        """测试加载内置数据集"""
        df = self.loader.load_builtin_dataset()
        assert isinstance(df, pd.DataFrame)
        assert df.shape[0] == 506
        assert df.shape[1] == 14
        assert 'MEDV' in df.columns

    def test_load_csv_file(self, tmp_path):
        """测试加载CSV文件"""
        # 创建测试CSV
        csv_path = tmp_path / "test.csv"
        test_data = pd.DataFrame({
            'CRIM': [0.1, 0.2],
            'ZN': [0, 10],
            'MEDV': [20, 30]
        })
        test_data.to_csv(csv_path, index=False)

        df = self.loader.load_csv(str(csv_path))
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2

    def test_preprocess_data(self):
        """测试数据预处理"""
        df = self.loader.load_builtin_dataset()
        X, y = self.loader.preprocess_data(df)

        assert isinstance(X, pd.DataFrame)
        assert isinstance(y, pd.Series)
        assert len(X) == len(y)
        assert 'MEDV' not in X.columns

    def test_split_data(self):
        """测试数据集划分"""
        df = self.loader.load_builtin_dataset()
        X, y = self.loader.preprocess_data(df)
        X_train, X_test, y_train, y_test = self.loader.split_data(X, y)

        assert len(X_train) + len(X_test) == len(X)
        assert len(y_train) + len(y_test) == len(y)
        assert len(X_train) > len(X_test)
