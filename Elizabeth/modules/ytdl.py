from pathlib import Path
import asyncio, time, io, math, os, logging, asyncio, shutil, re, subprocess, json
from re import findall
from asyncio import sleep
from telethon.events import NewMessage
from telethon.tl.custom import Dialog
from datetime import datetime as dt
from pytz import country_names as c_n, country_timezones as c_tz, timezone as tz
from hachoir.parser import createParser
import pybase64
from base64 import b64decode
from pySmartDL import SmartDL
from telethon.tl.types import DocumentAttributeVideo, DocumentAttributeAudio
from telethon import events
from Elizabeth.events import register
from Elizabeth.utils import progress
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from validators.url import url
from html import unescape
from urllib.error import HTTPError
import bs4
from bs4 import BeautifulSoup
from youtube_dl import YoutubeDL
from datetime import datetime
from youtube_dl.utils import (DownloadError, ContentTooShortError,

                              ExtractorError, GeoRestrictedError,
                              MaxDownloadsReached, PostProcessingError,
                              UnavailableVideoError, XAttrMetadataError)

try:

   from youtubesearchpython import SearchVideos 

except:
	os.system("pip install pip install youtube-search-python")
	from youtubesearchpython import SearchVideos 
	pass

@register(pattern="^yt (.*)")
async def download_video(v_url):
	url = v_url.pattern_match.group(1)
    	if not url:
        	rmsg = await v_url.get_reply_message()
        	myString = rmsg.text
        	url = re.search("(?P<url>https?://[^\s]+)", myString).group("url")
    	if not url:
        	await edit_or_reply(v_url, "What I am Supposed to find? Give link")
        	return
	v_url = await edit_or_reply(v_url, "`Preparing to download...`")
    	reply_to_id = await reply_id(v_url)
	opts = {
            "format": "bestaudio",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "writethumbnail": True,
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "320",
                }
            ],
            "outtmpl": "%(id)s.mp3",
            "quiet": True,
            "logtostderr": False,
        }
        video = False
        song = True
	try:
        	await v_url.edit("`Fetching data, please wait..`")
        	with YoutubeDL(opts) as ytdl:
         	   ytdl_data = ytdl.extract_info(url)
  	except DownloadError as DE:
     		await v_url.edit(f"`{str(DE)}`")
      	 	return
 	except ContentTooShortError:
	     	await v_url.edit("`The download content was too short.`")
        	return
   	except GeoRestrictedError:
        	await v_url.edit("`Video is not available from your geographic location due to geographic restrictions imposed by a website.`")
        	return
    	except MaxDownloadsReached:
       		await v_url.edit("`Max-downloads limit has been reached.`")
       		return
    	except PostProcessingError:
        	await v_url.edit("`There was an error during post processing.`")
        	return
   	except UnavailableVideoError:
        	await v_url.edit("`Media is not available in the requested format.`")
        	return
    	except XAttrMetadataError as XAME:
        	await v_url.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
        	return
    	except ExtractorError:
        	await v_url.edit("`There was an error during info extraction.`")
        	return
    	except Exception as e:
        	await v_url.edit(f"{str(type(e)): {str(e)}}")
        	return
	if song:
        await v_url.edit(f"`Preparing to upload song:`\\n**{ytdl_data['title']}**\\nby *Alexia*")
        await v_url.client.send_file(
            v_url.chat_id,
            f"{ytdl_data['id']}.mp3",
            supports_streaming=True,
            thumb=None,
            reply_to=reply_to_id,
            attributes=[
                DocumentAttributeAudio(
                    duration=int(ytdl_data["duration"]),
                    title=str(ytdl_data["title"]),
                    performer=str(ytdl_data["uploader"]),
                )
            ],
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(
                    d, t, v_url, c_time, "Uploading..", f"{ytdl_data['title']}.mp3"
                )
            ),
        )
        os.remove(f"{ytdl_data['id']}.mp3")
_help__ = """
 ➩ yt <youtube link>: uploads the song in it's best quality available
"""

__mod_name__ = "Ytdl"