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
CLAN_ID = "3063703446" 
BOT_UID = "14942629274" 
PW = '613E476BB3708A0162637547ED62E058FF637113CE4E555A901D1ED00197BDE3'

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- Global Variables ---
glory_running = False 
glory_task = None
online_writer = None
whisper_writer = None

# --- MultiAccount Manager ---
class MultiAccountManager:
    def __init__(self): self.accounts_file = "accounts.json"
    def load_accounts(self):
        try:
            with open(self.accounts_file, "r") as f: return json.load(f)
        except: return {}

multi_account_manager = MultiAccountManager()

# --- অটো-স্টার্ট গ্লোরি বুস্টার (REAL LOGIN & WAIT EDITION) ---
async def anas_spider_glory_booster():
    global glory_running
    print(f"\n{'='*50}")
    print(f"🚀 [SPIDER AUTO-START] REAL Glory Farm Activated!")
    print(f"{'='*50}\n")
    
    try:
        accounts_data = multi_account_manager.load_accounts()
        if not accounts_data:
            print("❌ Error: accounts.json is empty or not found!")
            return
    except Exception as e: 
        print(f"❌ accounts.json error: {e}")
        return

    while glory_running:
        print(f"\n🔄 Starting new CS Match Cycle for Slave IDs...")
        
        for uid, password in accounts_data.items():
            if not glory_running: break
            
            # মেইন বট আইডি স্কিপ করা হচ্ছে 
            if str(uid) == BOT_UID:
                continue
                
            print(f"🔐 Logging into Slave ID: {uid}...")
            try:
                open_id, access_token = await GeNeRaTeAccEss(uid, password)
                if not open_id: 
                    print(f"❌ Login failed for {uid}")
                    continue
                
                PyL = await EncRypTMajoRLoGin(open_id, access_token)
                res = await MajorLogin(PyL)
                if not res: continue
                
                auth = await DecRypTMajoRLoGin(res)
                LoGinDaTa = await GetLoginData(auth.url, PyL, auth.token)
                dec_data = await DecRypTLoGinDaTa(LoGinDaTa)
                
                OnLineiP, OnLineporT = dec_data.Online_IP_Port.split(":")
                AutHToKen = await xAuThSTarTuP(int(auth.account_uid), auth.token, int(auth.timestamp), auth.key, auth.iv)
                
                slave_reader, slave_writer = await asyncio.open_connection(OnLineiP, int(OnLineporT))
                
                # ১. Auth প্যাকেট পাঠানো এবং রেসপন্স রিড করা
                slave_writer.write(bytes.fromhex(AutHToKen))
                await slave_writer.drain()
                await slave_reader.read(4096) 
                await asyncio.sleep(1.5) 
                
                # ২. স্কোয়াড তৈরি
                p = await OpEnSq(auth.key, auth.iv, auth.region)
                slave_writer.write(p)
                await slave_writer.drain()
                await slave_reader.read(4096) 
                await asyncio.sleep(1.5)
                
                # ৩. ম্যাচ স্টার্ট (FS) প্যাকেট পাঠানো
                s = await FS(auth.key, auth.iv) 
                slave_writer.write(s)
                await slave_writer.drain()
                
                print(f"🎮 Match Start Packet Sent for UID: {uid}. Holding connection...")
                
                # ম্যাচ স্টার্ট হওয়ার জন্য ৮ সেকেন্ড অপেক্ষা
                await asyncio.sleep(8) 
                
                slave_writer.close()
                await slave_writer.wait_closed()
                print(f"✅ CS Match Started Successfully for UID: {uid}")
                
            except Exception as e:
                print(f"⚠️ Error with UID {uid}: {e}")
            
            # এক আইডি থেকে অন্য আইডির মাঝে ৫ সেকেন্ড গ্যাপ
            await asyncio.sleep(5) 
            
        print(f"🕒 IDs processed! Waiting 60 seconds before next round...")
        await asyncio.sleep(60)

# --- নেটওয়ার্কিং ফাংশনসমূহ ---
async def SEndPacKeT(ChaT_W, OnLine_W, TypE, PacKeT):
    try:
        if TypE == 'ChaT' and whisper_writer: 
            whisper_writer.write(PacKeT); await whisper_writer.drain()
        elif TypE == 'OnLine' and online_writer: 
            online_writer.write(PacKeT); await online_writer.drain()
    except: pass

async def safe_send_message(chat_type, message, target_uid, chat_id, key, iv):
    try:
        P = await SEndMsG(chat_type, message, target_uid, chat_id, key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
    except: pass

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

# --- কমান্ড হ্যান্ডলার (TcPChaT) ---
async def TcPChaT(ip, port, AutHToKen, key, iv, LoGinDaTaUncRypTinG, ready_event, region):
    global whisper_writer
    while True:
        try:
            reader, writer = await asyncio.open_connection(ip, int(port))
            whisper_writer = writer
            writer.write(bytes.fromhex(AutHToKen))
            await writer.drain()
            ready_event.set()

            if LoGinDaTaUncRypTinG.Clan_ID:
                clan_id = LoGinDaTaUncRypTinG.Clan_ID
                clan_compiled_data = LoGinDaTaUncRypTinG.Clan_Compiled_Data
                print(f'\n - TarGeT BoT in CLan ! \n - Clan Uid > {clan_id}')
                try:
                    pK = await AuthClan(clan_id, clan_compiled_data, key, iv)
                    writer.write(pK); await writer.drain()
                except: pass
            
            while True:
                data = await reader.read(9999)
                if not data: 
                    # 🛑 স্প্যাম থামানোর ফিক্স 🛑
                    print("⚠️ Chat Connection closed. Reconnecting in 5s...")
                    await asyncio.sleep(5) 
                    break
                
                if data.hex().startswith("120000"):
                    try:
                        response = await DecodeWhisperMessage(data.hex()[10:])
                        if response:
                            msg_type = response.Data.chat_type
                            inPuTMsG = response.Data.msg.lower().strip()
                            # Commands
                            if inPuTMsG == "/admin":
                                await safe_send_message(msg_type, "👤 Dev: Anas (SPIDER)", response.Data.uid, response.Data.Chat_ID, key, iv)
                    except: pass
                        
        except Exception as e: 
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
                if not data: 
                    await asyncio.sleep(5)
                    break
        except: 
            online_writer = None
            await asyncio.sleep(5)

# --- মেইন স্টার্টআপ ---
async def MaiiiinE():
    global glory_running, glory_task
    
    os.system('clear')
    print(render('ANAS', colors=['white', 'blue'], align='center'))
    print("🕸️ SPIDER BOT INITIALIZING...")

    open_id, access_token = await GeNeRaTeAccEss(BOT_UID, PW)
    if not open_id: 
        return print("❌ Login Failed! Check UID/Password.")

    PyL = await EncRypTMajoRLoGin(open_id, access_token)
    res = await MajorLogin(PyL)
    if not res: return
    
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
    
    # 🛑 অটো স্টার্ট ফিক্স (আর চ্যাটের জন্য অপেক্ষা করবে না) 🛑
    print("\n⏳ Auto Glory Farm will start in 10 seconds. Please wait...")
    await asyncio.sleep(10) 
    
    glory_running = True
    glory_task = asyncio.create_task(anas_spider_glory_booster()) 
    
    await asyncio.Event().wait()

if __name__ == '__main__':
    try: asyncio.run(MaiiiinE())
    except KeyboardInterrupt: sys.exit(0)
