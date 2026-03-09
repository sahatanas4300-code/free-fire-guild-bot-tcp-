import asyncio

# আপনার ২০টি বটের লিস্ট (accounts.json থেকে আসবে)
all_bots = ["uid1", "uid2", "uid3", "uid4", "uid5", "uid6", "uid7", "uid8", ..., "uid20"]
GUILD_ID = "আপনার_গিল্ডের_আইডি"

async def wait_for_guild_approval(uid, token):
    """গিল্ড অ্যাপ্রুভালের জন্য অপেক্ষা করার লজিক"""
    print(f"[{uid}] গিল্ডের অবস্থা চেক করা হচ্ছে...")
    
    in_guild = await check_if_in_guild(token) # xC4.py থেকে গিল্ড চেকিং প্যাকেট
    
    if not in_guild:
        print(f"[{uid}] গিল্ডে নেই! রিকোয়েস্ট পাঠানো হচ্ছে...")
        await send_guild_request(token, GUILD_ID) # xC4.py থেকে রিকোয়েস্ট প্যাকেট
        
        # যতক্ষণ অ্যাকসেপ্ট না হবে, বট এখানে আটকে থাকবে
        while not in_guild:
            print(f"[{uid}] মালিকের অ্যাপ্রুভালের অপেক্ষায় আছে...")
            await asyncio.sleep(30) # ৩০ সেকেন্ড পর পর চেক করবে
            in_guild = await check_if_in_guild(token)
            
    print(f"[{uid}] ✅ গিল্ডে জয়েন সফল হয়েছে! এখন খেলার জন্য প্রস্তুত।")
    return True

async def run_squad_match(team_name, leader, members):
    """৪ জনের টিম বানিয়ে ম্যাচ স্টার্ট করার লজিক"""
    print(f"\n--- {team_name} তৈরি করা হচ্ছে ---")
    
    # ১. লিডার স্কোয়াড তৈরি করবে
    await create_squad(leader['token']) 
    
    # ২. লিডার বাকি ৩ জনকে ইনভাইট দিবে এবং তারা একসেপ্ট করবে
    for member in members:
        await invite_player(leader['token'], member['uid'])
        await accept_invite(member['token'], leader['uid'])
        print(f"  -> {member['uid']} টিমে জয়েন করেছে।")
        
    # ৩. সবাই রেডি হলে লিডার ম্যাচ স্টার্ট দিবে
    print(f"🎮 {team_name} ফুল! ম্যাচ স্টার্ট দেওয়া হচ্ছে...")
    await start_match(leader['token']) # xC4.py এর FS প্যাকেট
    await asyncio.sleep(10) # ম্যাচ রেজিস্টার হওয়ার জন্য হোল্ড

async def main():
    print("🕸️ SPIDER ADVANCED GUILD BOT (SQUAD MODE) 🕸️")
    
    # ধাপ ১: ২০টি বটকে ৫টি টিমে ভাগ করা (৪ জন করে)
    teams = [all_bots[i:i+4] for i in range(0, len(all_bots), 4)]
    
    # ধাপ ২: সব বটকে গিল্ড অ্যাপ্রুভালের জন্য পাঠানো
    for uid in all_bots:
        # টোকেন জেনারেট করে গিল্ড অ্যাপ্রুভালের লজিক কল করা হবে
        pass
        
    # ধাপ ৩: সব বট গিল্ডে ঢুকে গেলে ৫টি টিম একসাথে রান করবে
    while True:
        for index, team in enumerate(teams):
            leader = team[0]
            members = team[1:]
            # টিম অনুযায়ী ম্যাচ রান করা
            await run_squad_match(f"Team-{index+1}", leader, members)
            
        print("\n⏳ সব টিমের রাউন্ড শেষ। পরবর্তী রাউন্ড শুরু হচ্ছে...")
        await asyncio.sleep(60)
