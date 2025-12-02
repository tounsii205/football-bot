from flask import Flask, request, jsonify
import os
import json
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

# Configuration
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
PAYPAL_EMAIL = os.environ.get('PAYPAL_EMAIL', 'tounsii205@gmail.com')
SUPABASE_REF = os.environ.get('SUPABASE_REF', 'wksopcigrtbirejcsmox')
PREMIUM_PRICE = int(os.environ.get('PREMIUM_PRICE', '15'))

TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "✅ Football Predictions Bot is running!",
        "bot": "@predit25_bot",
        "paypal": PAYPAL_EMAIL,
        "premium": f"${PREMIUM_PRICE}/month"
    })

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming Telegram messages"""
    try:
        update = request.get_json()
        
        if not update:
            return jsonify({"status": "no_update"})
        
        # Extract message data
        message = update.get('message', {})
        if not message:
            return jsonify({"status": "no_message"})
        
        chat_id = message.get('chat', {}).get('id')
        user_id = message.get('from', {}).get('id')
        username = message.get('from', {}).get('username', '')
        first_name = message.get('from', {}).get('first_name', '')
        text = message.get('text', '').strip()
        
        if not chat_id or not text:
            return jsonify({"status": "invalid_message"})
        
        print(f"[{datetime.now()}] 📨 Message from {first_name}: {text}")
        
        # Process the message
        process_message(chat_id, user_id, username, first_name, text)
        
        return jsonify({"status": "success"})
    
    except Exception as e:
        print(f"[{datetime.now()}] ❌ Error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)})

def send_message(chat_id, text):
    """Send message to Telegram user"""
    try:
        url = f"{TELEGRAM_API}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML"
        }
        response = requests.post(url, json=data)
        return response.json()
    except Exception as e:
        print(f"Error sending message: {e}")
        return None

def process_message(chat_id, user_id, username, first_name, text):
    """Process incoming message and respond"""
    
    # Handle commands
    if text == "/start":
        welcome = f"""🤖 مرحباً بك في <b>GoatPredict25</b>! ⚽

أنا بوت توقعات المباريات بتقنية AI + Human Analysis (70%+30%)

📝 <b>كيفاش تستعملني:</b>
1️⃣ صيفط اسم أي فريق (مثال: Real Madrid)
2️⃣ احصل على التوقعات!

🆓 <b>النسخة المجانية:</b>
- الفريق الفائز فقط

💎 <b>النسخة Premium (${PREMIUM_PRICE}/شهر):</b>
- النتيجة الدقيقة
- توقيت الأهداف
- الركنيات والتسديدات
- تحليل مفصل كامل

اضغط /premium للاشتراك

🚀 <b>جرب دابا:</b> صيفط اسم فريقك المفضل!"""
        send_message(chat_id, welcome)
    
    elif text == "/premium":
        premium_msg = f"""💎 <b>اشترك في Premium</b>

✅ النتيجة الدقيقة (Score exact)
✅ توقيت الأهداف (Goals timing)
✅ الركنيات (Corners prediction)
✅ التسديدات المركزة (Shots on target)
✅ الحيازة (Possession %)
✅ البطاقات (Yellow/Red cards)
✅ تحليل AI + Human مفصل (70%+30%)

💰 <b>السعر: ${PREMIUM_PRICE}/شهر فقط</b>

📧 <b>طريقة الدفع:</b>
1️⃣ ادفع ${PREMIUM_PRICE}$ على PayPal:
   👉 <code>{PAYPAL_EMAIL}</code>

2️⃣ بعد الدفع، صيفط:
   - Screenshot الدفع
   - أو Transaction ID

3️⃣ سيتم تفعيل Premium تلقائياً! ⚡

⚠️ <b>مهم:</b> تأكد من الدفع لنفس البريد أعلاه"""
        send_message(chat_id, premium_msg)
    
    elif text == "/help":
        help_msg = f"""❓ <b>المساعدة</b>

📝 <b>الأوامر:</b>
/start - بدء البوت
/premium - معلومات Premium (${PREMIUM_PRICE}/شهر)
/help - المساعدة

⚽ <b>كيفاش تحصل على التوقعات:</b>
1️⃣ صيفط اسم الفريق (مثال: Barcelona)
2️⃣ احصل على التوقعات!

🆓 <b>Free:</b> الفريق الفائز فقط
💎 <b>Premium (${PREMIUM_PRICE}/شهر):</b> تحليل كامل مفصل

📧 <b>للدعم:</b> {PAYPAL_EMAIL}"""
        send_message(chat_id, help_msg)
    
    else:
        # Team search
        send_message(chat_id, f"🔍 جاري البحث عن مباريات {text}...")
        
        # For now, simple response (you'll integrate with Composio later)
        response = f"""🆓 <b>توقعات مجانية - {text}</b>

⚽ الفريق الفائز المتوقع: {text}

━━━━━━━━━━━━━━━━
💎 <b>بغيتي تحليل مفصل؟</b>
اشترك في Premium ب ${PREMIUM_PRICE}/شهر فقط!

✅ النتيجة الدقيقة
✅ توقيت الأهداف
✅ الركنيات والتسديدات
✅ تحليل AI كامل

اضغط /premium للاشتراك"""
        send_message(chat_id, response)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
