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

# --- বটের প্রাথমিক তথ্য (Anas SPIDER Configuration) ---
CLAN_ID = "3063703446" 
BOT_UID = "4594650572" 

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- গ্লোবাল ভেরিয়েবল ---
glory_running = False 
glory_task = None
online_writer = None
whisper_writer = None
insquad = None 
joining_team = False 
auto_start_running = False
stop_auto = False
lag_running = False
lag_task = None
evo_cycle_running = False
evo_cycle_task = None
reject_spam_running = False
reject_spam_task = None

# --- ১৬-আইডি গ্লোরি বুস্টার লজিক (Anas Edition) ---
async def anas_spider_glory_booster(key, iv, region):
    global glory_running
    print(f"🚀 [SPIDER] Starting Multi-ID Glory Farming...")
    
    try:
        with open("accounts.json", "r") as f:
            accounts_data = json.load(f)
        uids = list(accounts_data.keys())[:16] 
    except: return print("❌ accounts.json not found!")

    # ধাপ ১: গিল্ড রিকোয়েস্ট পাঠানো
    for target_uid in uids:
        if not glory_running: break
        try:
            req = await SEnd_InV(5, int(target_uid), key, iv, region) 
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', req)
        except: pass
        await asyncio.sleep(1.5)

    # ধাপ ২: ৪টি গ্রুপে ভাগ করে লুপ শুরু
    while glory_running: 
        for i in range(0, 16, 4):
            if not glory_running: break
            group = uids[i:i+4]
            leader = group[0]
            
            try:
                p = await OpEnSq(key, iv, region)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', p)
                c = await cHSq(4, int(leader), key, iv, region)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', c)
                s = await FS(key, iv) 
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', s)
                print(f"🎮 Group {int(i/4)+1} Started. Leader: {leader}")
            except: pass
            
            print(f"🕒 Waiting 60 seconds (Gap)...")
            await asyncio.sleep(60)

# --- হেল্পার ফাংশনসমূহ ---
class MultiAccountManager:
    def __init__(self): self.accounts_file = "accounts.json"
    def load_accounts(self):
        try:
            with open(self.accounts_file, "r") as f: return json.load(f)
        except: return {}

multi_account_manager = MultiAccountManager()

async def safe_send_message(chat_type, message, target_uid, chat_id, key, iv):
    try:
        P = await SEndMsG(chat_type, message, target_uid, chat_id, key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
    except: pass

async def SEndPacKeT(ChaT_W, OnLine_W, TypE, PacKeT):
    if TypE == 'ChaT' and whisper_writer: whisper_writer.write(PacKeT); await whisper_writer.drain()
    elif TypE == 'OnLine' and online_writer: online_writer.write(PacKeT); await online_writer.drain()

def get_random_color():
    return random.choice(["[FF0000]", "[00FF00]", "[0000FF]", "[FFFF00]", "[FF00FF]", "[00FFFF]"])

# --- TCP চ্যাট হ্যান্ডলার (কমান্ড সেন্টার) ---
async def TcPChaT(ip, port, AutHToKen, key, iv, LoGinDaTaUncRypTinG, ready_event, region):
    global glory_running, glory_task, whisper_writer, online_writer
    try:
        reader, writer = await asyncio.open_connection(ip, int(port))
        whisper_writer = writer
        writer.write(bytes.fromhex(AutHToKen)); await writer.drain()
        ready_event.set()
        
        while True:
            data = await reader.read(9999)
            if not data: break
            if data.hex().startswith("120000"):
                response = await DecodeWhisperMessage(data.hex()[10:])
                if response:
                    uid_s = response.Data.uid
                    chat_id = response.Data.Chat_ID
                    msg = response.Data.msg.lower().strip()

                    # --- ANAS SPIDER COMMANDS ---
                    if msg.startswith('/anas_glory'):
                        if not glory_running:
                            glory_running = True
                            glory_task = asyncio.create_task(anas_spider_glory_booster(key, iv, region))
                            await safe_send_message(response.Data.chat_type, "🚀 SPIDER Glory Farming: STARTED (16 IDs Active)", uid_s, chat_id, key, iv)
                        else:
                            await safe_send_message(response.Data.chat_type, "⚠️ Already running, Mama!", uid_s, chat_id, key, iv)

                    elif msg == '/stop_glory':
                        glory_running = False
                        if glory_task: glory_task.cancel()
                        await safe_send_message(response.Data.chat_type, "🛑 SPIDER Glory Farming: STOPPED", uid_s, chat_id, key, iv)

                    elif msg == "/admin":
                        await safe_send_message(response.Data.chat_type, f"👤 Dev: Anas Bhai (SPIDER)\n🏢 Business: FIRE FOX REPAIR\n🎯 Clan ID: {CLAN_ID}", uid_s, chat_id, key, iv)

                    elif msg == "/help":
                        h = "[B][C][00FFFF]--- SPIDER MENU ---\n/anas_glory - Start 16-ID Loop\n/stop_glory - Stop Farming\n/admin - Dev Info\n/exit - Leave Group"
                        await safe_send_message(response.Data.chat_type, h, uid_s, chat_id, key, iv)
    except: pass

async def TcPOnLine(ip, port, key, iv, AutHToKen):
    global online_writer
    while True:
        try:
            reader, writer = await asyncio.open_connection(ip, int(port))
            online_writer = writer
            writer.write(bytes.fromhex(AutHToKen)); await writer.drain()
            while True:
                data = await reader.read(9999)
                if not data: break
        except: await asyncio.sleep(2)

# --- মেইন ফাংশন (Startup) ---
async def MaiiiinE():
    Uid, Pw = BOT_UID, '613E476BB3708A0162637547ED62E058FF637113CE4E555A901D1ED00197BDE3'
    os.system('clear')
    print(render('ANAS', colors=['white', 'cyan'], align='center'))
    
    open_id, access_token = await GeNeRaTeAccEss(Uid, Pw)
    if not open_id: return print("❌ Invalid Account")
    
    PyL = await EncRypTMajoRLoGin(open_id, access_token)
    res = await MajorLogin(PyL)
    auth = await DecRypTMajoRLoGin(res)
    
    LoGinDaTa = await GetLoginData(auth.url, PyL, auth.token)
    dec_data = await DecRypTLoGinDaTa(LoGinDaTa)
    
    OnLineiP, OnLineporT = dec_data.Online_IP_Port.split(":")
    ChaTiP, ChaTporT = dec_data.AccountIP_Port.split(":")
    
    AutHToKen = await xAuThSTarTuP(int(auth.account_uid), auth.token, int(auth.timestamp), auth.key, auth.iv)
    ready_event = asyncio.Event()
    
    asyncio.create_task(TcPChaT(ChaTiP, ChaTporT, AutHToKen, auth.key, auth.iv, dec_data, ready_event, auth.region))
    asyncio.create_task(TcPOnLine(OnLineiP, OnLineporT, auth.key, auth.iv, AutHToKen))  
    
    print(f"🤖 SPIDER BOT ONLINE\n🔹 UID: {auth.account_uid}\n🔹 Status: 🟢 READY")
    await asyncio.Event().wait()

if __name__ == '__main__':
    try: asyncio.run(MaiiiinE())
    except KeyboardInterrupt: sys.exit(0)
