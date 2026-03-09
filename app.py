import json
import asyncio
import aiohttp
import os
import sys

# মডিউল ইম্পোর্ট
try:
    from xC4 import EncRypTMajoRLoGin, MajorLogin, DecRypTMajoRLoGin, GetLoginData, DecRypTLoGinDaTa, xAuThSTarTuP, FS, OpEnSq, SEnd_InV, CrEaTe_ProTo, GeneRaTePk
except ImportError:
    print("❌ xC4.py মডিউল পাওয়া যায়নি!")

ACCOUNTS_FILE = "accounts.json"
REGION = "sg" # রিজিয়ন (ind, bd বা sg)
CLAN_ID = "3063703446"

async def get_access_token(uid, password):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"uid": uid, "password": password, "response_type": "token", "client_type": "2", "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3", "client_id": "100067"}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=data, timeout=10) as resp:
                if resp.status == 200:
                    res = await resp.json()
                    return res.get("open_id"), res.get("access_token")
    except: pass
    return None, None

async def Apply_Guild_Packet(clan_id, K, V):
    """গিল্ডে রিকোয়েস্ট পাঠানোর কাস্টম প্যাকেট"""
    fields = {1: 18, 2: {1: int(clan_id)}} # Garena Clan Apply Action
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '0515', K, V)

async def process_bot(bot_info, action="apply", team_members=[]):
    """এই ফাংশনটি রিকোয়েস্ট পাঠানো এবং গেম খেলা—দুটি কাজই করবে"""
    uid = bot_info['uid']
    try:
        open_id, token = await get_access_token(uid, bot_info['pwd'])
        if not open_id: return False

        PyL = await EncRypTMajoRLoGin(open_id, token)
        res = await MajorLogin(PyL)
        if not res: return False

        auth = await DecRypTMajoRLoGin(res)
        LoGinDaTa = await GetLoginData(auth.url, PyL, auth.token)
        dec_data = await DecRypTLoGinDaTa(LoGinDaTa)
        
        OnLineiP, OnLineporT = dec_data.Online_IP_Port.split(":")
        AutHToKen = await xAuThSTarTuP(int(auth.account_uid), auth.token, int(auth.timestamp), auth.key, auth.iv)

        reader, writer = await asyncio.open_connection(OnLineiP, int(OnLineporT))
        writer.write(bytes.fromhex(AutHToKen))
        await writer.drain()
        await asyncio.sleep(2) 

        # --- লজিক ১: গিল্ডে রিকোয়েস্ট পাঠানো ---
        if action == "apply":
            req_packet = await Apply_Guild_Packet(CLAN_ID, auth.key, auth.iv)
            writer.write(req_packet)
            await writer.drain()
            print(f"📩 [{uid}] গিল্ডে জয়েন রিকোয়েস্ট পাঠিয়েছে!")
            
        # --- লজিক ২: স্কোয়াড ও ম্যাচ স্টার্ট ---
        elif action == "play":
            if team_members: # যদি লিডার হয়
                sq_packet = await OpEnSq(auth.key, auth.iv, REGION)
                writer.write(sq_packet)
                await writer.drain()
                await asyncio.sleep(2)
                
                # মেম্বারদের ইনভাইট দেওয়া
                for mem in team_members:
                    inv_packet = await SEnd_InV(1, mem['uid'], auth.key, auth.iv, REGION)
                    writer.write(inv_packet)
                    await writer.drain()
                
                print(f"🎮 [LEADER: {uid}] টিম রেডি করে ম্যাচ স্টার্ট দিচ্ছে!")
            else:
                print(f"👥 [MEMBER: {uid}] স্কোয়াডে জয়েন করার জন্য রেডি।")
                
            # সবাই ম্যাচ স্টার্ট (FS) প্যাকেট পাঠাবে গ্লোরি কনফার্ম করতে
            match_packet = await FS(auth.key, auth.iv)
            writer.write(match_packet)
            await writer.drain()
            await asyncio.sleep(8) 

        writer.close()
        await writer.wait_closed()
        return True

    except Exception as e:
        return False

async def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    print("="*55)
    print("🕸️ SPIDER ADVANCED GLORY BOOSTER (AUTO REQUEST) 🕸️")
    print("="*55)

    if not os.path.exists(ACCOUNTS_FILE):
        print("❌ accounts.json ফাইল নেই!")
        return

    with open(ACCOUNTS_FILE, "r") as f:
        accounts_dict = json.load(f)

    all_bots = [{'uid': u, 'pwd': p} for u, p in accounts_dict.items() if str(u) not in ["4594650572", "14942629274"]]

    # ================= [ ধাপ ১: গিল্ড রিকোয়েস্ট ] =================
    print(f"\n🛡️ ধাপ ১: {len(all_bots)} টি বট থেকে গিল্ড রিকোয়েস্ট পাঠানো হচ্ছে...")
    tasks = [process_bot(bot, action="apply") for bot in all_bots]
    await asyncio.gather(*tasks)

    print("\n" + "="*55)
    print(f"👑 মামা, সব বট থেকে {CLAN_ID} গিল্ডে রিকোয়েস্ট পাঠানো হয়েছে!")
    print("👑 গেম ওপেন করে আপনার মেইন আইডি থেকে রিকোয়েস্টগুলো অ্যাকসেপ্ট করুন।")
    print("="*55)

    # আপনার জন্য অপেক্ষা করবে
    await asyncio.get_event_loop().run_in_executor(None, input, "\n👉 অ্যাকসেপ্ট করা শেষ হলে এখানে ENTER চাপুন (ম্যাচ স্টার্ট হবে)... ")

    # ================= [ ধাপ ২: স্কোয়াড গ্লোরি ফার্মিং ] =================
    print("\n🎮 ধাপ ২: ৫টি টিম তৈরি এবং গ্লোরি ফার্মিং শুরু হচ্ছে...\n")
    teams = [all_bots[i:i+4] for i in range(0, len(all_bots), 4)]

    round_num = 1
    while True:
        print(f"🔄 ======= রাউন্ড {round_num} =======")
        for index, team in enumerate(teams):
            leader = team[0]
            members = team[1:]
            
            print(f"🚀 --- TEAM-{index+1} প্রসেসিং ---")
            tasks = [process_bot(mem, action="play", team_members=[]) for mem in members]
            tasks.append(process_bot(leader, action="play", team_members=members))
            
            await asyncio.gather(*tasks)
            await asyncio.sleep(5)
            
        print(f"\n💤 রাউন্ড {round_num} শেষ। পরবর্তী রাউন্ড ৬০ সেকেন্ড পর...")
        await asyncio.sleep(60)
        round_num += 1

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 বোটটি বন্ধ করা হয়েছে।")
        sys.exit(0)
