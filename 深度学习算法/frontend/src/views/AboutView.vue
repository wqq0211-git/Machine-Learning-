<template>
  <div class="page">
    <h2 class="section-title">项目说明</h2>
    <div class="panel">
      <h3>实验目的</h3>
      <p>实现并比较自定义 CNN 与 ResNet-18 在 CIFAR-10 十分类任务上的训练、评估与推理表现。</p>
      <h3>CNN 与 ResNet-18</h3>
      <p>CNN 通过卷积、归一化、激活和池化提取局部图像特征。ResNet-18 使用残差连接，形式为 H(x)=F(x)+x，可缓解深层网络训练退化问题。</p>
      <h3>迁移学习</h3>
      <p>ResNet-18 可加载 ImageNet 预训练权重，并替换最后一层分类器以适配 CIFAR-10 的 10 个类别。</p>
      <h3>系统架构</h3>
      <p>前端使用 Vue 3、Element Plus、ECharts；后端使用 FastAPI 提供统一 /api 接口；模型训练与推理使用 PyTorch。</p>
      <h3>启动方法</h3>
      <p>后端进入 backend 后运行 uvicorn main:app --host 127.0.0.1 --port 8000 --reload；前端进入 frontend 后运行 npm run dev。</p>
    </div>
  </div>
</template>

