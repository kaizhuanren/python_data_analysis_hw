import pandas as pd
import matplotlib.pyplot as plt

# 创建关键词频率数据
data = {
    "keyword": [
        "learning", "network", "neural", "deep", "via", "graph", "image", "data", "adversarial", "detection",
        "representation", "reinforcement", "optimization", "object", "model", "estimation", "efficient", "robust",
        "video", "prediction", "segmentation", "training", "transformer", "diffusion", "language", "large", 
        "generation", "towards", "multimodal", "knowledge", "framework"
    ],
    "2020": [
        1677, 969, 628, 513, 459, 431, 336, 276, 269, 256, 243, 237, 229, 226, 213, 191, 186, 181, 180, 163,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    ],
    "2021": [
        1951, 911, 706, 448, 562, 460, 338, 290, 249, 296, 326, 302, 246, 249, 268, 0, 226, 206, 204, 0,
        214, 202, 0, 0, 0, 0, 0, 0, 0, 0, 0
    ],
    "2022": [
        2112, 795, 728, 391, 658, 516, 459, 316, 242, 392, 359, 325, 283, 327, 351, 0, 252, 237, 266, 0,
        245, 0, 388, 0, 0, 0, 0, 0, 0, 0, 0
    ],
    "2023": [
        2477, 809, 860, 354, 855, 633, 584, 403, 0, 445, 447, 391, 332, 353, 760, 0, 342, 0, 322, 0,
        289, 0, 363, 371, 330, 0, 0, 0, 0, 0, 0
    ],
    "2024": [
        2720, 762, 858, 0, 1166, 733, 785, 561, 0, 518, 499, 436, 454, 0, 1569, 0, 474, 0, 453, 0,
        245, 0, 513, 834, 886, 615, 575, 409, 0, 0, 0
    ],
    "2025": [
        668, 220, 163, 0, 332, 258, 239, 137, 0, 218, 118, 436, 153, 0, 387, 0, 153, 0, 126, 0,
        113, 0, 0, 174, 298, 226, 164, 0, 179, 137, 135
    ]
}

df = pd.DataFrame(data)
df.set_index("keyword", inplace=True)
df = df.sort_index()

# 绘制热力图形式的可视化
plt.figure(figsize=(18, 10))
plt.imshow(df.fillna(0), aspect="auto", cmap="YlGnBu")
plt.xticks(ticks=range(len(df.columns)), labels=df.columns)
plt.yticks(ticks=range(len(df.index)), labels=df.index)
plt.colorbar(label="Frequency")
plt.title("Keyword Frequencies by Year (2020–2025)")
plt.xlabel("Year")
plt.ylabel("Keyword")
plt.grid(False)
plt.tight_layout()
plt.show()
