# utils/data_loader.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import os

class DataLoader:
    def __init__(self):
        self.scaler = StandardScaler()
        self.feature_columns = None

    def load_builtin_dataset(self):
        """加载内置的Boston Housing数据集"""
        # 优先使用本地CSV文件
        local_csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'boston_housing.csv')
        if os.path.exists(local_csv_path):
            return pd.read_csv(local_csv_path)

        # 如果本地文件不存在，尝试从网络加载
        try:
            data_url = "http://lib.stat.cmu.edu/datasets/boston"
            raw_df = pd.read_csv(data_url, sep="\\s+", skiprows=22, header=None)
            data = np.hstack([raw_df.values[::2, :], raw_df.values[1::2, :2]])
            target = raw_df.values[1::2, 2]

            feature_names = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM',
                             'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT']
            df = pd.DataFrame(data, columns=feature_names)
            df['MEDV'] = target

            # 保存到本地以便下次使用
            os.makedirs(os.path.dirname(local_csv_path), exist_ok=True)
            df.to_csv(local_csv_path, index=False)

            return df
        except Exception as e:
            raise RuntimeError(f"无法加载Boston Housing数据集: {e}")

    def load_csv(self, file_path):
        """加载CSV文件"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")

        df = pd.read_csv(file_path)

        # 检查是否包含MEDV列
        if 'MEDV' not in df.columns:
            raise ValueError("CSV文件必须包含'MEDV'列作为目标变量")

        return df

    def preprocess_data(self, df):
        """数据预处理"""
        # 分离特征和目标变量
        X = df.drop('MEDV', axis=1)
        y = df['MEDV']

        # 保存特征列名
        self.feature_columns = X.columns.tolist()

        # 处理缺失值
        X = X.fillna(X.mean())

        # 标准化特征
        X_scaled = pd.DataFrame(
            self.scaler.fit_transform(X),
            columns=X.columns,
            index=X.index
        )

        return X_scaled, y

    def split_data(self, X, y, test_size=0.2, random_state=42):
        """划分训练集和测试集"""
        return train_test_split(X, y, test_size=test_size, random_state=random_state)

    def get_feature_names(self):
        """获取特征列名"""
        return self.feature_columns
