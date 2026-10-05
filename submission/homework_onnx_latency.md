# Bài tập về nhà 3 — Export ONNX và đo latency trên CPU

`yolo26n.pt` → ONNX (imgsz 640, `model.export(format="onnx", end2end=True/False)`), chạy bằng ONNX Runtime trên CPU của máy cá nhân,
`bus.jpg`, trung bình 30 lần sau 1 lần warm-up, `iou=0.7` (script: `onnx_bench.py`, số liệu thô: `onnx_bench.json`).

| Head | conf | preprocess (ms) | inference (ms) | postprocess (ms) | số box |
|---|---:|---:|---:|---:|---:|
| one-to-one (NMS-free) | 0.25 | 12.09 | 79.23 | 0.68 | 5 |
| one-to-one (NMS-free) | 0.001 | 11.30 | 80.45 | 0.56 | 177 |
| one-to-many + NMS | 0.25 | 12.08 | 76.61 | 5.81 | 5 |
| one-to-many + NMS | 0.001 | 11.45 | 77.55 | 7.61 | 186 |

**Nhận xét.**
- Preprocess và inference gần như bằng nhau giữa hai head (cùng backbone/neck); khác biệt nằm ở postprocess.
- Trên CPU, postprocess của one-to-many + NMS là 5.8 ms ở conf 0.25 và 7.6 ms ở conf 0.001, so với 0.6–0.7 ms của one-to-one: chậm hơn ~8–14 lần,
  gấp nhiều lần so với chênh lệch ~1 ms đo trên GPU T4 ở mục 1C (1.6 ms so với 0.5 ms).
- Chi phí NMS tăng theo số box ứng viên (5.8 → 7.6 ms khi conf hạ từ 0.25 xuống 0.001), còn one-to-one gần như không đổi (0.68 → 0.56 ms),
  nên NMS-free cho độ trễ ổn định hơn khi cảnh đông hoặc ngưỡng thấp.
- Tổng latency vẫn bị inference chi phối (~77–80 ms); NMS-free chỉ giảm phần postprocess. Số liệu phụ thuộc máy, chỉ dùng để so sánh tương đối.
