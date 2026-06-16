# app.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import sys

# 添加Graphviz到PATH
graphviz_path = r"C:\Program Files\Graphviz\bin"
if os.path.exists(graphviz_path):
    os.environ["PATH"] = graphviz_path + ";" + os.environ.get("PATH", "")

from utils.data_loader import DataLoader
from utils.model import LinearRegressionModel, DecisionTreeModel, RandomForestModel
from utils.visualization import Visualizer

class BostonHousingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("波士顿房价预测系统")
        self.root.geometry("1200x800")

        # 初始化组件
        self.data_loader = DataLoader()
        self.linear_model = LinearRegressionModel()
        self.decision_tree_model = DecisionTreeModel()
        self.random_forest_model = RandomForestModel()
        self.visualizer = Visualizer()

        # 当前选中的模型
        self.current_model = None
        self.current_model_name = None

        # 数据存储
        self.df = None
        self.current_figure = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.feature_names = None

        # 创建界面
        self.create_widgets()

        # 默认加载内置数据集
        self.load_builtin_dataset()

    def create_widgets(self):
        """创建主界面"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # 左侧控制面板
        control_frame = ttk.LabelFrame(main_frame, text="控制面板", padding="10")
        control_frame.grid(row=0, column=0, rowspan=2, sticky=(tk.N, tk.S), padx=(0, 10))

        # 数据管理区域
        data_frame = ttk.LabelFrame(control_frame, text="数据管理", padding="5")
        data_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(data_frame, text="加载内置数据集",
                  command=self.load_builtin_dataset).pack(fill=tk.X, pady=2)
        ttk.Button(data_frame, text="上传CSV文件",
                  command=self.upload_csv).pack(fill=tk.X, pady=2)

        self.data_info_label = ttk.Label(data_frame, text="未加载数据")
        self.data_info_label.pack(fill=tk.X, pady=5)

        # 算法选择区域
        algo_frame = ttk.LabelFrame(control_frame, text="算法选择", padding="5")
        algo_frame.pack(fill=tk.X, pady=(0, 10))

        self.algorithm_var = tk.StringVar(value="linear")
        ttk.Radiobutton(algo_frame, text="线性回归", variable=self.algorithm_var,
                       value="linear", command=self.on_algorithm_change).pack(anchor=tk.W)
        ttk.Radiobutton(algo_frame, text="决策树回归", variable=self.algorithm_var,
                       value="decision_tree", command=self.on_algorithm_change).pack(anchor=tk.W)
        ttk.Radiobutton(algo_frame, text="随机森林回归", variable=self.algorithm_var,
                       value="random_forest", command=self.on_algorithm_change).pack(anchor=tk.W)

        # 模型参数区域
        param_frame = ttk.LabelFrame(control_frame, text="模型参数", padding="5")
        param_frame.pack(fill=tk.X, pady=(0, 10))

        # 决策树参数
        self.dt_param_frame = ttk.Frame(param_frame)
        self.dt_param_frame.pack(fill=tk.X)

        ttk.Label(self.dt_param_frame, text="最大深度:").pack(anchor=tk.W)
        self.max_depth_var = tk.StringVar(value="5")
        ttk.Entry(self.dt_param_frame, textvariable=self.max_depth_var).pack(fill=tk.X)

        ttk.Label(self.dt_param_frame, text="最小样本分裂数:").pack(anchor=tk.W)
        self.min_samples_split_var = tk.StringVar(value="2")
        ttk.Entry(self.dt_param_frame, textvariable=self.min_samples_split_var).pack(fill=tk.X)

        # 随机森林参数
        self.rf_param_frame = ttk.Frame(param_frame)
        self.rf_param_frame.pack(fill=tk.X)

        ttk.Label(self.rf_param_frame, text="树的数量:").pack(anchor=tk.W)
        self.n_estimators_var = tk.StringVar(value="100")
        ttk.Entry(self.rf_param_frame, textvariable=self.n_estimators_var).pack(fill=tk.X)

        # 操作按钮
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(button_frame, text="训练模型",
                  command=self.train_model).pack(fill=tk.X, pady=2)
        ttk.Button(button_frame, text="保存模型",
                  command=self.save_model).pack(fill=tk.X, pady=2)
        ttk.Button(button_frame, text="加载模型",
                  command=self.load_model).pack(fill=tk.X, pady=2)

        # 预测区域
        predict_frame = ttk.LabelFrame(control_frame, text="单条预测", padding="5")
        predict_frame.pack(fill=tk.X, pady=(0, 10))

        self.predict_entries = {}
        for feature in ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM',
                       'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT']:
            ttk.Label(predict_frame, text=f"{feature}:").pack(anchor=tk.W)
            entry = ttk.Entry(predict_frame)
            entry.pack(fill=tk.X)
            self.predict_entries[feature] = entry

        ttk.Button(predict_frame, text="预测房价",
                  command=self.predict_single).pack(fill=tk.X, pady=5)

        self.prediction_label = ttk.Label(predict_frame, text="预测结果: -")
        self.prediction_label.pack(fill=tk.X)

        # 右侧显示区域
        display_frame = ttk.Frame(main_frame)
        display_frame.grid(row=0, column=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        display_frame.columnconfigure(0, weight=1)
        display_frame.rowconfigure(1, weight=1)

        # 数据预览区域
        preview_frame = ttk.LabelFrame(display_frame, text="数据预览", padding="5")
        preview_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        # 创建Treeview用于显示数据
        self.tree = ttk.Treeview(preview_frame, show='headings', height=10)
        self.tree_scroll = ttk.Scrollbar(preview_frame, orient=tk.VERTICAL,
                                        command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.tree_scroll.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # 可视化区域
        viz_frame = ttk.LabelFrame(display_frame, text="可视化", padding="5")
        viz_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 可视化选项
        viz_button_frame = ttk.Frame(viz_frame)
        viz_button_frame.pack(fill=tk.X, pady=(0, 5))

        ttk.Button(viz_button_frame, text="预测对比图",
                  command=self.show_predictions_plot).pack(side=tk.LEFT, padx=2)
        ttk.Button(viz_button_frame, text="残差分布图",
                  command=self.show_residuals_plot).pack(side=tk.LEFT, padx=2)
        ttk.Button(viz_button_frame, text="特征重要性图",
                  command=self.show_feature_importance).pack(side=tk.LEFT, padx=2)
        ttk.Button(viz_button_frame, text="决策树结构",
                  command=self.show_decision_tree).pack(side=tk.LEFT, padx=2)
        ttk.Button(viz_button_frame, text="评估指标图",
                  command=self.show_metrics_plot).pack(side=tk.LEFT, padx=2)
        ttk.Button(viz_button_frame, text="算法对比",
                  command=self.show_algorithm_comparison).pack(side=tk.LEFT, padx=2)

        # 图表显示区域
        self.chart_frame = ttk.Frame(viz_frame)
        self.chart_frame.pack(fill=tk.BOTH, expand=True)

        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var,
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))

    def on_algorithm_change(self):
        """算法选择改变时的回调"""
        algo = self.algorithm_var.get()

        # 隐藏所有参数框架
        self.dt_param_frame.pack_forget()
        self.rf_param_frame.pack_forget()

        # 根据选择显示对应参数
        if algo == "linear":
            pass  # 线性回归没有额外参数
        elif algo == "decision_tree":
            self.dt_param_frame.pack(fill=tk.X)
        elif algo == "random_forest":
            self.rf_param_frame.pack(fill=tk.X)

    def load_builtin_dataset(self):
        """加载内置数据集"""
        try:
            self.df = self.data_loader.load_builtin_dataset()
            self.update_data_display()
            self.status_var.set("已加载内置Boston Housing数据集")
        except Exception as e:
            messagebox.showerror("错误", f"加载数据失败: {str(e)}")

    def upload_csv(self):
        """上传CSV文件"""
        file_path = filedialog.askopenfilename(
            title="选择CSV文件",
            filetypes=[("CSV文件", "*.csv"), ("所有文件", "*.*")]
        )

        if file_path:
            try:
                self.df = self.data_loader.load_csv(file_path)
                self.update_data_display()
                self.status_var.set(f"已加载文件: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("错误", f"加载文件失败: {str(e)}")

    def update_data_display(self):
        """更新数据预览显示"""
        if self.df is None:
            return

        # 清空Treeview
        self.tree.delete(*self.tree.get_children())

        # 设置列
        self.tree["columns"] = list(self.df.columns)
        for col in self.df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=80, anchor=tk.CENTER)

        # 插入数据（最多显示100行）
        for idx, row in self.df.head(100).iterrows():
            self.tree.insert("", tk.END, values=list(row))

        # 更新数据信息
        self.data_info_label.config(
            text=f"样本数: {self.df.shape[0]}, 特征数: {self.df.shape[1]-1}"
        )

        # 预处理数据
        self.X, self.y = self.data_loader.preprocess_data(self.df)
        self.X_train, self.X_test, self.y_train, self.y_test = \
            self.data_loader.split_data(self.X, self.y)
        self.feature_names = self.data_loader.get_feature_names()

    def get_current_model(self):
        """获取当前选中的模型"""
        algo = self.algorithm_var.get()
        if algo == "linear":
            return self.linear_model, "线性回归"
        elif algo == "decision_tree":
            return self.decision_tree_model, "决策树回归"
        elif algo == "random_forest":
            return self.random_forest_model, "随机森林回归"
        return None, None

    def train_model(self):
        """训练模型"""
        if self.df is None:
            messagebox.showwarning("警告", "请先加载数据")
            return

        try:
            # 获取当前模型
            model, model_name = self.get_current_model()
            if model is None:
                messagebox.showwarning("警告", "请选择算法")
                return

            # 获取参数
            algo = self.algorithm_var.get()
            if algo == "linear":
                model.create_model()
            elif algo == "decision_tree":
                max_depth = int(self.max_depth_var.get()) if self.max_depth_var.get() else None
                min_samples_split = int(self.min_samples_split_var.get())
                model.create_model(
                    max_depth=max_depth,
                    min_samples_split=min_samples_split
                )
            elif algo == "random_forest":
                n_estimators = int(self.n_estimators_var.get())
                model.create_model(n_estimators=n_estimators)

            # 训练模型
            model.train(self.X_train, self.y_train)

            # 评估模型
            metrics = model.evaluate(self.X_test, self.y_test)

            # 显示结果
            result_msg = (
                f"{model_name}训练完成!\n\n"
                f"评估指标:\n"
                f"MAE: {metrics['mae']:.4f}\n"
                f"MSE: {metrics['mse']:.4f}\n"
                f"RMSE: {metrics['rmse']:.4f}\n"
                f"R²: {metrics['r2']:.4f}"
            )
            messagebox.showinfo("训练完成", result_msg)
            self.status_var.set(f"{model_name}训练完成")

        except Exception as e:
            messagebox.showerror("错误", f"训练失败: {str(e)}")

    def save_model(self):
        """保存模型"""
        model, model_name = self.get_current_model()
        if model is None or not model.is_trained:
            messagebox.showwarning("警告", "请先训练模型")
            return

        file_path = filedialog.asksaveasfilename(
            title="保存模型",
            defaultextension=".pkl",
            filetypes=[("Pickle文件", "*.pkl"), ("所有文件", "*.*")]
        )

        if file_path:
            try:
                model.save_model(file_path)
                self.status_var.set(f"{model_name}已保存: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败: {str(e)}")

    def load_model(self):
        """加载模型"""
        model, model_name = self.get_current_model()
        if model is None:
            messagebox.showwarning("警告", "请选择算法")
            return

        file_path = filedialog.askopenfilename(
            title="加载模型",
            filetypes=[("Pickle文件", "*.pkl"), ("所有文件", "*.*")]
        )

        if file_path:
            try:
                model.load_model(file_path)
                self.status_var.set(f"{model_name}已加载: {os.path.basename(file_path)}")
                # 警告用户
                messagebox.showwarning("注意",
                    "模型已加载。单条预测功能可能无法使用，\n"
                    "因为特征缩放器未保存。请先训练模型以使用完整功能。")
            except Exception as e:
                messagebox.showerror("错误", f"加载失败: {str(e)}")

    def predict_single(self):
        """单条预测"""
        model, model_name = self.get_current_model()
        if model is None or not model.is_trained:
            messagebox.showwarning("警告", "请先训练模型")
            return

        try:
            # 获取输入值
            input_data = {}
            for feature, entry in self.predict_entries.items():
                value = entry.get()
                if not value:
                    messagebox.showwarning("警告", f"请输入{feature}的值")
                    return
                input_data[feature] = float(value)

            # 转换为DataFrame
            input_df = pd.DataFrame([input_data])

            # 标准化
            input_scaled = pd.DataFrame(
                self.data_loader.scaler.transform(input_df),
                columns=input_df.columns
            )

            # 预测
            prediction = model.predict(input_scaled)[0]

            # 显示结果
            self.prediction_label.config(
                text=f"预测结果: ${prediction*1000:,.2f}"
            )
            self.status_var.set(f"预测房价: ${prediction*1000:,.2f}")

        except ValueError as e:
            messagebox.showerror("错误", f"请输入有效的数值: {str(e)}")
        except Exception as e:
            messagebox.showerror("错误", f"预测失败: {str(e)}")

    def show_predictions_plot(self):
        """显示预测对比图"""
        model, model_name = self.get_current_model()
        if model is None or not model.is_trained:
            messagebox.showwarning("警告", "请先训练模型")
            return

        predictions = model.predict(self.X_test)
        fig = self.visualizer.plot_predictions(
            self.y_test.values, predictions,
            title=f"{model_name} - 预测值 vs 真实值"
        )
        self.display_figure(fig)

    def show_residuals_plot(self):
        """显示残差分布图"""
        model, model_name = self.get_current_model()
        if model is None or not model.is_trained:
            messagebox.showwarning("警告", "请先训练模型")
            return

        predictions = model.predict(self.X_test)
        fig = self.visualizer.plot_residuals(
            self.y_test.values, predictions,
            title=f"{model_name} - 残差分布"
        )
        self.display_figure(fig)

    def show_feature_importance(self):
        """显示特征重要性图"""
        model, model_name = self.get_current_model()
        if model is None or not model.is_trained:
            messagebox.showwarning("警告", "请先训练模型")
            return

        if not hasattr(model, 'get_feature_importance'):
            messagebox.showwarning("警告", "当前算法不支持特征重要性")
            return

        importance = model.get_feature_importance(self.feature_names)
        fig = self.visualizer.plot_feature_importance(
            importance, title=f"{model_name} - 特征重要性"
        )
        self.display_figure(fig)

    def show_decision_tree(self):
        """显示决策树结构"""
        if self.algorithm_var.get() != "decision_tree":
            messagebox.showwarning("警告", "请选择决策树算法")
            return

        if not self.decision_tree_model.is_trained:
            messagebox.showwarning("警告", "请先训练模型")
            return

        try:
            graph = self.visualizer.plot_decision_tree(
                self.decision_tree_model.model, self.feature_names,
                title="决策树结构"
            )
            if graph:
                # 保存并打开决策树图
                graph.render("decision_tree", format="png", cleanup=True)
                messagebox.showinfo("信息", "决策树已保存为 decision_tree.png")
        except Exception as e:
            messagebox.showwarning("警告",
                "无法生成决策树图。\n\n"
                "请确保已安装Graphviz：\n"
                "1. 下载: https://graphviz.org/download/\n"
                "2. 安装后将bin目录添加到系统PATH\n"
                "3. 重启应用")

    def show_metrics_plot(self):
        """显示评估指标图"""
        model, model_name = self.get_current_model()
        if model is None or not model.is_trained:
            messagebox.showwarning("警告", "请先训练模型")
            return

        metrics = model.evaluate(self.X_test, self.y_test)
        fig = self.visualizer.plot_metrics_comparison(
            metrics, title=f"{model_name} - 评估指标"
        )
        self.display_figure(fig)

    def show_algorithm_comparison(self):
        """显示算法对比"""
        if self.df is None:
            messagebox.showwarning("警告", "请先加载数据")
            return

        # 训练所有模型并收集指标
        models = {
            "线性回归": self.linear_model,
            "决策树回归": self.decision_tree_model,
            "随机森林回归": self.random_forest_model
        }

        all_metrics = {}
        for name, model in models.items():
            if model.is_trained:
                metrics = model.evaluate(self.X_test, self.y_test)
                all_metrics[name] = metrics

        if not all_metrics:
            messagebox.showwarning("警告", "请先训练至少一个模型")
            return

        # 创建对比图 - 使用表格样式的布局
        fig, ax = plt.subplots(figsize=(12, 6))

        # 准备数据
        metric_names = ['MAE', 'MSE', 'RMSE', 'R2']
        metric_keys = ['mae', 'mse', 'rmse', 'r2']
        algo_names = list(all_metrics.keys())

        # 设置柱状图位置
        x = np.arange(len(metric_names))
        width = 0.25  # 柱子宽度
        colors = ['#2196F3', '#FF9800', '#4CAF50']

        # 绘制每种算法的柱子
        for i, (algo, color) in enumerate(zip(algo_names, colors)):
            values = [all_metrics[algo][key] for key in metric_keys]
            offset = (i - len(algo_names)/2 + 0.5) * width
            bars = ax.bar(x + offset, values, width, label=algo, color=color, alpha=0.85)

            # 添加数值标签
            for bar, val in zip(bars, values):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{val:.3f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

        # 设置图表
        ax.set_xlabel('评估指标', fontsize=12)
        ax.set_ylabel('数值', fontsize=12)
        ax.set_title('三种算法性能对比', fontsize=14, fontweight='bold', pad=15)
        ax.set_xticks(x)
        ax.set_xticklabels(metric_names, fontsize=11)
        ax.legend(fontsize=10, loc='upper left')
        ax.grid(True, alpha=0.3, axis='y')

        # 设置y轴从0开始
        ax.set_ylim(bottom=0)

        plt.tight_layout()

        self.display_figure(fig)

    def display_figure(self, fig):
        """在GUI中显示图表"""
        # 关闭之前的图表
        if hasattr(self, 'current_figure') and self.current_figure is not None:
            plt.close(self.current_figure)

        # 清空图表区域
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        # 创建matplotlib画布
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # 保存当前图表引用
        self.current_figure = fig

def main():
    root = tk.Tk()
    app = BostonHousingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
