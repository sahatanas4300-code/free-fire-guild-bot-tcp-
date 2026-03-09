import json
import asyncio
import aiohttp
import os
import random

# xC4 theke dorkari jinish import kora
try:
    from xC4 import EncRypTMajoRLoGin, MajorLogin, DecRypTMajoRLoGin, GetLoginData, DecRypTLoGinDaTa, xAuThSTarTuP, FS, OpEnSq, SEnd_InV, CrEaTe_ProTo, GeneRaTePk
except ImportError:
    print("❌ xC4.py module paoa jayni!")

ACCOUNTS_FILE = "accounts.json"
REGION = "sg"
CLAN_ID = "3063703446" # Apnar Guild ID

async def Apply_Guild_Packet(uid, clan_id, K, V):
    """Spam join packet structure"""
    fields = {
        1: 18,
        2: {
            1: int(clan_id),
            2: "S M ROBOT",
            11: int(uid)
        }
    }
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '0515', K, V)

async def get_access_token(uid, password):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    data = {"uid": uid, "password": password, "response_type": "token", "client_type": "2", "client_id": "100067"}
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

        PyL = await EncRypTMajoRLoGin(open_id, token)
        res = await MajorLogin(PyL)
        auth = await DecRypTMajoRLoGin(res)
        LoGinDaTa = await GetLoginData(auth.url, PyL, auth.token)
        dec_data = await DecRypTLoGinDaTa(LoGinDaTa)
        
        OnLineiP, OnLineporT = dec_data.Online_IP_Port.split(":")
        AutHToKen = await xAuThSTarTuP(int(auth.account_uid), auth.token, int(auth.timestamp), auth.key, auth.iv)

        reader, writer = await asyncio.open_connection(OnLineiP, int(OnLineporT))
        writer.write(bytes.fromhex(AutHToKen))
        await writer.drain()

        if action == "apply":
            req_packet = await Apply_Guild_Packet(uid, CLAN_ID, auth.key, auth.iv)
            writer.write(req_packet)
            await writer.drain()
            print(f"📩 [{uid}] Guild join request pathiyeche!")

        writer.close()
        return True
    except: return False

async def main():
    print("🕸️ SPIDER ADVANCED GLORY BOOSTER 🕸️")
    with open(ACCOUNTS_FILE, "r") as f:
        data = json.load(f)
    
    # Sudhu prothom 20ti bot nibe
    bots = [{'uid': b['uid'], 'pwd': b['password']} for b in data[:20]]

    print(f"\n🛡️ Dhap 1: {len(bots)}ti bot theke Guild request pathano hocche...")
    await asyncio.gather(*[process_bot(b, "apply") for b in bots])

    print("\n✅ Request pathano shesh! Game e giye Accept korun.")
    input("\n👉 Accept kora shesh hole ENTER chapun (Match start hobe)...")
    
    print("\n🎮 Dhap 2: Glory farming shuru hocche...")
    # Ekhane match start er logic thakbe...

if __name__ == "__main__":
    asyncio.run(main())
