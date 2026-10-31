# justmgz

تطبيق ويندوز (نافذة أصلية) لتشغيل محرك [tr4mpass](https://github.com/tr4m0ryp/tr4mpass)
وفتح قفل iCloud. يثبت المتطلبات، يبني المحرك، يمرر USB، ويكشف الجهاز تلقائياً.

## التحميل
https://github.com/moha700m/justmgz/releases/latest/download/justmgz.exe

## البناء
```powershell
.\build-local.ps1
```
أو ادفع تعديلاً — GitHub Actions يبني وينشر تلقائياً.

## البنية
- `justmgz.py` — التطبيق (UAC، WSL، بناء المحرك، usbipd، نافذة WebView2)
- `app/justmgz-engine.py` — الجسر: EventBus + SSE + 5 باكندات كشف + محاكي
- `app/ui.html` — الواجهة العربية
- `app/names.json` — 82 موديل
