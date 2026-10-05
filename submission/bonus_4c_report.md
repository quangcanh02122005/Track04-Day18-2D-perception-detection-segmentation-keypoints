# Bonus 4C — Val lật gương và flip_idx

Train YOLO26n-pose 40 epoch, imgsz 640, T4, seed 0. Pose mAP50-95:

| Model | val gốc | val lật gương |
|---|---:|---:|
| flip_idx giải phẫu | 0.436 | 0.425 |
| flip_idx đồng nhất | 0.415 | 0.275 |

Model đồng nhất tụt 0.415 → 0.275 (khoảng −34%) khi hổ quay trái, còn model giải phẫu gần như giữ nguyên (−0.01).

**Metric nào che lỗi?** Trên val gốc hai model chỉ khác 0.02 (0.436 so với 0.415), và Pose mAP50 đều ~0.995 nên mAP50 hoàn toàn che lỗi; mAP50-95 chỉ lộ nhẹ. Nguyên nhân: mọi hổ ở train và val đều quay phải (210/0 và 53/0), nên val gốc không có ca nào để nhãn trái/phải bị đảo. Lỗi chỉ lộ ra khi đổi phân phối (val lật gương).

**Thiết kế val tốt hơn:** thêm các tình huống triển khai vào val (hổ quay cả hai hướng, lật gương, xoay nhẹ, che khuất), tách theo video/cảnh để tránh ảnh gần trùng (các ảnh Frame_* cùng video), báo cáo mAP50-95 và OKS theo từng keypoint/từng nhóm trái-phải thay vì chỉ mAP50.
