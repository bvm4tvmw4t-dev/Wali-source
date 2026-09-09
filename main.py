import os
import sys
import asyncio
from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaDocument, MessageMediaPhoto

# استخراج البيانات من فارات البيئة أو وضعها افتراضياً
API_ID = int(os.environ.get("API_ID", "1234567"))
API_HASH = os.environ.get("API_HASH", "your_api_hash")

client = TelegramClient("wali_source", API_ID, API_HASH)

# قاعدة بيانات مؤقتة للفارات داخل السورس
VARIABLES = {}

# قاموس الخطوط لميزة FONTS_AUTO
FONTS = {
    "font1": str.maketrans("0123456789", "𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗"),
    "font2": str.maketrans("0123456789", "𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵"),
    "font3": str.maketrans("0123456789", "０１２３４５６７８９"),
    "font4": str.maketrans("0123456789", "𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡𝟘"),
    "font5": str.maketrans("0123456789", "𝟢𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫"),
    "font6": str.maketrans("0123456789", "①②③④⑤⑥⑦⑧⑨⓪"),
    "font7": str.maketrans("0123456789", "❶❷❸❹❺❻❼❽❾⓿"),
    "font8": str.maketrans("0123456789", "0123456789"),
    "font9": str.maketrans("0123456789", "₁₂₃₄₅₆₇₈₉₀"),
    "font10": str.maketrans("0123456789", "𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿"),
    "font11": str.maketrans("0123456789", "١٢٣٤٥٦٧٨٩٠"),
}

# --- نظام إدارة الفارات ---
@client.on(events.NewMessage(outgoing=True, pattern=r"^\.اضف فار (.+) (.+)"))
async def add_var(event):
    var_name = event.pattern_match.group(1).strip()
    var_value = event.pattern_match.group(2).strip()
    VARIABLES[var_name] = var_value
    await event.edit(f"☑️ **تم بنجاح إضافة الفار:**\n`{var_name}`\n\n• القيمة:\n`{var_value}`\n\nℹ️ أرسل `.تحديث` لتطبيق التغييرات.")

@client.on(events.NewMessage(outgoing=True, pattern=r"^\.حذف فار (.+)"))
async def del_var(event):
    var_name = event.pattern_match.group(1).strip()
    if var_name in VARIABLES:
        del VARIABLES[var_name]
        await event.edit(f"🗑 **تم حذف الفار بنجاح:**\n`{var_name}`\n\nℹ️ أرسل `.تحديث` إذا تطلب الأمر.")
    else:
        await event.edit(f"❌ **عذراً، الفار `{var_name}` غير موجود.**")

@client.on(events.NewMessage(outgoing=True, pattern=r"^\.جلب فار (.+)"))
async def get_var(event):
    var_name = event.pattern_match.group(1).strip()
    if var_name in VARIABLES:
        await event.edit(f"🔍 **معلومات الفار `{var_name}`:**\n\nالقيمة: `{VARIABLES[var_name]}`")
    else:
        await event.edit(f"❌ **الفار `{var_name}` غير مسجل لديك.**")

@client.on(events.NewMessage(outgoing=True, pattern=r"^\.تحديث$"))
async def restart_bot(event):
    await event.edit("🔄 **جاري تحديث السورس وتطبيق الفارات...**")
    os.execl(sys.executable, sys.executable, *sys.argv)

# --- ميزة جلب الوقتية / الوسائط ذات العرض الواحد ---
@client.on(events.NewMessage(outgoing=True, pattern=r"^\.جلب الوقتية$"))
async def get_view_once(event):
    reply = await event.get_reply_message()
    if not reply:
        await event.edit("❌ **يرجى الرد على الصورة أو الفيديو المؤقت (العرض الواحد).**")
        return
    
    await event.edit("⏳ **جاري سحب الحفظ المؤقت...**")
    try:
        media = await reply.download_media()
        await client.send_file("me", media, caption="📥 **تم سحب الصورة/الفيديو المؤقت بنجاح بواسطة سورس الوالي.**")
        os.remove(media)
        await event.edit("✅ **تم سحب الوسائط وإرسالها إلى المحفوظات بنجاح!**")
    except Exception as e:
        await event.edit(f"❌ حدث خطأ أثناء السحب: `{str(e)}`")

print("🤖 السورس جاهز للتشغيل...")
client.start()
client.run_until_disconnected()
