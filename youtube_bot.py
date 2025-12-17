import discord
from discord.ext import tasks
import feedparser
import datetime
import keep_alive
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
YOUTUBE_CHANNEL_ID = os.getenv('YOUTUBE_CHANNEL_ID')

try:
    CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
except TypeError:
    CHANNEL_ID = 0

YOUTUBE_RSS_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={YOUTUBE_CHANNEL_ID}"
intents = discord.Intents.default()
client = discord.Client(intents=intents)

last_video_id = None

@client.event
async def on_ready():
    print(f'SYSTEM ONLINE: {client.user}')
    if not DISCORD_TOKEN or not YOUTUBE_CHANNEL_ID or not CHANNEL_ID:
        print("WARNING: Missing Configuration in .env")
    check_youtube.start()

@tasks.loop(seconds=60)
async def check_youtube():
    global last_video_id
    channel = client.get_channel(CHANNEL_ID)
    
    if channel is None:
        return

    try:
        feed = feedparser.parse(YOUTUBE_RSS_URL)
        
        if feed.entries:
            latest_video = feed.entries[0]
            video_id = latest_video.yt_videoid
            video_link = latest_video.link
            video_title = latest_video.title
            author_name = latest_video.author
            
            if last_video_id is None:
                last_video_id = video_id
                return

            if video_id != last_video_id:
                last_video_id = video_id
                
                embed = discord.Embed(
                    title="⚠️ INCOMING_TRANSMISSION",
                    url=video_link,
                    description=f"```glsl\n# SYSTEM_ALERT: NEW_VIDEO_DETECTED\n# SOURCE: {author_name}\n# STATUS: DECRYPTED_SUCCESSFULLY```",
                    color=0x00FF00
                )
                
                thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
                embed.set_image(url=thumbnail_url)
                
                embed.add_field(
                    name="📂 PAYLOAD", 
                    value=f"```{video_title}```", 
                    inline=False
                )
                embed.add_field(
                    name="🔗 EXECUTE_LINK", 
                    value=f"**[>>> CLICK_TO_ACCESS_DATABASE <<<]({video_link})**", 
                    inline=True
                )
                
                now = datetime.datetime.now().strftime("%H:%M:%S")
                embed.set_footer(text=f"TIMESTAMP: {now} | ENCRYPTION: AES-256")
                
                await channel.send(content="|| @everyone ||", embed=embed)
                
    except Exception:
        pass

@check_youtube.before_loop
async def before_check_youtube():
    await client.wait_until_ready()

keep_alive.keep_alive()
client.run(DISCORD_TOKEN)