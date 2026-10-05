import time, json, sys
from ultralytics import YOLO
from ultralytics.utils import ASSETS
img=str(ASSETS/'bus.jpg')
res=[]
for tag,kw in [("one-to-one (end2end, NMS-free)",dict(end2end=True)),("one-to-many + NMS",dict(end2end=False))]:
    p=YOLO('yolo26n.pt').export(format='onnx',imgsz=640,verbose=False,simplify=False,**kw)
    m=YOLO(p,task='detect')
    for conf in (0.25,0.001):
        m.predict(img,conf=conf,iou=0.7,device='cpu',verbose=False)
        n=30; acc=dict(preprocess=0,inference=0,postprocess=0)
        for _ in range(n):
            r=m.predict(img,conf=conf,iou=0.7,device='cpu',verbose=False)[0]
            for k in acc: acc[k]+=r.speed[k]/n
        res.append(dict(head=tag,conf=conf,**{k+'_ms':round(v,2) for k,v in acc.items()},boxes=len(r.boxes)))
        print(res[-1],flush=True)
json.dump(res,open('onnx_bench.json','w'),indent=1)
