# 🐱 YOLO屏幕监控应用 喵~

基于YOLO26的实时电脑屏幕内容识别和标记工具 喵~ 使用面向对象设计，采用SOLID原则，支持高性能实时检测 😺

## 功能特性 🐾

- 🎯 **实时检测**：使用YOLO26模型实时识别屏幕上的80类COCO物体 喵~
- 🖥️ **屏幕捕获**：支持全屏或自定义区域捕获 😺
- ⚡ **高性能**：FPS限制功能防止CPU占用过高 喵喵~
- 🎨 **可视化标记**：实时绘制检测框、类别名称和置信度 😸
- ⚙️ **灵活配置**：支持多种YOLO模型和自定义检测参数 喵~
- 🎮 **交互控制**：支持暂停/继续和快捷键操作 🐱
- 📝 **喵日志**：可爱的喵风格日志输出 喵喵喵~

## 项目结构 🐾

```
.
├── main.py                   # 🚀 应用入口 喵~
├── requirements.txt          # 📦 依赖列表 喵~
├── README.md                 # 📖 项目文档 喵~
├── .gitignore                # 🙈 Git忽略配置 喵~
└── src/                      # 📂 源代码包 喵~
    ├── __init__.py
    ├── config.py             # ⚙️ 配置管理 喵~
    ├── logger.py             # 🐱 喵日志模块 喵喵~
    ├── screen_capture.py     # 📹 屏幕捕获模块 (ScreenCapture类) 喵~
    ├── yolo_detector.py      # 🎯 YOLO检测模块 (YOLODetector类) 喵~
    └── screen_monitor_app.py # 🖥️ 主应用模块 (ScreenMonitorApp类) 喵~
```

## 架构设计 🐾

### 类结构 喵~

```
┌─────────────────────────────────────────┐
│       ScreenMonitorApp                   │
│  （主应用 - 协调各组件）喵~                 │
├─────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────────┐ │
│  │ScreenCapture│    │  YOLODetector   │ │
│  │（屏幕捕获）喵 │    │  （目标检测）喵~   │ │
│  └─────────────┘    └─────────────────┘ │
└─────────────────────────────────────────┘
```

### 设计原则 😺

| 原则 | 应用说明 喵~ |
|------|----------|
| **S (单一职责)** | ScreenCapture负责捕获，YOLODetector负责检测，App负责协调 喵~ |
| **O (开闭原则)** | 可扩展新的检测器而无需修改现有代码 喵喵~ |
| **D (依赖倒置)** | App依赖抽象接口而非具体实现 喵~ |

## 安装 🐾

### 1. 克隆项目 喵~

```bash
git clone <项目地址>
cd kb
```

### 2. 创建虚拟环境（推荐）喵~

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. 安装依赖 喵喵~

```bash
pip install -r requirements.txt
```

### 4. 下载YOLO模型 喵~

首次运行时，程序会自动下载 `yolo26n.pt` 模型 喵~ 你也可以手动下载：

```bash
python -c "from ultralytics import YOLO; YOLO('yolo26n.pt')"
```

## 使用方法 🐾

### 基本使用 喵~

```bash
python main.py
```

### 快捷键 😺

| 按键 | 功能 喵~ |
|------|------|
| `q` | 退出程序 喵~ |
| `s` | 暂停/继续监控 喵喵~ |

### 日志输出示例 喵~

```
14:30:25 😺 喵~ ============================================================
14:30:25 😺 喵~ 🚀 YOLO屏幕监控应用启动
14:30:25 😺 喵~ ============================================================
14:30:25 😺 喵~ 正在加载YOLO模型: yolo26n.pt
14:30:26 😺 喵~ 屏幕捕获初始化: 区域大小 1920x1080
14:30:26 😺 喵~ YOLO检测器初始化完成
14:30:26 😺 喵~   - 置信度阈值: 0.5
14:30:26 😺 喵~   - IOU阈值: 0.45
14:30:26 😺 喵~   - 检测范围: 类别: [0]
14:30:26 😺 喵~ ==================================================
14:30:26 😺 喵~ 屏幕监控应用初始化
14:30:26 😺 喵~   - FPS限制: 30
14:30:26 😺 喵~   - 显示窗口: 1280x720
14:30:26 😺 喵~ ==================================================
14:30:26 😺 喵~ 应用实例创建完成
14:30:26 😺 喵~ 屏幕监控启动...
14:30:27 😺 喵~ 📊 运行统计 - FPS: 28.5 | 检测到: 2 个物体 | 总帧数: 150
```

## 配置说明 🐾

编辑 `src/config.py` 或创建自定义配置 喵~

```python
from src.config import AppConfig

config = AppConfig()

# 检测器配置 喵~
config.detector.model_path = "yolo26s.pt"  # 模型选择 喵~
config.detector.confidence_threshold = 0.7  # 置信度阈值 喵~
config.detector.classes = [0]  # 只检测人（默认已设置）喵~

# 屏幕配置 喵~
config.screen.display_size = (1920, 1080)  # 显示窗口大小 喵~
config.screen.fps_limit = 60  # FPS限制 喵~

app = create_app_from_config(config)
app.run()
```

### 模型选择 喵~

| 模型 | 大小 | 速度 | 精度 | 推荐场景 喵~ |
|------|------|------|------|----------|
| yolo26n.pt | 最小 | 最快 | 较低 | 实时性优先 喵~ |
| yolo26s.pt | 小 | 快 | 中等 | 平衡选择 喵喵~ |
| yolo26m.pt | 中等 | 中等 | 较高 | 高精度需求 喵~ |
| yolo26l.pt | 大 | 较慢 | 高 | 离线分析 喵喵~ |
| yolo26x.pt | 最大 | 最慢 | 最高 | 最高精度 喵~ |

### 检测类别 😺

COCO数据集80类物体索引 喵~

```
0: person          40: bottle
1: bicycle         41: wine glass
2: car             42: cup
3: motorcycle      43: fork
4: airplane        44: knife
5: bus             45: spoon
6: train           46: bowl
7: truck           47: banana
8: boat            48: apple
9: traffic light   49: sandwich
10: fire hydrant   50: orange
... 等
```

完整类别列表: [COCO Dataset](https://docs.ultralytics.com/datasets/detect/coco/) 喵~

## 高级用法 🐾

### 自定义监控区域 喵~

```python
from src.screen_capture import ScreenCapture

# 只监控屏幕的左上角 640x480 区域 喵~
capture = ScreenCapture({
    "top": 0,
    "left": 0,
    "width": 640,
    "height": 480
})

app = ScreenMonitorApp(detector=detector, capture=capture)
```

### 检测特定类别 喵~

```python
# 只检测人和车辆 喵~
detector = YOLODetector(
    model_path="yolo26n.pt",
    classes=[0, 1, 2, 3, 5, 7]  # person, bicycle, car, motorcycle, bus, truck
)
```

### 调整显示窗口 喵~

```python
app = ScreenMonitorApp(
    detector=detector,
    display_size=(1280, 720),  # 缩小显示 喵~
    fps_limit=30  # 限制FPS 喵喵~
)
```

## 性能优化 喵~

### CPU优化 😺

```python
config.screen.fps_limit = 15  # 降低FPS 喵~
config.detector.model_path = "yolo26n.pt"  # 使用最小模型 喵~
```

### GPU加速（需要NVIDIA GPU）喵~

1. 安装PyTorch GPU版本 喵~
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

2. 使用时会自动启用GPU加速 喵~

## 技术栈 🐾

- **检测框架**: [Ultralytics YOLO26](https://github.com/ultralytics/ultralytics) 喵~
- **屏幕捕获**: [MSS](https://github.com/BoboTiG/python-mss) 喵喵~
- **图像处理**: [OpenCV](https://opencv.org/) 喵~
- **数值计算**: [NumPy](https://numpy.org/) 喵~

## 系统要求 喵~

- Python 3.8+ 喵~
- Windows / Linux / macOS 喵喵~
- 至少4GB RAM 喵~
- 推荐使用独立显卡（可选）喵~

## 故障排除 喵~

### 问题：模型下载失败 😿

```bash
# 手动下载模型 喵~
python -c "from ultralytics import YOLO; YOLO('yolo26n.pt')"
```

### 问题：检测速度慢 喵~

- 使用更小的模型（yolo26n.pt）喵~
- 降低 `fps_limit` 喵喵~
- 减小 `display_size` 喵~
- 指定检测类别减少计算量 喵~

### 问题：OpenCV窗口无响应 喵~

确保在GUI环境运行，不支持纯SSH远程会话（需要X11转发）喵~

## 开发计划 喵~

- [ ] 支持录制检测视频 喵~
- [ ] 添加检测日志记录 喵喵~
- [ ] 支持多显示器 喵~
- [ ] 添加Web界面 喵喵~
- [ ] 导出检测结果到JSON/CSV 喵~

## 许可证 喵~

MIT License 喵~

## 贡献 喵~

欢迎提交Issue和Pull Request 喵喵~

---

**享受实时屏幕检测的乐趣喵~** 🐱😺🐾
