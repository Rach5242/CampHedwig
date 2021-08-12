import sqlite3
import discord
from discord.ext import commands
import datetime

"""
DROP DATASET MAKEUP

0. guild_id
1. channel
2. emoji
3. message
4. image
5. time
6. last_drop
"""


async def set_drop_channel(guild, channel):
    r = await fetch_drop(guild)
    db = sqlite3.connect('drops.sqlite') 
    c = db.cursor()
    if r is None:
        c.execute("INSERT INTO drops(guild_id, channel) VALUES(?,?)",(guild, channel,))
    
    elif r is not None:
        c.execute("UPDATE drops SET channel = ? WHERE guild_id = ?", (channel, guild,))
    
    db.commit()
    c.close()
    db.close()

async def set_user(guild, user, count):
    db = sqlite3.connect('drops.sqlite')
    c = db.cursor()
    c.execute("INSERT INTO users(guild_id, user_id, count, active) VALUES(?,?,?)", (guild, user, count, 'True',))
    db.commit()
    c.close()
    db.close()

async def update_count(guild, user):
    r = await fetch_user(guild, user)
    if r is None:
        await set_user(guild, user, 1)
    else:
        db = sqlite3.connect('drops.sqlite')
        c = db.cursor()
        c.execute("UPDATE users SET count = ? WHERE guild_id = ? and user_id = ?", (int(r[2]) + 1, guild, user,))
        db.commit()
        c.close()
        db.close() 

async def fetch_user(guild, user):
    db = sqlite3.connect('drops.sqlite')
    c = db.cursor()
    result = c.execute("SELECT * FROM users WHERE guild_id = ? and user_id = ?", (guild, user,)).fetchone()
    c.close()
    db.close()
    return result

async def fetch_all(guild):
    db = sqlite3.connect('drops.sqlite')
    cursor = db.cursor()
    results = cursor.execute("SELECT user_id, count FROM users WHERE guild_id = ? and active = ? ORDER BY count DESC", (guild, 'True',)).fetchall()
    cursor.close()
    db.close()
    return results

async def add_prefix(guild, prefix):
    r = await fetch_prefix(guild)
    db = sqlite3.connect('main.sqlite')
    c = db.cursor()
    if r is None:
        c.execute("INSERT INTO config(guild_id, prefix) VALUES(?,?)", (guild, prefix,))
    
    else:
        c.execute("UPDATE config SET prefix = ? WHERE guild_id = ?", (prefix, guild,))
    
    db.commit()
    c.close()
    db.close()

async def fetch_prefix(guild):
    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()
    results = cursor.execute("SELECT prefix FROM config WHERE guild_id = ?", (guild,)).fetchone()
    cursor.close()
    db.close()
    return results

async def set_msg_time(guild, time):
    r = await fetch_drop(guild)
    db = sqlite3.connect('drops.sqlite')
    c = db.cursor()
    if r is None:
        c.execute("INSERT INTO drops(guild_id, time) VALUES(?,?)", (guild, time,))
    
    elif r is not None:
        c.execute("UPDATE drops SET time = ? WHERE guild_id = ?", (time, guild,)) 

    db.commit()
    c.close()
    db.close() 

async def fetch_all_drops():
    db = sqlite3.connect('drops.sqlite')
    c = db.cursor()
    results = c.execute("SELECT * FROM drops").fetchall()
    c.close()
    db.close()
    return results

async def fetch_drop(guild):
    db = sqlite3.connect('drops.sqlite')
    c = db.cursor()
    result = c.execute("SELECT * FROM drops WHERE guild_id = ?", (guild,)).fetchone()
    c.close()
    db.close()
    return result

async def set_drop_msg(guild, message):
    r = await fetch_drop(guild)
    db = sqlite3.connect('drops.sqlite')
    c = db.cursor()
    if r is None:
        c.execute("INSERT INTO drops(guild_id, message) VALUES(?,?)", (guild, message,))
    
    elif r is not None:
        c.execute("UPDATE drops SET message = ? WHERE guild_id = ?", (message, guild,))
    
    db.commit()
    c.close()
    db.close()

async def set_drop_image(guild, image):
    r = await fetch_drop(guild)
    db = sqlite3.connect('drops.sqlite')
    c = db.cursor()
    if r is None:
        c.execute("INSERT INTO drops(guild_id, image) VALUES(?,?)", (guild, image,))
    
    elif r is not None:
        c.execute("UPDATE drops SET image = ? WHERE guild_id = ?", (image, guild,))
    
    db.commit()
    c.close()
    db.close()

async def set_drop_emoji(guild, emoji):
    r = await fetch_drop(guild)
    db = sqlite3.connect('drops.sqlite')
    c = db.cursor()
    if r is None:
        c.execute("INSERT INTO drops(guild_id, emoji) VALUES(?,?)", (guild, emoji,))

    elif r is not None:
        c.execute("UPDATE drops SET emoji = ? WHERE guild_id = ?", (emoji, guild,))

    db.commit()
    c.close()
    db.close()

async def set_last_drop(guild):
    TimeNow = datetime.datetime.utcnow().strftime('%m, %d, %Y %H:%M:%S')
    db = sqlite3.connect('drops.sqlite')
    c = db.cursor()
    c.execute("UPDATE drops SET last = ? WHERE guild_id = ? ", (TimeNow, guild,))
    db.commit()
    c.close()
    db.close()
