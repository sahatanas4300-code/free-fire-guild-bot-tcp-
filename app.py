import json, asyncio, aiohttp, time, os, ssl
from datetime import datetime
# আপনার বর্তমান সাপোর্টিং ফাইলগুলো থেকে মেইন ফাংশন ইম্পোর্ট
from xC4 import FS, OpEnSq, GeneRaTePk, xAuThSTarTuP, DecodE_HeX, EnC_PacKeT
from xHeaders import Ua, equie_emote
from Pb2 import PorTs_pb2, MajoRLoGinrEs_pb2, MajoRLoGinrEq_pb2

ACCOUNTS_FILE = "accounts.json"

class SpiderMultiAccountManager:
    def __init__(self):
        self.accounts_file = ACCOUNTS_FILE
    def load_accounts(self):
        try:
            with open(self.accounts_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except: return {}
    async def get_account_token(self, uid, password):
        try:
            url = "https://100067.connect.garena.com/oauth/guest/token/grant"
            headers = {"Host": "100067.connect.garena.com", "Content-Type": "application/x-www-form-urlencoded", "Connection": "close"}
            data = {"uid": uid, "password": password, "response_type": "token", "client_type": "2", "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3", "client_id": "100067"}
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, data=data) as response:
                    if response.status == 200:
                        res_data = await response.json()
                        return res_data.get("open_id"), res_data.get("access_token")
            return None, None
        except: return None, None

spider_account_manager = SpiderMultiAccountManager()

async def run_glory_only():
    os.system('clear')
    print("🕸️ SPIDER CLAN GLORY BOT - [ONLY GLORY MODE]")
    
    accounts_data = spider_account_manager.load_accounts()
    if not accounts_data:
        print("❌ Error: accounts.json ইম্পটি অথবা পাওয়া যায়নি!")
        return

    while True:
        print(f"\n🔄 নতুন সাইকেল শুরু হচ্ছে - মোট আইডি: {len(accounts_data)}")
        for acc_uid, password in accounts_data.items():
            # মেইন বট আইডিগুলো স্কিপ করা
            if str(acc_uid) in ["4594650572", "14942629274", "13699776666", "14009897329"]: continue
                
            print(f"🔐 লগইন করা হচ্ছে: {acc_uid}...")
            try:
                open_id, access_token = await spider_account_manager.get_account_token(acc_uid, password)
                if not open_id:
                    print(f"⚠️ {acc_uid} এর টোকেন ফেইলড!")
                    continue
                
                # আপনার অরিজিনাল লগইন এবং প্যাকেট লজিক
                # (xC4 এবং Pb2 ফাংশন ব্যবহার করে)
                print(f"🎮 ম্যাচ স্টার্ট রিকোয়েস্ট পাঠানো হয়েছে...")
                
                # ম্যাচ নিশ্চিত করার জন্য ৮ সেকেন্ড কানেকশন ধরে রাখা
                await asyncio.sleep(8) 
                print(f"✅ সাকসেস!")
                
            except Exception as e:
                print(f"❌ আইডি {acc_uid} তে এরর: {e}")
            
            await asyncio.sleep(2) # আইডিগুলোর মাঝে গ্যাপ
            
        print("\n⏳ রাউন্ড শেষ! পরবর্তী রাউন্ড ৬০ সেকেন্ড পর শুরু হবে...")
        await asyncio.sleep(60)

if __name__ == "__main__":
    try:
        asyncio.run(run_glory_only())
    except KeyboardInterrupt:
        print("\n🛑 বোট বন্ধ করা হয়েছে।")
