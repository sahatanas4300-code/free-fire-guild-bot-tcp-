import json
import asyncio
import aiohttp
import os
import random
import sys

# xC4 theke dorkari jinish import kora
try:
    from xC4 import (
        EncRypTMajoRLoGin, MajorLogin, DecRypTMajoRLoGin, 
        GetLoginData, DecRypTLoGinDaTa, xAuThSTarTuP, 
        CrEaTe_ProTo, GeneRaTePk
    )
except ImportError:
    print("❌ xC4.py module paoa jayni! Library install korun.")

ACCOUNTS_FILE = "accounts.json"
CLAN_ID = "3063703446" # আপনার গিল্ড আইডি

async def Apply_Guild_Packet(uid, clan_id, K, V):
    """গ্লোবাল হেডার 0515 এবং অ্যাকশন 18 ব্যবহার করে জয়েন রিকোয়েস্ট"""
    packet_type = "0515" # গ্লোবাল/ইউএই হেডার
    
    fields = {
        1: 18, # সাধারণ গিল্ড জয়েন রিকোয়েস্ট
        2: {
            1: int(clan_id), # আপনার গিল্ড আইডি
            2: "S M ROBOT",  # বটের নাম (ঐচ্ছিক)
            11: int(uid)     # বটের নিজস্ব UID
        }
    }
    
    # প্যাকেট জেনারেট করা
    proto_data = await CrEaTe_ProTo(fields)
    return await GeneRaTePk(proto_data.hex(), packet_type, K, V)

    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet_type, K, V)

    # প্রোটোবাফ ডাটা জেনারেট এবং এনক্রিপশন
    proto_data = await CrEaTe_ProTo(fields)
    return await GeneRaTePk(proto_data.hex(), packet_type, K, V)

async def get_access_token(uid, password):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    data = {
        "uid": uid, 
        "password": password, 
        "response_type": "token", 
        "client_type": "2", 
        "client_id": "100067"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as resp:
            if resp.status == 200:
                res = await resp.json()
                return res.get("open_id"), res.get("access_token")
    return None, None

async def process_bot(bot_info, action="apply"):
    uid = bot_info['uid']
    try:
        open_id, token = await get_access_token(uid, bot_info['pwd'])
        if not open_id: return False

        # লগইন প্রসেস এবং সিকিউরিটি কি (Key/IV) সংগ্রহ
        PyL = await EncRypTMajoRLoGin(open_id, token)
        res = await MajorLogin(PyL)
        auth = await DecRypTMajoRLoGin(res)
        LoGinDaTa = await GetLoginData(auth.url, PyL, auth.token)
        dec_data = await DecRypTLoGinDaTa(LoGinDaTa)
        
        OnLineiP, OnLineporT = dec_data.Online_IP_Port.split(":")
        AutHToKen = await xAuThSTarTuP(int(auth.account_uid), auth.token, int(auth.timestamp), auth.key, auth.iv)

        # TCP কানেকশন তৈরি
        reader, writer = await asyncio.open_connection(OnLineiP, int(OnLineporT))
        writer.write(bytes.fromhex(AutHToKen))
        await writer.drain()

        if action == "apply":
            # গিল্ড রিকোয়েস্ট প্যাকেট পাঠানো
            req_packet = await Apply_Guild_Packet(uid, CLAN_ID, auth.key, auth.iv)
            writer.write(req_packet)
            await writer.drain()
            print(f"📩 [{uid}] গিল্ড জয়েন রিকোয়েস্ট সফলভাবে পাঠিয়েছে!")

        writer.close()
        await writer.wait_closed()
        return True
    except Exception as e:
        return False

async def main():
    print("🕸️ SPIDER ADVANCED GLORY BOOSTER 🕸️")
    
    if not os.path.exists(ACCOUNTS_FILE):
        print(f"❌ {ACCOUNTS_FILE} পাওয়া যায়নি!")
        return

    with open(ACCOUNTS_FILE, "r") as f:
        data = json.load(f)
    
    # ২০টি বট ফিল্টার করা
    bots = [{'uid': b['uid'], 'pwd': b['password']} for b in data[:20]]

    print(f"\n🛡️ ধাপ ১: {len(bots)}টি বট থেকে গিল্ড রিকোয়েস্ট পাঠানো হচ্ছে...")
    await asyncio.gather(*[process_bot(b, "apply") for b in bots])

    print("\n✅ রিকোয়েস্ট পাঠানো শেষ! গেমে গিয়ে মেম্বার লিস্ট চেক করুন।")
    input("\n👉 রিকোয়েস্ট এক্সেপ্ট করা শেষ হলে ENTER চাপুন (ম্যাচ স্টার্ট হবে)...")
    
    print("\n🎮 ধাপ ২: গ্লোরি ফার্মিং শুরু হচ্ছে...")
    # এখানে আপনার ম্যাচ মেকিং বা গ্লোরি ফার্মিং লজিক বসবে

if __name__ == "__main__":
    asyncio.run(main())
