import requests, os, psutil, sys, jwt, pickle, json, binascii, time, urllib3, base64, datetime, re, socket, threading, ssl, pytz, aiohttp
from protobuf_decoder.protobuf_decoder import Parser
from xC4 import * ; from xHeaders import *
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from Pb2 import DEcwHisPErMsG_pb2, MajoRLoGinrEs_pb2, PorTs_pb2, MajoRLoGinrEq_pb2, sQ_pb2, Team_msg_pb2
from cfonts import render, say
from APIS import insta
from flask import Flask, jsonify, request
import asyncio, signal, random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# --- SPIDER Configuration (Anas Bhai - Abu Dhabi) ---
CLAN_ID = "3063703446" # আপনার ক্ল্যান আইডি
BOT_UID = "14942629274" # আপনার লগইন আইডি
PW = '613E476BB3708A0162637547ED62E058FF637113CE4E555A901D1ED00197BDE3'

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- Global Variables ---
glory_running = False 
glory_task = None
online_writer = None
whisper_writer = None
insquad = None 
joining_team = False 
fast_spam_running = False
custom_spam_running = False
spam_request_running = False
lag_running = False
evo_cycle_running = False
reject_spam_running = False

# --- MultiAccount Manager ---
class MultiAccountManager:
    def __init__(self): self.accounts_file = "accounts.json"
    def load_accounts(self):
        try:
            with open(self.accounts_file, "r") as f: return json.load(f)
        except: return {}

multi_account_manager = MultiAccountManager()

# --- ১৬-আইডি গ্লোরি বুস্টার লজিক (Anas Edition) ---
async def anas_spider_glory_booster(key, iv, region):
    global glory_running
    print(f"🚀 [SPIDER] Starting 16-ID Glory Farm for Clan: {CLAN_ID}")
    
    try:
        accounts_data = multi_account_manager.load_accounts()
        uids = list(accounts_data.keys())[:16] # আপনার লিস্টের ১৬টি আইডি
    except Exception as e: 
        print(f"❌ accounts.json error: {e}")
        return

    # ধাপ ১: গিল্ড জয়েন রিকোয়েস্ট পাঠানো
    for target_uid in uids:
        if not glory_running: break
        try:
            req_packet = await SEnd_InV(5, int(target_uid), key, iv, region) 
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', req_packet)
            print(f"✅ Request Sent: {target_uid}")
        except: pass
        await asyncio.sleep(1.5)

    # ধাপ ২: ৪টি গ্রুপে ভাগ করে সিএস (CS) ম্যাচ লুপ শুরু
    while glory_running: 
        for i in range(0, 16, 4):
            if not glory_running: break
            squad_uids = uids[i:i+4]
            leader_uid = squad_uids[0]
            
            try:
                p = await OpEnSq(key, iv, region)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', p)
                
                c = await cHSq(4, int(leader_uid), key, iv, region)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', c)
                
                s = await FS(key, iv) 
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', s)
                print(f"🎮 Group {int(i/4)+1} Started. Leader: {leader_uid}")
            except Exception as e:
                print(f"⚠️ Start error: {e}")
            
            # আপনার রিকোয়েস্ট অনুযায়ী ১ মিনিটের (৬০ সেকেন্ড) বিরতি
            print(f"🕒 Waiting 60 seconds (Anas Request Gap)...")
            await asyncio.sleep(60)

# --- নেটওয়ার্কিং ও হেল্পার ফাংশনসমূহ ---
async def SEndPacKeT(ChaT_W, OnLine_W, TypE, PacKeT):
    try:
        if TypE == 'ChaT' and whisper_writer: 
            whisper_writer.write(PacKeT)
            await whisper_writer.drain()
        elif TypE == 'OnLine' and online_writer: 
            online_writer.write(PacKeT)
            await online_writer.drain()
    except: pass

async def safe_send_message(chat_type, message, target_uid, chat_id, key, iv):
    try:
        P = await SEndMsG(chat_type, message, target_uid, chat_id, key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
    except Exception as e:
        print(f"Error sending message: {e}")

def get_random_color():
    return random.choice(["[FF0000]", "[00FF00]", "[0000FF]", "[FFFF00]", "[FF00FF]", "[00FFFF]"])

async def GeNeRaTeAccEss(uid, password):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    data = {"uid": uid, "password": password, "response_type": "token", "client_type": "2", 
            "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3", "client_id": "100067"}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=Hr, data=data) as response:
            if response.status != 200: return None, None
            try:
                res_json = await response.json()
                return res_json.get("open_id"), res_json.get("access_token")
            except: return None, None

# --- কমান্ড হ্যান্ডলার (TcPChaT) - অরিজিনাল লজিক ---
async def TcPChaT(ip, port, AutHToKen, key, iv, LoGinDaTaUncRypTinG, ready_event, region):
    global glory_running, glory_task, whisper_writer, online_writer
    while True:
        try:
            reader, writer = await asyncio.open_connection(ip, int(port))
            whisper_writer = writer
            writer.write(bytes.fromhex(AutHToKen))
            await writer.drain()
            ready_event.set()
            
            # অরিজিনাল চ্যাট রিড লুপ
            while True:
                data = await reader.read(9999)
                if not data: break
                
                # মেসেজ ডিকোড লজিক
                if data.hex().startswith("120000"):
                    try:
                        msg_decoded = await DeCode_PackEt(data.hex()[10:])
                        response = await DecodeWhisperMessage(data.hex()[10:])
                        
                        if response:
                            uid_s = response.Data.uid
                            chat_id = response.Data.Chat_ID
                            msg_type = response.Data.chat_type
                            inPuTMsG = response.Data.msg.lower().strip()
                            
                            print(f"Received message: {inPuTMsG} from UID: {uid_s} in chat type: {msg_type}")

                            # --- Anas (SPIDER) Commands ---
                            if inPuTMsG.startswith('/anas_glory'):
                                if not glory_running:
                                    glory_running = True
                                    glory_task = asyncio.create_task(anas_spider_glory_booster(key, iv, region))
                                    await safe_send_message(msg_type, "🚀 SPIDER Glory Farm: STARTED (16 IDs Active)", uid_s, chat_id, key, iv)
                                else:
                                    await safe_send_message(msg_type, "⚠️ Already running, Mama!", uid_s, chat_id, key, iv)

                            elif inPuTMsG == '/stop_glory':
                                glory_running = False
                                if glory_task: glory_task.cancel()
                                await safe_send_message(msg_type, "🛑 SPIDER Glory Farm: STOPPED", uid_s, chat_id, key, iv)

                            # --- Basic Commands ---
                            elif inPuTMsG == "/admin":
                                admin_info = """
[C][B][FF0000]╔══════════╗
[FFFFFF]👤 Developer : Anas (SPIDER)
[FFFFFF]🏢 Business  : FIRE FOX REPAIR CAR
[FFFFFF]🎯 Clan ID   : 3063703446
[FF0000]╚══════════╝
"""
                                await safe_send_message(msg_type, admin_info, uid_s, chat_id, key, iv)
                                
                            elif inPuTMsG == "/help":
                                h_menu = """
[B][C][00FFFF]--- SPIDER BOT MENU ---
/anas_glory - Start 16-ID Farming
/stop_glory - Stop Farming Loop
/admin - Developer Info
"""
                                await safe_send_message(msg_type, h_menu, uid_s, chat_id, key, iv)
                                
                            # --- Test Command ---
                            elif inPuTMsG == "/test":
                                await safe_send_message(msg_type, "[B][C][00FF00]✅ Bot is working perfectly, Mama!", uid_s, chat_id, key, iv)

                    except Exception as e:
                        print(f"Error decoding message: {e}")
                        
        except Exception as e: 
            print(f"Chat connection error: {e}")
            whisper_writer = None
            await asyncio.sleep(5)

# --- অনলাইন কানেকশন হ্যান্ডলার ---
async def TcPOnLine(ip, port, key, iv, AutHToKen):
    global online_writer
    while True:
        try:
            reader, writer = await asyncio.open_connection(ip, int(port))
            online_writer = writer
            writer.write(bytes.fromhex(AutHToKen))
            await writer.drain()
            while True:
                data = await reader.read(9999)
                if not data: break
        except: 
            online_writer = None
            await asyncio.sleep(5)

# --- মেইন স্টার্টআপ (MaiiiinE) ---
async def MaiiiinE():
    os.system('clear')
    print(render('ANAS', colors=['white', 'blue'], align='center'))
    print("🕸️ SPIDER BOT INITIALIZING (Abu Dhabi Time)...")

    open_id, access_token = await GeNeRaTeAccEss(BOT_UID, PW)
    if not open_id: 
        print("❌ Login Failed! Check UID/Password.")
        return

    PyL = await EncRypTMajoRLoGin(open_id, access_token)
    res = await MajorLogin(PyL)
    if not res: return print("❌ MajorLogin Error")
    
    auth = await DecRypTMajoRLoGin(res)
    LoGinDaTa = await GetLoginData(auth.url, PyL, auth.token)
    dec_data = await DecRypTLoGinDaTa(LoGinDaTa)
    
    OnLineiP, OnLineporT = dec_data.Online_IP_Port.split(":")
    ChaTiP, ChaTporT = dec_data.AccountIP_Port.split(":")
    
    AutHToKen = await xAuThSTarTuP(int(auth.account_uid), auth.token, int(auth.timestamp), auth.key, auth.iv)
    ready_event = asyncio.Event()
    
    asyncio.create_task(TcPChaT(ChaTiP, ChaTporT, AutHToKen, auth.key, auth.iv, dec_data, ready_event, auth.region))
    asyncio.create_task(TcPOnLine(OnLineiP, OnLineporT, auth.key, auth.iv, AutHToKen))  
    
    print(f"🤖 SPIDER BOT ONLINE\n🔹 UID: {auth.account_uid}\n🔹 Name: {dec_data.AccountName}\n🔹 Status: 🟢 READY")
    await asyncio.Event().wait()

# --- ইমপ্লিমেন্টেশন ---
def start_insta_api():
    try:
        from APIS import insta
        port = 8082
        insta.app.run(host="0.0.0.0", port=port, debug=False)
    except: pass

if __name__ == '__main__':
    try:
        threading.Thread(target=start_insta_api, daemon=True).start()
        asyncio.run(MaiiiinE())
    except KeyboardInterrupt: 
        print("\n🛑 Bot stopped by Anas Bhai.")
        sys.exit(0)
