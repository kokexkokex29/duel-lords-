# 🏆 Duel Lords - BombSquad Tournament Bot

نظام إدارة بطولات BombSquad شامل مع بوت Discord ومنصة ويب احترافية لتتبع إحصائيات اللاعبين وجدولة المباريات التلقائية.

## ✨ المميزات

### مميزات بوت Discord
- **أوامر Slash**: واجهة أوامر Discord حديثة
- **إدارة اللاعبين**: تسجيل وإزالة اللاعبين (للإدارة فقط)
- **إحصائيات البطولة**: تتبع الانتصارات والخسائر والتعادلات والقتل والوفيات
- **جدولة المباريات**: جدولة المبارزات التلقائية مع تذكيرات قبل 5 دقائق
- **Embeds غنية**: رسائل Discord جميلة ومهنية
- **دعم متعدد اللغات**: اللغة الإنجليزية والبرتغالية
- **معلومات الخادم**: وصول سريع لتفاصيل خادم BombSquad
- **نظام المتصدرين**: نظام ترتيب شامل

### مميزات منصة الويب
- **لوحة تحكم مباشرة**: إحصائيات البطولة في الوقت الفعلي
- **متصدري اللاعبين**: ترتيبات تفاعلية مع إحصائيات مفصلة
- **تاريخ المباريات**: سجل مباريات البطولة الكامل
- **تصميم متجاوب**: واجهة متوافقة مع الهواتف المحمولة
- **المظهر المظلم**: تصميم مظلم احترافي
- **واجهات برمجة التطبيقات**: API RESTful للوصول للبيانات

### مميزات إدارية
- **تحكم الإدارة**: أوامر مقيدة لإدارة البطولة
- **قاعدة بيانات دائمة**: قاعدة بيانات SQLite لتخزين البيانات
- **تذكيرات تلقائية**: إشعارات رسائل خاصة قبل المباريات
- **تتبع الإحصائيات**: مقاييس شاملة لأداء اللاعبين
- **تسجيل نتائج المباريات**: تتبع مفصل لنتائج المباريات

## 🚀 البدء السريع

### المتطلبات الأساسية
- Python 3.9 أو أعلى
- رمز بوت Discord
- معرفة أساسية بإعداد بوت Discord

### متغيرات البيئة
قم بإنشاء متغيرات البيئة التالية:

```bash
DISCORD_BOT_TOKEN=your_discord_bot_token_here
SESSION_SECRET=your_session_secret_key_here
```

### التشغيل المحلي

1. **استنساخ المستودع**
```bash
git clone <repository-url>
cd duel-lords-bot
```

2. **تثبيت التبعيات**
```bash
pip install -r requirements.txt
```

3. **تعيين متغيرات البيئة**
```bash
export DISCORD_BOT_TOKEN="your_bot_token"
export SESSION_SECRET="your_secret_key"
```

4. **تشغيل التطبيق**
```bash
python main.py
```

## 🌐 نشر على Render.com

### إنشاء ملف requirements.txt أولاً:
قم بإنشاء ملف `requirements.txt` في مجلد المشروع:

```txt
discord.py>=2.3.0
flask>=2.3.0
flask-sqlalchemy>=3.0.0
gunicorn>=21.0.0
psycopg2-binary>=2.9.0
sqlalchemy>=2.0.0
email-validator>=2.0.0
```

### خطوات النشر التفصيلية:

#### 1. إنشاء حساب Render.com
- اذهب إلى [render.com](https://render.com)
- أنشئ حساب جديد أو سجل الدخول بحساب موجود
- اربط حساب GitHub الخاص بك

#### 2. رفع الكود إلى GitHub
```bash
# إنشاء مستودع جديد على GitHub
git init
git add .
git commit -m "Initial commit - Duel Lords Bot"
git remote add origin https://github.com/yourusername/duel-lords-bot.git
git push -u origin main
```

#### 3. إنشاء Web Service جديد
- في لوحة تحكم Render، اضغط **"New +"**
- اختر **"Web Service"**
- اختر **"Build and deploy from a Git repository"**
- اختر المستودع الذي رفعته للتو

#### 4. إعداد الخدمة
```
Name: duel-lords-tournament
Runtime: Python 3
Region: Ohio (US East) - أو أقرب منطقة لك
Branch: main
Root Directory: . (فارغ)
Build Command: pip install -r requirements.txt
Start Command: python main.py
```

#### 5. إضافة متغيرات البيئة (Environment Variables)
في قسم **"Environment Variables"** أضف:

```
DISCORD_BOT_TOKEN: [ضع توكن البوت هنا]
SESSION_SECRET: [ضع مفتاح سري عشوائي هنا]
PORT: 5000
PYTHONUNBUFFERED: 1
```

لإنتاج SESSION_SECRET عشوائي:
```bash
# استخدم هذا الأمر أو أي مولد كلمات مرور
openssl rand -hex 32
```

#### 6. إعدادات متقدمة
- **Instance Type**: Free (للبداية) أو Starter (للاستخدام المستمر)
- **Auto-Deploy**: Yes (للنشر التلقائي عند التحديث)

#### 7. النشر والمراقبة
- اضغط **"Create Web Service"**
- راقب سجلات البناء في تبويب **"Logs"**
- انتظر حتى تظهر رسالة "Your service is live at..."

#### 8. إعداد Discord Bot
بعد النشر بنجاح:
- اذهب إلى [Discord Developer Portal](https://discord.com/developers/applications)
- اختر تطبيقك أو أنشئ واحد جديد
- في قسم **"Bot"**:
  - انسخ التوكن وضعه في متغيرات البيئة على Render
  - فعّل **"MESSAGE CONTENT INTENT"**
- في قسم **"OAuth2" > "URL Generator"**:
  - اختر **"bot"** و **"applications.commands"**
  - اختر الصلاحيات المطلوبة
  - انسخ الرابط وادع البوت لخادمك

### 🔧 استكشاف الأخطاء الشائعة

#### مشكلة: البوت لا يتصل
```bash
# تحقق من السجلات في Render
# ابحث عن: "Discord bot started" أو أخطاء التوكن
```

#### مشكلة: الموقع لا يعمل
```bash
# تحقق من أن PORT=5000 في متغيرات البيئة
# تأكد من أن Start Command هو: python main.py
```

#### مشكلة: أوامر Discord لا تظهر
```bash
# تحقق من أن البوت له صلاحيات applications.commands
# انتظر بضع دقائق حتى تتم مزامنة الأوامر
```

### 📊 مراقبة الأداء
- استخدم تبويب **"Metrics"** لمراقبة استخدام الذاكرة والمعالج
- راجع **"Logs"** بانتظام للتأكد من عدم وجود أخطاء
- فعّل **"Auto-Deploy"** للتحديثات التلقائية

### 💰 إدارة التكاليف
- **Free Tier**: يتوقف بعد 15 دقيقة من عدم النشاط
- **Starter Plan**: 7$/شهر، يعمل 24/7
- **Professional**: 25$/شهر، للاستخدام المكثف

### 🔄 التحديثات
```bash
# لتحديث الكود:
git add .
git commit -m "Update: وصف التحديث"
git push origin main

# Render سيقوم بالنشر تلقائياً إذا كان Auto-Deploy مفعل
```

## 🎮 أوامر Discord

### أوامر للاعبين
- `/ip` - عرض IP والمنفذ لخادم BombSquad
- `/stats [@player]` - عرض إحصائيات اللاعب
- `/leaderboard` - عرض ترتيب البطولة
- `/players` - قائمة جميع اللاعبين المسجلين

### أوامر الإدارة (فقط للإدارة)
- `/register @player name` - تسجيل لاعب جديد
- `/remove_player @player` - إزالة لاعب من البطولة
- `/update_stats @p1 @p2 result kills deaths` - تحديث نتائج المباراة
- `/duel @player1 @player2 day hour minute` - جدولة مبارزة

### أمثلة الاستخدام:
```
/register @JohnDoe "John the Bomber"
/duel @JohnDoe @JaneSmith 25 18 30
/update_stats @JohnDoe @JaneSmith player1_win 5 2 3 5
```

## 🏗️ بنية المشروع

```
duel-lords-bot/
├── app.py              # تطبيق Flask الرئيسي والنماذج
├── bot.py              # بوت Discord وأوامره
├── database.py         # مدير قاعدة البيانات SQLite
├── web_routes.py       # مسارات منصة الويب
├── keepalive.py        # خادم الويب للحفاظ على النشاط
├── main.py             # نقطة الدخول الرئيسية
├── translations.py     # نظام الترجمة
├── models.py           # تعريفات نماذج قاعدة البيانات
├── templates/          # قوالب HTML
│   ├── base.html
│   ├── index.html
│   ├── leaderboard.html
│   └── players.html
├── static/
│   └── style.css       # أنماط CSS مخصصة
└── README.md
```

## 🎯 معلومات الخادم

- **IP الخادم**: `18.228.228.44`
- **المنفذ**: `3827`
- **العنوان الكامل**: `18.228.228.44:3827`

## 🔧 التطوير

### إضافة أوامر جديدة:
1. افتح `bot.py`
2. أضف دالة الأمر الجديد مع `@bot.tree.command`
3. تأكد من مزامنة الأوامر مع `await bot.tree.sync()`

### إضافة صفحات ويب جديدة:
1. أضف مسار في `web_routes.py`
2. أنشئ قالب HTML في `templates/`
3. أضف الأنماط في `static/style.css`

### تخصيص قاعدة البيانات:
- عدل النماذج في `app.py`
- أضف وظائف قاعدة البيانات في `database.py`

## 🐛 استكشاف الأخطاء وإصلاحها

### مشاكل شائعة:
1. **البوت غير متصل**: تحقق من صحة `DISCORD_BOT_TOKEN`
2. **أخطاء قاعدة البيانات**: تأكد من وجود أذونات الكتابة
3. **أوامر لا تعمل**: تحقق من مزامنة الأوامر في السجلات
4. **موقع الويب لا يحمل**: تحقق من منفذ الخادم والإعدادات

### عرض السجلات:
```bash
# في Render.com
انتقل إلى Dashboard -> Your Service -> Logs

# محلياً
تحقق من مخرجات وحدة التحكم
```

## 📊 نظام النقاط

- **فوز**: 3 نقاط
- **تعادل**: 1 نقطة
- **خسارة**: 0 نقطة

## 🔒 الأمان

- أوامر الإدارة مقيدة للمديرين فقط
- جلسات آمنة للموقع
- التحقق من صحة البيانات
- حماية من SQL injection

## 🤝 المساهمة

1. Fork المستودع
2. أنشئ فرع للميزة (`git checkout -b feature/AmazingFeature`)
3. Commit التغييرات (`git commit -m 'Add some AmazingFeature'`)
4. Push للفرع (`git push origin feature/AmazingFeature`)
5. افتح Pull Request

## 📝 الترخيص

هذا المشروع مرخص تحت رخصة MIT - راجع ملف [LICENSE](LICENSE) للتفاصيل.

## 🙏 الشكر والتقدير

- [Discord.py](https://discordpy.readthedocs.io/) - مكتبة بوت Discord
- [Flask](https://flask.palletsprojects.com/) - إطار عمل الويب
- [Bootstrap](https://getbootstrap.com/) - إطار عمل CSS
- [BombSquad](https://www.froemling.net/apps/bombsquad) - اللعبة

---

صنع بـ ❤️ لمجتمع BombSquad العربي