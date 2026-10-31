# إضافة ثغرة جديدة (عند صدورها)

الإطار مبني عشان تضيف طريقة في دقائق، بدون لمس باقي الكود.

## 1) أنشئ ملف

```
jmz/methods/newexploit.py
```

```python
from .base import Method

class NewExploit(Method):
    def __init__(self):
        super().__init__(
            name="newexploit",
            chips=["A15", "A16"],      # المعالجات المدعومة
            offline=True,               # هل تلغي شرط الإنترنت؟
            needs_hardware=[],          # ["RP2350"] لو تحتاج لوحة
            ios_max=27.0,               # أقصى إصدار
            description="ثغرة جديدة — وصف قصير",
        )

    def steps(self):
        return ["خطوة 1", "خطوة 2"]

    def run(self, device):
        return {"ok": True, "log": "..."}
```

## 2) سجّلها

في `jmz/methods/__init__.py`:

```python
from .newexploit import NewExploit
REGISTRY.add(NewExploit())
```

## 3) حدّث المصفوفة

في `jmz/support.py` أضف الفرع:

```python
if chip in ("A15", "A16") and v <= 27.0:
    return {"verdict": "supported", "method": "newexploit", "offline": True,
            "requires": [], "notes": ["ثغرة جديدة"]}
```

## 4) اختبر

```bash
python -m jmz plan --chip A15 --ios 26.1
python -m unittest discover -s tests -v
```

15 اختبار موجودة — أضف اختباراً للطريقة الجديدة قبل الدمج.

## قواعد التصميم

1. **لا نجاح كاذب**: `ok` لا يكون True إلا بدليل من المخرجات.
2. **تحقق قبل التنفيذ**: افحص الشريحة والإصدار.
3. **قابلية التراجع**: أي خطوة تكتب على الجهاز تحتاج نسخة احتياطية.
4. **الشفافية**: كل طريقة تعيد `log` كامل.
