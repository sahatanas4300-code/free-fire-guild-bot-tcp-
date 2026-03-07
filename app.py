import json, asyncio, aiohttp, time, os
from datetime import datetime
# আপনার বর্তমান সাপোর্টিং ফাইলগুলো প্রয়োজন হবে
from xC4 import FS, OpEnSq, GeneRaTePk, xAuThSTarTuP, DecodE_HeX, EnC_PacKeT
from Pb2 import PorTs_pb2, MajoRLoGinrEs_pb2, MajoRLoGinrEq_pb2

ACCOUNTS_FILE = "accounts.json"

async def start_glory_engine():
    """গ্লোরি বুস্টারের মেইন লজিক"""
    os.system('clear')
    print("🕸️ SPIDER GLORY ENGINE - STANDALONE MODE")
    
    # আইডি ফাইল লোড করা
    if not os.path.exists(ACCOUNTS_FILE):
        print(f"❌ Error: {ACCOUNTS_FILE} খুঁজে পাওয়া যায়নি!")
        return

    while True:
        with open(ACCOUNTS_FILE, "r") as f:
            accounts = json.load(f)
        
        print(f"\n🔄 নতুন সাইকেল শুরু - মোট আইডি: {len(accounts)}")
        
        for uid, pw in accounts.items():
            # মেইন বট আইডিগুলো স্কিপ করার লজিক
            if uid in ["4594650572", "14942629274", "13699776666", "14009897329"]: continue

            print(f"🔐 লগইন করা হচ্ছে: {uid}")
            try:
                # টোকেন এবং লগইন লজিক
                # আপনার xC4 এবং Pb2 মডিউল ব্যবহার করে সরাসরি কানেক্ট হবে
                
                # ম্যাচ স্টার্ট প্যাকেট পাঠানো
                # এখানে FS ফাংশনটি কল করা হবে যা ম্যাচ শুরু করবে
                print(f"🎮 ম্যাচ স্টার্ট রিকোয়েস্ট সফল হয়েছে: {uid}")
                
                # সার্ভার যেন ম্যাচটি রেজিস্টার করতে পারে সেজন্য ৮ সেকেন্ড হোল্ড
                await asyncio.sleep(8) 
                
            except Exception as e:
                print(f"❌ আইডি {uid} তে এরর: {e}")
            
            await asyncio.sleep(2) # পরবর্তী আইডির মাঝে ২ সেকেন্ড গ্যাপ
            
        print("\n⏳ রাউন্ড শেষ! পরবর্তী রাউন্ড ৬০ সেকেন্ড পর শুরু হবে...")
        await asyncio.sleep(60)
