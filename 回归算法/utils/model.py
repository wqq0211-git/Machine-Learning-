# utils/model.py
import numpy as np
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

class LinearRegressionModel:
    def __init__(self):
        self.model = None
        self.is_trained = False

    def create_model(self, fit_intercept=True, copy_X=True, n_jobs=None):
        """创建线性回归模型"""
        self.model = LinearRegression(
            fit_intercept=fit_intercept,
            copy_X=copy_X,
            n_jobs=n_jobs
        )
        return self.model

    def train(self, X_train, y_train):
        """训练模型"""
        if self.model is None:
            raise ValueError("请先创建模型")

        self.model.fit(X_train, y_train)
        self.is_trained = True

    def predict(self, X):
        """预测"""
        if not self.is_trained:
            raise ValueError("请先训练模型")

        return self.model.predict(X)

    def evaluate(self, X_test, y_test):
        """评估模型"""
        predictions = self.predict(X_test)

        mae = mean_absolute_error(y_test, predictions)
        mse = mean_squared_error(y_test, predictions)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, predictions)

        return {
            'mae': mae,
            'mse': mse,
            'rmse': rmse,
            'r2': r2
        }

    def save_model(self, file_path):
        """保存模型"""
        if not self.is_trained:
            raise ValueError("请先训练模型")

        with open(file_path, 'wb') as f:
            pickle.dump(self.model, f)

    def load_model(self, file_path):
        """加载模型"""
        with open(file_path, 'rb') as f:
            self.model = pickle.load(f)
        self.is_trained = True

    def get_params(self):
        """获取模型参数"""
        if self.model is None:
            return {}
        return self.model.get_params()

class DecisionTreeModel:
    def __init__(self):
        self.model = None
        self.is_trained = False

    def create_model(self, max_depth=None, min_samples_split=2,
                     min_samples_leaf=1, max_features=None):
        """创建决策树回归模型"""
        self.model = DecisionTreeRegressor(
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            min_samples_leaf=min_samples_leaf,
            max_features=max_features,
            random_state=42
        )
        return self.model

    def train(self, X_train, y_train):
        """训练模型"""
        if self.model is None:
            raise ValueError("请先创建模型")

        self.model.fit(X_train, y_train)
        self.is_trained = True

    def predict(self, X):
        """预测"""
        if not self.is_trained:
            raise ValueError("请先训练模型")

        return self.model.predict(X)

    def evaluate(self, X_test, y_test):
        """评估模型"""
        predictions = self.predict(X_test)

        mae = mean_absolute_error(y_test, predictions)
        mse = mean_squared_error(y_test, predictions)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, predictions)

        return {
            'mae': mae,
            'mse': mse,
            'rmse': rmse,
            'r2': r2
        }

    def save_model(self, file_path):
        """保存模型"""
        if not self.is_trained:
            raise ValueError("请先训练模型")

        with open(file_path, 'wb') as f:
            pickle.dump(self.model, f)

    def load_model(self, file_path):
        """加载模型"""
        with open(file_path, 'rb') as f:
            self.model = pickle.load(f)
        self.is_trained = True

    def get_feature_importance(self, feature_names):
        """获取特征重要性"""
        if not self.is_trained:
            raise ValueError("请先训练模型")

        importance = self.model.feature_importances_
        return dict(zip(feature_names, importance))

    def get_params(self):
        """获取模型参数"""
        if self.model is None:
            return {}
        return self.model.get_params()

class RandomForestModel:
    def __init__(self):
        self.model = None
        self.is_trained = False

    def create_model(self, n_estimators=100, max_depth=None,
                     min_samples_split=2, min_samples_leaf=1,
                     max_features='sqrt', n_jobs=None):
        """创建随机森林回归模型"""
        self.model = RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            min_samples_leaf=min_samples_leaf,
            max_features=max_features,
            n_jobs=n_jobs,
            random_state=42
        )
        return self.model

    def train(self, X_train, y_train):
        """训练模型"""
        if self.model is None:
            raise ValueError("请先创建模型")

        self.model.fit(X_train, y_train)
        self.is_trained = True

    def predict(self, X):
        """预测"""
        if not self.is_trained:
            raise ValueError("请先训练模型")

        return self.model.predict(X)

    def evaluate(self, X_test, y_test):
        """评估模型"""
        predictions = self.predict(X_test)

        mae = mean_absolute_error(y_test, predictions)
        mse = mean_squared_error(y_test, predictions)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, predictions)

        return {
            'mae': mae,
            'mse': mse,
            'rmse': rmse,
            'r2': r2
        }

    def save_model(self, file_path):
        """保存模型"""
        if not self.is_trained:
            raise ValueError("请先训练模型")

        with open(file_path, 'wb') as f:
            pickle.dump(self.model, f)

    def load_model(self, file_path):
        """加载模型"""
        with open(file_path, 'rb') as f:
            self.model = pickle.load(f)
        self.is_trained = True

    def get_feature_importance(self, feature_names):
        """获取特征重要性"""
        if not self.is_trained:
            raise ValueError("请先训练模型")

        importance = self.model.feature_importances_
        return dict(zip(feature_names, importance))

    def get_params(self):
        """获取模型参数"""
        if self.model is None:
            return {}
        return self.model.get_params()
