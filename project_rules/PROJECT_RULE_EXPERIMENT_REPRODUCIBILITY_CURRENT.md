# DeepLearning-HANK Experiment Reproducibility Rule

最后更新：2026-08-20

适用范围：

- HANK simulation；
- Deep Learning experiment；
- numerical solver experiment；
- calibration experiment；
- paper result generation。

---

# 0. 总原则

实验结果必须可追溯。

一个实验结果必须回答：

- 使用什么代码？
- 使用什么模型？
- 使用什么数据？
- 使用什么配置？
- 得到了什么结果？
- 结果限制是什么？

失败实验也是科研资产。

禁止删除：

- failed experiment；
- negative result；
- unsuccessful hypothesis test。

失败结果应记录原因。

---

# 1. Experiment Identity

每个实验必须具有：

## Experiment ID

格式建议：

`EXP-YYYYMMDD-NAME`

例如：

`EXP-20260820-HANK-AR1-001`

---

必须记录：

- Experiment ID；
- date；
- researcher；
- purpose；
- hypothesis；
- research question。

---

# 2. Code Environment

必须记录：

## Version

包括：

- Git commit SHA；
- branch；
- repository。

---

## Software

包括：

Python：

- Python version；
- package versions；
- environment file。

MATLAB：

- MATLAB version；
- toolbox version。

---

## Hardware

包括：

- CPU；
- GPU；
- memory；
- operating system。

---

## Randomness

必须记录：

- random seed；
- seed policy；
- deterministic setting。

如果无随机：

记录：

`NOT_APPLICABLE`

---

# 3. Model Configuration

实验必须保存：

## Economic Configuration

包括：

- parameters；
- calibration file；
- model version；
- equation version。

---

## Deep Learning Configuration

包括：

- architecture；
- optimizer；
- learning rate；
- batch size；
- epochs；
- loss function；
- evaluation metric。

---

## Solver Configuration

包括：

- solver method；
- tolerance；
- maximum iteration；
- convergence criteria。

---

# 4. Dataset Record

必须记录：

## Source

包括：

- dataset name；
- provider；
- version/date。

---

## Sample

包括：

- sample period；
- selection rule；
- inclusion/exclusion criteria。

---

## Processing

包括：

- preprocessing；
- normalization；
- filtering；
- missing value handling。

---

# 5. Result Record

每个实验必须保存：

## Baseline

包括：

- baseline definition；
- comparison target。

---

## Metrics

包括：

- numerical metrics；
- economic metrics；
- evaluation criteria。

---

## Outputs

包括：

- tables；
- figures；
- generated files；
- hashes。

---

## Interpretation

必须区分：

- observation；
- explanation；
- hypothesis support。

禁止：

从单次实验直接推出过强经济结论。

---

## Limitations

必须记录：

- known limitations；
- unresolved issues；
- future work。

---

# 6. Experiment Status

统一状态：

## PASS

定义：

实验目标完成。

证据：

- environment recorded；
- configuration recorded；
- output verified。

---

## PASS_WITH_OBSERVATIONS

定义：

实验基本完成。

但是存在：

- limitations；
- minor warnings；
- unresolved observations。

---

## BLOCKED

定义：

实验无法继续。

原因可能：

- environment；
- missing data；
- solver failure；
- insufficient evidence。

要求：

保存 blocker evidence。

---

## FAILED_RESEARCH_HYPOTHESIS

定义：

实验运行正确。

但是研究假设未获得支持。

例如：

- treatment 无显著效果；
- model improvement 不成立；
- hypothesis rejected。

该状态不是工程失败。

---

# 7. Output Safety

实验输出默认：

- timestamped；
- no-overwrite；
- manifest；
- hash。

禁止：

- 覆盖旧结果；
- 删除失败结果；
- 混用不同实验输出。

---

# 8. Paper Result Boundary

只有满足：

- reproducibility；
- diagnostic review；
- output verification；
- scientific interpretation review；

实验结果才可以进入论文 Results。

代码运行成功不等于科研结论成立。

---

# 9. Final Principle

失败实验：

不是垃圾。

失败实验：

是科研路径的一部分。
