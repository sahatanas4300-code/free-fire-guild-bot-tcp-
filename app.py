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

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- Global Variables ---
online_writer = None
whisper_writer = None
spam_room = False
spammer_uid = None
spam_chat_id = None
spam_uid = None
Spy = False
Chat_Leave = False
fast_spam_running = False
fast_spam_task = None
custom_spam_running = False
custom_spam_task = None
spam_request_running = False
spam_request_task = None
evo_fast_spam_running = False
evo_fast_spam_task = None
evo_custom_spam_running = False
evo_custom_spam_task = None
reject_spam_running = False
insquad = None 
joining_team = False 
reject_spam_task = None
lag_running = False
lag_task = None
evo_cycle_running = False
evo_cycle_task = None
auto_start_running = False
auto_start_teamcode = None
stop_auto = False
auto_start_task = None
start_spam_duration = 18
wait_after_match = 20
start_spam_delay = 0.2

# --- SPIDER GLORY BOOSTER VARIABLES ---
glory_running = False
glory_task = None

evo_emotes = {
    "1": "909000063", "2": "909000068", "3": "909000075", "4": "909040010",
    "5": "909000081", "6": "909039011", "7": "909000085", "8": "909000090",
    "9": "909000098", "10": "909035007", "11": "909042008", "12": "909041005",
    "13": "909033001", "14": "909038010", "15": "909038012", "16": "909045001",
    "17": "909049010", "18": "909051003"
}

EMOTE_MAP = {
    1: 909000063, 2: 909000081, 3: 909000075, 4: 909000085, 5: 909000134,
    6: 909000098, 7: 909035007, 8: 909051012, 9: 909000141, 10: 909034008,
    11: 909051015, 12: 909041002, 13: 909039004, 14: 909042008, 15: 909051014,
    16: 909039012, 17: 909040010, 18: 909035010, 19: 909041005, 20: 909051003,
    21: 909034001
}

BADGE_VALUES = {
    "s1": 1048576, "s2": 32768, "s3": 2048, "s4": 64, "s5": 262144
}

def start_insta_api():
    port = insta.find_free_port()
    print(f"🚀 Starting Insta API on port {port}")
    insta.app.run(host="0.0.0.0", port=port, debug=False)

def dec_to_hex(decimal):
    hex_str = hex(decimal)[2:]
    return hex_str.upper() if len(hex_str) % 2 == 0 else '0' + hex_str.upper()

async def encrypt_packet(packet_hex, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    packet_bytes = bytes.fromhex(packet_hex)
    padded_packet = pad(packet_bytes, AES.block_size)
    encrypted = cipher.encrypt(padded_packet)
    return encrypted.hex()

async def nmnmmmmn(packet_hex, key, iv):
    return await encrypt_packet(packet_hex, key, iv)

def get_idroom_by_idplayer(packet_hex):
    try:
        json_result = get_available_room(packet_hex)
        parsed_data = json.loads(json_result)
        json_data = parsed_data["5"]["data"]
        data = json_data["1"]["data"]
        return data['15']["data"]
    except: return None

async def check_player_in_room(target_uid, key, iv):
    try:
        status_packet = await GeT_Status(int(target_uid), key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', status_packet)
        return True
    except: return False

class MultiAccountManager:
    def __init__(self):
        self.accounts_file = "accounts.json"
    
    def load_accounts(self):
        try:
            with open(self.accounts_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except: return {}
    
    async def get_account_token(self, uid, password):
        try:
            url = "https://100067.connect.garena.com/oauth/guest/token/grant"
            headers = {
                "Host": "100067.connect.garena.com",
                "User-Agent": await Ua(),
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "close"
            }
            data = {
                "uid": uid, "password": password, "response_type": "token",
                "client_type": "2", "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
                "client_id": "100067"
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, data=data) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("open_id"), data.get("access_token")
            return None, None
        except: return None, None

multi_account_manager = MultiAccountManager()

# =========================================================================
# --- AUTO GLORY BOOSTER LOGIC ---
# =========================================================================
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

    print("⏳ Auto Glory Farm waiting 10 seconds for main bot to stabilize...")
    await asyncio.sleep(10)

    while glory_running:
        print(f"\n🔄 Starting new CS Match Cycle for Slave IDs...")
        
        for acc_uid, password in accounts_data.items():
            if not glory_running: break
            
            # Skipping main bot IDs to prevent conflicts
            if str(acc_uid) in ["4594650572", "14942629274", "13699776666", "14009897329"]:
                continue
                
            print(f"🔐 Logging into Slave ID: {acc_uid}...")
            try:
                open_id, access_token = await multi_account_manager.get_account_token(acc_uid, password)
                if not open_id: 
                    print(f"❌ Login failed for {acc_uid}")
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
                
                slave_writer.write(bytes.fromhex(AutHToKen))
                await slave_writer.drain()
                await slave_reader.read(4096) 
                await asyncio.sleep(1.5) 
                
                try:
                    p = await OpEnSq(auth.key, auth.iv, auth.region)
                    if isinstance(p, str): p = bytes.fromhex(p)
                    slave_writer.write(p)
                    await slave_writer.drain()
                    await slave_reader.read(4096) 
                    await asyncio.sleep(1.5)
                except: pass
                
                try:
                    s = await FS(auth.key, auth.iv) 
                    if isinstance(s, str): s = bytes.fromhex(s)
                    slave_writer.write(s)
                    await slave_writer.drain()
                except: pass
                
                print(f"🎮 Match Start Packet Sent for UID: {acc_uid}. Holding connection 8s...")
                await asyncio.sleep(8) 
                
                slave_writer.close()
                await slave_writer.wait_closed()
                print(f"✅ CS Match Started Successfully for UID: {acc_uid}")
                
            except Exception as e:
                print(f"⚠️ Error with UID {acc_uid}: {e}")
            
            await asyncio.sleep(5) 
            
        print(f"🕒 IDs processed! Waiting 60 seconds before next round...")
        await asyncio.sleep(60)

async def SEnd_InV_with_Cosmetics(Nu, Uid, K, V, region):
    region = "ind"
    fields = {
        1: 2, 
        2: {
            1: int(Uid), 
            2: region, 
            4: int(Nu),
            5: {
                1: "BOT",                    
                2: int(await get_random_avatar()),     
                5: random.choice([1048576, 32768, 2048]),  
            }
        }
    }

    if region.lower() == "ind":
        packet = '0514'
    elif region.lower() == "bd":
        packet = "0519"
    else:
        packet = "0515"
        
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet, K, V)   
            
async def join_custom_room(room_id, room_password, key, iv, region):
    fields = {
        1: 61, 
        2: {
            1: int(room_id),
            2: {
                1: int(room_id),  
                2: int(time.time()),  
                3: "BOT",  
                5: 12,  
                6: 9999999,  
                7: 1,  
                8: {
                    2: 1,
                    3: 1,
                },
                9: 3,  
            },
            3: str(room_password),  
        }
    }
    
    if region.lower() == "ind": packet_type = '0514'
    elif region.lower() == "bd": packet_type = "0519"
    else: packet_type = "0515"
        
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet_type, key, iv)
    
async def leave_squad(key, iv, region):
    fields = {
        1: 7,
        2: {
            1: 12480598706  
        }
    }
    
    packet = (await CrEaTe_ProTo(fields)).hex()
    
    if region.lower() == "ind": packet_type = '0514'
    elif region.lower() == "bd": packet_type = "0519"
    else: packet_type = "0515"
        
    return await GeneRaTePk(packet, packet_type, key, iv)    
    
async def RedZed_SendInv(bot_uid, uid, key, iv):
    try:
        fields = {
            1: 33, 
            2: {
                1: int(uid), 2: "IND", 3: 1, 4: 1, 6: "sm!!", 7: 330, 8: 1000, 9: 100, 10: "DZ", 
                12: 1, 13: int(uid), 16: 1, 17: {2: 159, 4: "y[WW", 6: 11, 8: "2.121.2", 9: 3, 10: 1}, 
                18: 306, 19: 18, 24: 902000306, 26: {}, 27: {1: 11, 2: int(bot_uid), 3: 99999999999}, 
                28: {}, 31: {1: 1, 2: 32768}, 32: 32768, 
                34: {1: bot_uid, 2: 8, 3: b"\x10\x15\x08\x0A\x0B\x13\x0C\x0F\x11\x04\x07\x02\x03\x0D\x0E\x12\x01\x05\x06"}
            }
        }
        packet = await CrEaTe_ProTo(fields)
        return await GeneRaTePk(packet.hex(), '0515', key, iv)
    except Exception as e:
        print(f"❌ Error in RedZed_SendInv: {e}")
        return None
    
async def request_join_with_badge(target_uid, badge_value, key, iv, region):
    fields = {
        1: 33,
        2: {
            1: int(target_uid), 2: region.upper(), 3: 1, 4: 1,
            5: bytes([1, 7, 9, 10, 11, 18, 25, 26, 32]), 6: "iG:[C][B][FF0000] SM", 7: 330, 8: 1000, 10: region.upper(),
            11: bytes([49, 97, 99, 52, 98, 56, 48, 101, 99, 102, 48, 52, 55, 56, 97, 52, 52, 50, 48, 51, 98, 102, 56, 102, 97, 99, 54, 49, 50, 48, 102, 53]),
            12: 1, 13: int(target_uid), 
            14: {1: 2203434355, 2: 8, 3: "\u0010\u0015\b\n\u000b\u0013\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"},
            16: 1, 17: 1, 18: 312, 19: 46, 23: bytes([16, 1, 24, 1]), 24: int(await get_random_avatar()), 26: "", 28: "",
            31: {1: 1, 2: badge_value}, 32: badge_value, 
            34: {1: int(target_uid), 2: 8, 3: bytes([15,6,21,8,10,11,19,12,17,4,14,20,7,2,1,5,16,3,13,18])}
        },
        10: "en", 13: {2: 1, 3: 1}
    }
    packet = (await CrEaTe_ProTo(fields)).hex()
    if region.lower() == "ind": packet_type = '0514'
    elif region.lower() == "bd": packet_type = "0519"
    else: packet_type = "0515"
    return await GeneRaTePk(packet, packet_type, key, iv)    
    
async def start_auto_packet(key, iv, region):
    fields = {1: 9, 2: {1: 12480598706}}
    if region.lower() == "ind": packet_type = '0514'
    elif region.lower() == "bd": packet_type = "0519"
    else: packet_type = "0515"
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet_type, key, iv)

async def leave_squad_packet(key, iv, region):
    fields = {1: 7, 2: {1: 12480598706}}
    if region.lower() == "ind": packet_type = '0514'
    elif region.lower() == "bd": packet_type = "0519"
    else: packet_type = "0515"
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet_type, key, iv)

async def join_teamcode_packet(team_code, key, iv, region):
    fields = {
        1: 4, 
        2: {
            4: bytes.fromhex("01090a0b121920"), 5: str(team_code), 6: 6, 8: 1,
            9: {2: 800, 6: 11, 8: "1.111.1", 9: 5, 10: 1}
        }
    }
    if region.lower() == "ind": packet_type = '0514'
    elif region.lower() == "bd": packet_type = "0519"
    else: packet_type = "0515"
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet_type, key, iv)
    
async def auto_start_loop(team_code, uid, chat_id, chat_type, key, iv, region):
    global auto_start_running, stop_auto
    print(f"[AUTO] Auto start loop started for team {team_code}")
    while not stop_auto:
        try:
            status_msg = f"[B][C][FFA500]🤖 Auto Start Bot\n🎯 Team: {team_code}\n⚡ Joining team..."
            await safe_send_message(chat_type, status_msg, uid, chat_id, key, iv)
            join_packet = await join_teamcode_packet(team_code, key, iv, region)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
            await asyncio.sleep(2)
            
            start_msg = f"[B][C][00FF00]✅ Joined team {team_code}\n🎯 Starting match for {start_spam_duration} seconds..."
            await safe_send_message(chat_type, start_msg, uid, chat_id, key, iv)
            
            start_packet = await start_auto_packet(key, iv, region)
            end_time = time.time() + start_spam_duration
            
            while time.time() < end_time and not stop_auto:
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', start_packet)
                await asyncio.sleep(start_spam_delay)
            
            if stop_auto: break
            
            wait_msg = f"[B][C][FFFF00]⏳ Match started! Bot in lobby waiting {wait_after_match} seconds..."
            await safe_send_message(chat_type, wait_msg, uid, chat_id, key, iv)
            
            waited = 0
            while waited < wait_after_match and not stop_auto:
                await asyncio.sleep(1)
                waited += 1
            
            if stop_auto: break
            
            leave_msg = f"[B][C][FF0000]🔄 Leaving team {team_code} to rejoin and start again..."
            await safe_send_message(chat_type, leave_msg, uid, chat_id, key, iv)
            leave_packet = await leave_squad_packet(key, iv, region)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', leave_packet)
            await asyncio.sleep(2)
            
        except Exception as e:
            error_msg = f"[B][C][FF0000]❌ Auto start error: {str(e)}\n"
            await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)
            break
    
    auto_start_running = False
    stop_auto = False
    print(f"[AUTO] Auto start loop stopped for team {team_code}")
    
async def reset_bot_state(key, iv, region):
    try:
        leave_packet = await leave_squad(key, iv, region)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', leave_packet)
        await asyncio.sleep(0.5)
        return True
    except Exception as e:
        return False    
    
async def create_custom_room(room_name, room_password, max_players, key, iv, region):
    fields = {
        1: 3, 
        2: {
            1: room_name, 2: room_password, 3: max_players, 4: 1, 5: 1, 6: "en", 
            7: {1: "BotHost", 2: int(await get_random_avatar()), 3: 330, 4: 1048576, 5: "BOTCLAN"}
        }
    }
    if region.lower() == "ind": packet_type = '0514'
    elif region.lower() == "bd": packet_type = "0519"
    else: packet_type = "0515"
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet_type, key, iv)              

async def real_multi_account_join(target_uid, key, iv, region):
    try:
        accounts_data = multi_account_manager.load_accounts()
        if not accounts_data: return 0, 0
        
        success_count = 0
        total_accounts = len(accounts_data)
        
        for account_uid, password in accounts_data.items():
            try:
                open_id, access_token = await multi_account_manager.get_account_token(account_uid, password)
                if not open_id or not access_token: continue
                join_packet = await SEnd_InV(5, int(target_uid), key, iv, region)
                if join_packet:
                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
                    success_count += 1
                await asyncio.sleep(2)
            except: continue
        return success_count, total_accounts
    except: return 0, 0

async def handle_badge_command(cmd, inPuTMsG, uid, chat_id, key, iv, region, chat_type):
    parts = inPuTMsG.strip().split()
    if len(parts) < 2:
        return
    
    target_uid = parts[1]
    badge_value = BADGE_VALUES.get(cmd, 1048576)
    
    if not target_uid.isdigit():
        return
    
    initial_msg = f"[B][C][1E90FF]🌀 Request received! Preparing to spam {target_uid}...\n"
    await safe_send_message(chat_type, initial_msg, uid, chat_id, key, iv)
    
    try:
        await reset_bot_state(key, iv, region)
        join_packet = await request_join_with_badge(target_uid, badge_value, key, iv, region)
        
        for i in range(3):
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
            await asyncio.sleep(0.1)
        
        success_msg = f"[B][C][00FF00]✅ Successfully Sent 3 Join Requests!\n🎯 Target: {target_uid}\n🏷️ Badge: {badge_value}\n"
        await safe_send_message(chat_type, success_msg, uid, chat_id, key, iv)
        await asyncio.sleep(1)
        await reset_bot_state(key, iv, region)
    except Exception as e:
        pass

async def auto_rings_emote_dual(sender_uid, key, iv, region):
    try:
        rings_emote_id = 909050009
        bot_uid = 13699776666
        emote_to_sender = await Emote_k(int(sender_uid), rings_emote_id, key, iv, region)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', emote_to_sender)
        await asyncio.sleep(0.5)
        emote_to_bot = await Emote_k(int(bot_uid), rings_emote_id, key, iv, region)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', emote_to_bot)
    except Exception as e:
        print(f"Error sending dual rings emote: {e}")    
        
async def Room_Spam(Uid, Rm, Nm, K, V):
    same_value = random.choice([32768])  
    fields = {
        1: 78,
        2: {
            1: int(Rm), 2: "iG:[C][B][FF0000] SM", 3: {2: 1, 3: 1}, 4: 330, 5: 6000, 6: 201, 10: int(await get_random_avatar()),  
            11: int(Uid), 12: 1, 15: {1: 1, 2: same_value}, 16: same_value, 
            18: {1: 11481904755, 2: 8, 3: "\u0010\u0015\b\n\u000b\u0013\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"},
            31: {1: 1, 2: same_value}, 32: same_value, 
            34: {1: int(Uid), 2: 8, 3: bytes([15,6,21,8,10,11,19,12,17,4,14,20,7,2,1,5,16,3,13,18])}
        }
    }
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '0e15', K, V)
async def evo_cycle_spam(uids, key, iv, region):
    global evo_cycle_running
    cycle_count = 0
    while evo_cycle_running:
        cycle_count += 1
        for emote_number, emote_id in evo_emotes.items():
            if not evo_cycle_running: break
            for uid in uids:
                try:
                    H = await Emote_k(int(uid), int(emote_id), key, iv, region)
                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                except: pass
            if evo_cycle_running:
                for i in range(5):
                    if not evo_cycle_running: break
                    await asyncio.sleep(1)
        if evo_cycle_running: await asyncio.sleep(2)

async def reject_spam_loop(target_uid, key, iv):
    global reject_spam_running
    count = 0
    while reject_spam_running and count < 150:
        try:
            packet1 = await banecipher1(target_uid, key, iv)
            packet2 = await banecipher(target_uid, key, iv)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', packet1)
            await asyncio.sleep(0.1)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', packet2)
            count += 1
            await asyncio.sleep(0.2)
        except: break
    return count    

async def handle_reject_completion(spam_task, target_uid, sender_uid, chat_id, chat_type, key, iv):
    try:
        spam_count = await spam_task
        completion_msg = f"[B][C][00FF00]✅ Reject Spam Completed for ID {target_uid}\n"
        await safe_send_message(chat_type, completion_msg, sender_uid, chat_id, key, iv)
    except: pass

async def banecipher(client_id, key, iv):
    banner_text = "SPAM\n" * 10
    fields = {1: 5, 2: {1: int(client_id), 2: 1, 3: int(client_id), 4: banner_text}}
    packet = await CrEaTe_ProTo(fields)
    encrypted_packet = await EnC_PacKeT(packet.hex(), key, iv)
    header_length = len(encrypted_packet) // 2
    header_length_final = await DecodE_HeX(header_length)
    if len(header_length_final) == 2: final_packet = "0515000000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 3: final_packet = "051500000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 4: final_packet = "05150000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 5: final_packet = "0515000" + header_length_final + encrypted_packet
    else: final_packet = "0515000000" + header_length_final + encrypted_packet
    return bytes.fromhex(final_packet)

async def banecipher1(client_id, key, iv):
    gay_text = "SPAM\n" * 10
    fields = {1: int(client_id), 2: 5, 4: 50, 5: {1: int(client_id), 2: gay_text}}
    packet = await CrEaTe_ProTo(fields)
    encrypted_packet = await EnC_PacKeT(packet.hex(), key, iv)
    header_length = len(encrypted_packet) // 2
    header_length_final = await DecodE_HeX(header_length)
    if len(header_length_final) == 2: final_packet = "0515000000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 3: final_packet = "051500000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 4: final_packet = "05150000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 5: final_packet = "0515000" + header_length_final + encrypted_packet
    else: final_packet = "0515000000" + header_length_final + encrypted_packet
    return bytes.fromhex(final_packet)

async def lag_team_loop(team_code, key, iv, region):
    global lag_running
    start_time = time.time()
    while lag_running:
        if time.time() - start_time > 20:
            lag_running = False
            break
        try:
            join_packet = await GenJoinSquadsPacket(team_code, key, iv)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
            await asyncio.sleep(0.01)
            leave_packet = await ExiT(None, key, iv)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', leave_packet)
            await asyncio.sleep(0.01)
        except: await asyncio.sleep(0.1)

# API Functions
def Get_clan_info(clan_id):
    try:
        url = f"https://get-clan-info.vercel.app/get_clan_info?clan_id={clan_id}"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            return f"Clan Name : {data['clan_name']}\nLevel : {data['level']}\nMembers : {data['guild_details']['total_members']}"
        return "Failed to get clan info"
    except: return "Error fetching info"

def get_player_bio(uid):
    try:
        url = f"https://info-wotaxxdev-api.vercel.app/info?uid={uid}"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            bio = data.get('socialInfo', {}).get('signature', "No bio available")
            return bio
        return "Failed to fetch bio"
    except Exception as e: return str(e)

def talk_with_ai(question):
    try:
        url = f"https://aashish-ai-api.vercel.app/ask?key=AASHISH65&message={question}"
        res = requests.get(url)
        if res.status_code == 200: return res.json()["message"]["content"]
        return "Error connecting to AI server."
    except: return "API Error"

def send_likes(uid):
    try:
        server2 = "bd"
        BYPASS_TOKEN = "your_token_here"
        url = f"https://yourlikeapi/like?uid={uid}&server_name={server2}&x-vercel-set-bypass-cookie=true&x-vercel-protection-bypass={BYPASS_TOKEN}"
        res = requests.get(url, timeout=15)
        if res.status_code == 200:
            data = res.json()
            if data.get('status') == 1:
                return f"✅ Likes sent to {data.get('PlayerNickname')}"
            return f"❌ Already maxed or failed."
        return "Like API Error"
    except: return "Like API Connection Failed"

Hr = {
    'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)",
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'Content-Type': "application/x-www-form-urlencoded",
    'Expect': "100-continue",
    'X-Unity-Version': "2018.4.11f1",
    'X-GA': "v1 1",
    'ReleaseVersion': '1.120.2'}

def get_random_color():
    colors = ["[FF0000]", "[00FF00]", "[0000FF]", "[FFFF00]", "[FF00FF]", "[00FFFF]", "[FFFFFF]", "[FFA500]"]
    return random.choice(colors)

async def get_random_avatar():
    await asyncio.sleep(0) 
    avatar_list = ['902050001', '902050002', '902050003', '902039016']
    return random.choice(avatar_list)
    
async def ultra_quick_emote_attack(team_code, emote_id, target_uid, key, iv, region):
    try:
        join_packet = await GenJoinSquadsPacket(team_code, key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
        await asyncio.sleep(1.5) 
        emote_packet = await Emote_k(int(target_uid), int(emote_id), key, iv, region)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', emote_packet)
        await asyncio.sleep(0.5)
        leave_packet = await ExiT(None, key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', leave_packet)
        return True, "Done"
    except Exception as e: return False, str(e)
        
async def encrypted_proto(encoded_hex):
    key = b'Yg&tc%DEuh6%Zc^8'
    iv = b'6oyZDr22E3ychjM%'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(encoded_hex, AES.block_size)
    encrypted_payload = cipher.encrypt(padded_message)
    return encrypted_payload
    
async def GeNeRaTeAccEss(uid , password):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    headers = {
        "Host": "100067.connect.garena.com",
        "User-Agent": (await Ua()),
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close"}
    data = {
        "uid": uid, "password": password, "response_type": "token",
        "client_type": "2", "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067"}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=Hr, data=data) as response:
            if response.status != 200: return None, None
            data = await response.json()
            return data.get("open_id"), data.get("access_token")

async def EncRypTMajoRLoGin(open_id, access_token):
    major_login = MajoRLoGinrEq_pb2.MajorLogin()
    major_login.event_time = str(datetime.now())[:-7]
    major_login.game_name = "free fire"
    major_login.platform_id = 1
    major_login.client_version = "1.120.2"
    major_login.system_software = "Android OS 9 / API-28"
    major_login.open_id = open_id
    major_login.open_id_type = "4"
    major_login.access_token = access_token
    string = major_login.SerializeToString()
    return await encrypted_proto(string)

async def MajorLogin(payload):
    url = "https://loginbp.ggblueshark.com/MajorLogin"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200: return await response.read()
            return None

async def GetLoginData(base_url, payload, token):
    url = f"{base_url}/GetLoginData"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    Hr['Authorization']= f"Bearer {token}"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200: return await response.read()
            return None

async def DecRypTMajoRLoGin(MajoRLoGinResPonsE):
    proto = MajoRLoGinrEs_pb2.MajorLoginRes()
    proto.ParseFromString(MajoRLoGinResPonsE)
    return proto

async def DecRypTLoGinDaTa(LoGinDaTa):
    proto = PorTs_pb2.GetLoginData()
    proto.ParseFromString(LoGinDaTa)
    return proto

async def DecodeWhisperMessage(hex_packet):
    packet = bytes.fromhex(hex_packet)
    proto = DEcwHisPErMsG_pb2.DecodeWhisper()
    proto.ParseFromString(packet)
    return proto
    
async def decode_team_packet(hex_packet):
    packet = bytes.fromhex(hex_packet)
    proto = sQ_pb2.recieved_chat()
    proto.ParseFromString(packet)
    return proto
    
async def xAuThSTarTuP(TarGeT, token, timestamp, key, iv):
    uid_hex = hex(TarGeT)[2:]
    uid_length = len(uid_hex)
    encrypted_timestamp = await DecodE_HeX(timestamp)
    encrypted_account_token = token.encode().hex()
    encrypted_packet = await EnC_PacKeT(encrypted_account_token, key, iv)
    encrypted_packet_length = hex(len(encrypted_packet) // 2)[2:]
    if uid_length == 9: headers = '0000000'
    elif uid_length == 8: headers = '00000000'
    elif uid_length == 10: headers = '000000'
    elif uid_length == 7: headers = '000000000'
    else: headers = '0000000'
    return f"0115{headers}{uid_hex}{encrypted_timestamp}00000{encrypted_packet_length}{encrypted_packet}"
     
async def cHTypE(H):
    if not H: return 'Squid'
    elif H == 1: return 'CLan'
    elif H == 2: return 'PrivaTe'
    
async def SEndMsG(H , message , Uid , chat_id , key , iv):
    TypE = await cHTypE(H)
    if TypE == 'Squid': msg_packet = await xSEndMsgsQ(message , chat_id , key , iv)
    elif TypE == 'CLan': msg_packet = await xSEndMsg(message , 1 , chat_id , chat_id , key , iv)
    elif TypE == 'PrivaTe': msg_packet = await xSEndMsg(message , 2 , Uid , Uid , key , iv)
    return msg_packet

async def SEndPacKeT(OnLinE , ChaT , TypE , PacKeT):
    if TypE == 'ChaT' and ChaT: whisper_writer.write(PacKeT) ; await whisper_writer.drain()
    elif TypE == 'OnLine': online_writer.write(PacKeT) ; await online_writer.drain()

async def safe_send_message(chat_type, message, target_uid, chat_id, key, iv, max_retries=3):
    for attempt in range(max_retries):
        try:
            P = await SEndMsG(chat_type, message, target_uid, chat_id, key, iv)
            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
            return True
        except:
            if attempt < max_retries - 1: await asyncio.sleep(0.5)
    return False

async def fast_emote_spam(uids, emote_id, key, iv, region):
    global fast_spam_running
    count = 0
    while fast_spam_running and count < 25:
        for uid in uids:
            try:
                H = await Emote_k(int(uid), int(emote_id), key, iv, region)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
            except: pass
        count += 1
        await asyncio.sleep(0.1)

async def custom_emote_spam(uid, emote_id, times, key, iv, region):
    global custom_spam_running
    count = 0
    while custom_spam_running and count < times:
        try:
            H = await Emote_k(int(uid), int(emote_id), key, iv, region)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
            count += 1
            await asyncio.sleep(0.1)
        except: break

async def spam_request_loop_with_cosmetics(target_uid, key, iv, region):
    global spam_request_running
    count = 0
    badge_rotation = [1048576, 32768, 2048, 64, 4094, 11233, 262144]
    while spam_request_running and count < 30:
        try:
            current_badge = badge_rotation[count % len(badge_rotation)]
            PAc = await OpEnSq(key, iv, region)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', PAc)
            await asyncio.sleep(0.2)
            C = await cHSq(5, int(target_uid), key, iv, region)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', C)
            await asyncio.sleep(0.2)
            V = await SEnd_InV_With_Cosmetics(5, int(target_uid), key, iv, region, current_badge)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', V)
            E = await ExiT(None, key, iv)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', E)
            count += 1
            await asyncio.sleep(0.5)
        except: await asyncio.sleep(0.5)
    return count
            
async def evo_emote_spam(uids, number, key, iv, region):
    try:
        emote_id = EMOTE_MAP.get(int(number))
        if not emote_id: return False, "Invalid number! Use 1-21 only."
        success_count = 0
        for uid in uids:
            try:
                H = await Emote_k(int(uid), emote_id, key, iv, region)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                success_count += 1
                await asyncio.sleep(0.1)
            except: pass
        return True, f"Sent to {success_count} player(s)"
    except Exception as e: return False, str(e)

async def evo_fast_emote_spam(uids, number, key, iv, region):
    global evo_fast_spam_running
    count = 0
    emote_id = EMOTE_MAP.get(int(number))
    if not emote_id: return False, "Invalid number!"
    while evo_fast_spam_running and count < 25:
        for uid in uids:
            try:
                H = await Emote_k(int(uid), emote_id, key, iv, region)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
            except: pass
        count += 1
        await asyncio.sleep(0.1)
    return True, "Done"

async def evo_custom_emote_spam(uids, number, times, key, iv, region):
    global evo_custom_spam_running
    count = 0
    emote_id = EMOTE_MAP.get(int(number))
    if not emote_id: return False, "Invalid number!"
    while evo_custom_spam_running and count < times:
        for uid in uids:
            try:
                H = await Emote_k(int(uid), emote_id, key, iv, region)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
            except: pass
        count += 1
        await asyncio.sleep(0.1)
    return True, "Done"

async def ArohiAccepted(uid,code,K,V):
    fields = {
        1: 4, 2: {
            1: uid, 3: uid, 8: 1, 9: {2: 161, 4: "y[WW", 6: 11, 8: "1.114.18", 9: 3, 10: 1}, 10: str(code)
        }
    }
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , '0515' , K , V)
# =========================================================================
# --- ONLINE HANDLER (SPAM FIXED HERE) ---
# =========================================================================
async def TcPOnLine(ip, port, key, iv, AutHToKen, reconnect_delay=5.0):
    global online_writer, last_status_packet, status_response_cache, insquad, joining_team, whisper_writer, region
    
    if insquad is not None: insquad = None
    if joining_team is True: joining_team = False
    online_writer = None
    whisper_writer = None
    
    while True:
        try:
            reader, writer = await asyncio.open_connection(ip, int(port))
            online_writer = writer
            bytes_payload = bytes.fromhex(AutHToKen)
            online_writer.write(bytes_payload)
            await online_writer.drain()
            
            while True:
                data2 = await reader.read(9999)
                if not data2: 
                    # 🛑 স্প্যাম থামানোর ম্যাজিক: এখানে ৫ সেকেন্ড অপেক্ষা করবে 🛑
                    await asyncio.sleep(5)
                    break
                    
                data_hex = data2.hex()
                
                if data_hex.startswith('0514'):
                    try:
                        decrypted = await DeCode_PackEt(data_hex[10:])
                        packet_json = json.loads(decrypted)
                        if packet_json.get('1') == 21:
                            if '2' in packet_json and 'data' in packet_json['2']:
                                emote_data = packet_json['2']['data']
                                if ('1' in emote_data and '2' in emote_data and '5' in emote_data and 'data' in emote_data['5']):
                                    nested = emote_data['5']['data']
                                    if '1' in nested and '3' in nested:
                                        sender_uid = nested.get('1', {}).get('data')
                                        emote_id = nested.get('3', {}).get('data')
                                        special_emote = await Emote_k(int(sender_uid), 909038002, key, iv, region)
                                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', special_emote)
                                        await asyncio.sleep(0.3)
                                        try:
                                            mirror_packet = await Emote_k(int(sender_uid), int(emote_id), key, iv, region)
                                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', mirror_packet)
                                        except: pass
                                        await asyncio.sleep(0.2)
                                        try:
                                            bot_uid = 14009897329
                                            bot_self_emote = await Emote_k(bot_uid, int(emote_id), key, iv, region)
                                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', bot_self_emote)
                                        except: pass
                                        continue
                    except: pass

                if data_hex.startswith('0500') and insquad is not None and joining_team == False:
                    try:
                        packet = await DeCode_PackEt(data_hex[10:])
                        packet_json = json.loads(packet)
                        if packet_json.get('1') in [6, 7]: 
                             insquad = None
                             joining_team = False
                             continue
                    except: pass
                
                if data_hex.startswith("0500") and insquad is None and joining_team == False:
                    try:
                        packet = await DeCode_PackEt(data_hex[10:])
                        packet_json = json.loads(packet)
                        uid = packet_json['5']['data']['1']['data']
                        invite_uid = packet_json['5']['data']['2']['data']['1']['data']
                        squad_owner = packet_json['5']['data']['1']['data']
                        code = packet_json['5']['data']['8']['data']
                        emote_id = 909050009
                        bot_uid = 14009897329
                        SendInv = await RedZed_SendInv(bot_uid, invite_uid, key, iv)
                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', SendInv)
                        inv_packet = await RejectMSGtaxt(squad_owner, uid, key, iv)
                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', inv_packet)
                        Join = await ArohiAccepted(squad_owner, code, key, iv)
                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', Join)
                        await asyncio.sleep(2)
                        emote_to_sender = await Emote_k(int(uid), emote_id, key, iv, region)
                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', emote_to_sender)
                        bot_emote = await Emote_k(int(bot_uid), emote_id, key, iv, region)
                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', bot_emote)
                        insquad = True
                    except:
                        insquad = None ; joining_team = False ; continue
                
                if data_hex.startswith('0500') and len(data_hex) > 1000 and joining_team:
                    try:
                        packet = await DeCode_PackEt(data_hex[10:])
                        packet_json = json.loads(packet)
                        OwNer_UiD , CHaT_CoDe , SQuAD_CoDe = await GeTSQDaTa(packet_json)
                        JoinCHaT = await AutH_Chat(3 , OwNer_UiD , CHaT_CoDe, key,iv)
                        await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , JoinCHaT)
                        joining_team = False
                    except: pass
                
                if data_hex.startswith('0500') and len(data_hex) > 1000 and joining_team == False:
                    try:
                        packet = await DeCode_PackEt(data_hex[10:])
                        packet_json = json.loads(packet)
                        OwNer_UiD , CHaT_CoDe , SQuAD_CoDe = await GeTSQDaTa(packet_json)
                        JoinCHaT = await AutH_Chat(3 , OwNer_UiD , CHaT_CoDe, key,iv)
                        await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , JoinCHaT)
                    except: pass

            if online_writer is not None:
                online_writer.close()
                await online_writer.wait_closed()
                online_writer = None
            
            if whisper_writer is not None:
                try: whisper_writer.close() ; await whisper_writer.wait_closed()
                except: pass
                whisper_writer = None
                
            insquad = None
            joining_team = False
        except: await asyncio.sleep(reconnect_delay)
                            
# =========================================================================
# --- CHAT HANDLER (SPAM FIXED HERE) ---
# =========================================================================
async def TcPChaT(ip, port, AutHToKen, key, iv, LoGinDaTaUncRypTinG, ready_event, region , reconnect_delay=5.0):
    global spam_room , whisper_writer , spammer_uid , spam_chat_id , spam_uid , online_writer , chat_id , XX , uid , Spy,data2, Chat_Leave, fast_spam_running, fast_spam_task, custom_spam_running, custom_spam_task, spam_request_running, spam_request_task, evo_fast_spam_running, evo_fast_spam_task, evo_custom_spam_running, evo_custom_spam_task, lag_running, lag_task, evo_cycle_running, evo_cycle_task, reject_spam_running, reject_spam_task
    while True:
        try:
            reader , writer = await asyncio.open_connection(ip, int(port))
            whisper_writer = writer
            bytes_payload = bytes.fromhex(AutHToKen)
            whisper_writer.write(bytes_payload)
            await whisper_writer.drain()
            ready_event.set()
            
            if LoGinDaTaUncRypTinG.Clan_ID:
                clan_id = LoGinDaTaUncRypTinG.Clan_ID
                clan_compiled_data = LoGinDaTaUncRypTinG.Clan_Compiled_Data
                pK = await AuthClan(clan_id , clan_compiled_data , key , iv)
                if whisper_writer: whisper_writer.write(pK) ; await whisper_writer.drain()
            
            while True:
                data = await reader.read(9999)
                if not data: 
                    # 🛑 স্প্যাম থামানোর ম্যাজিক: এখানে ৫ সেকেন্ড অপেক্ষা করবে 🛑
                    print("⚠️ Chat Connection Dropped. Reconnecting in 5s...")
                    await asyncio.sleep(5)
                    break
                
                if data.hex().startswith("120000"):
                    try:
                        response = await DecodeWhisperMessage(data.hex()[10:])
                        uid = response.Data.uid
                        chat_id = response.Data.Chat_ID
                        XX = response.Data.chat_type
                        inPuTMsG = response.Data.msg.lower()
                    except:
                        response = None

                    if response:
                        if inPuTMsG.strip() == '/stop_glory':
                            global glory_running, glory_task
                            if glory_task and not glory_task.done():
                                glory_running = False
                                glory_task.cancel()
                                await safe_send_message(response.Data.chat_type, "[B][C][00FF00]✅ Glory Farm STOPPED!", uid, chat_id, key, iv)
                            else:
                                await safe_send_message(response.Data.chat_type, "[B][C][FF0000]❌ Farm is not running!", uid, chat_id, key, iv)

                        elif inPuTMsG.strip() == '/anas_glory':
                            if not glory_running:
                                glory_running = True
                                glory_task = asyncio.create_task(anas_spider_glory_booster())
                                await safe_send_message(response.Data.chat_type, "[B][C][00FF00]✅ Glory Farm RE-STARTED!", uid, chat_id, key, iv)
                            else:
                                await safe_send_message(response.Data.chat_type, "[B][C][FFFF00]⚠️ Already running!", uid, chat_id, key, iv)

                        elif inPuTMsG.strip() == "/admin":
                            admin_message = """[C][B][FF0000]╔══════════╗\n[FFFFFF]✨ SUBSCRIBE IN YOUTUBE   \n[FFFFFF]          ⚡ SECRETXMODS❤️  \n[FF0000]╠══════════╣\n[FFD700]⚡ OWNER : [FFFFFF]SM    \n[FF0000]╚══════════╝"""
                            await safe_send_message(response.Data.chat_type, admin_message, uid, chat_id, key, iv)

                        elif inPuTMsG.strip().lower() in ("help", "/help", "menu", "/menu", "commands"):
                            header = f"[b][c]{get_random_color()}Hey User Welcome To S M ˣ Roʙᴏᴛ"
                            await safe_send_message(response.Data.chat_type, header, uid, chat_id, key, iv)
                            
                            extra_cmds = """[C][B][FFD700]═══⚡ SPIDER GLORY ⚡═══[00FFFF][B]\n├─ [00FFFF]Start Farm\n│  └─ [FF69B4]/anas_glory\n└─ [00FFFF]Stop Farm\n   └─ [FF69B4]/stop_glory\n[00FFFF]━━━━━━━━━━━━[FF69B4]"""
                            await safe_send_message(response.Data.chat_type, extra_cmds, uid, chat_id, key, iv)

                        response = None
                            
        except Exception as e: whisper_writer = None
        await asyncio.sleep(reconnect_delay)

async def MaiiiinE():
    Uid , Pw = '4594650572','613E476BB3708A0162637547ED62E058FF637113CE4E555A901D1ED00197BDE3'
    
    open_id , access_token = await GeNeRaTeAccEss(Uid , Pw)
    if not open_id or not access_token: return None
    
    PyL = await EncRypTMajoRLoGin(open_id , access_token)
    MajoRLoGinResPonsE = await MajorLogin(PyL)
    if not MajoRLoGinResPonsE: return None
    
    MajoRLoGinauTh = await DecRypTMajoRLoGin(MajoRLoGinResPonsE)
    UrL = MajoRLoGinauTh.url
    region = MajoRLoGinauTh.region
    ToKen = MajoRLoGinauTh.token
    TarGeT = MajoRLoGinauTh.account_uid
    key = MajoRLoGinauTh.key
    iv = MajoRLoGinauTh.iv
    timestamp = MajoRLoGinauTh.timestamp
    
    LoGinDaTa = await GetLoginData(UrL , PyL , ToKen)
    if not LoGinDaTa: return None
    LoGinDaTaUncRypTinG = await DecRypTLoGinDaTa(LoGinDaTa)
    OnLinePorTs = LoGinDaTaUncRypTinG.Online_IP_Port
    ChaTPorTs = LoGinDaTaUncRypTinG.AccountIP_Port
    OnLineiP , OnLineporT = OnLinePorTs.split(":")
    ChaTiP , ChaTporT = ChaTPorTs.split(":")
    acc_name = LoGinDaTaUncRypTinG.AccountName
    
    AutHToKen = await xAuThSTarTuP(int(TarGeT) , ToKen , int(timestamp) , key , iv)
    ready_event = asyncio.Event()
    
    task1 = asyncio.create_task(TcPChaT(ChaTiP, ChaTporT , AutHToKen , key , iv , LoGinDaTaUncRypTinG , ready_event ,region))
    task2 = asyncio.create_task(TcPOnLine(OnLineiP , OnLineporT , key , iv , AutHToKen))  

    os.system('clear')
    print("🤖 BLACK_APIS BOT & SPIDER GLORY - ONLINE")
    print("┌────────────────────────────────────┐")
    print("│ ██████████████████████████████████ │")
    print("└────────────────────────────────────┘")
    print(f"🔹 UID: {TarGeT}")
    print(f"🔹 Name: {acc_name}")
    print(f"🔹 Status: 🟢 READY")
    print("💡 Waiting 10s for Glory Farm to auto-start...")

    await ready_event.wait()
    
    # 🛑 অটো স্টার্ট লজিক 🛑
    global glory_running, glory_task
    glory_running = True
    glory_task = asyncio.create_task(anas_spider_glory_booster())

    await asyncio.gather(task1, task2, glory_task)

def handle_keyboard_interrupt(signum, frame):
    print("\n\n🛑 Bot shutdown requested...")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_keyboard_interrupt)
    
async def StarTinG():
    while True:
        try:
            await asyncio.wait_for(MaiiiinE() , timeout = 7 * 60 * 60)
        except KeyboardInterrupt:
            print("\n\n🛑 Bot shutdown by user")
            break
        except Exception as e: print(f"ErroR TcP - {e} => ResTarTinG ...")

if __name__ == '__main__':
    threading.Thread(target=start_insta_api, daemon=True).start()
    asyncio.run(StarTinG())
