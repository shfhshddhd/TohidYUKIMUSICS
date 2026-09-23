# Copyright (c) 2025 @SUDEEPBOTS <HellfireDevs>
# Location: delhi,noida
#
# All rights reserved.
#
# This code is the intellectual SUDEEPBOTS.
# You are not allowed to copy, modify, redistribute, or use this
# code for commercial or personal projects without explicit permission.
#
# Allowed:
# - Forking for personal learning
# - Submitting improvements via pull requests
#
# Not Allowed:
# - Claiming this code as your own
# - Re-uploading without credit or permission
# - Selling or using commercially
#
# Contact for permissions:
# Email: sudeepgithub@gmail.com

import YUKIIMUSIC.yuki_guard
import asyncio
import os
import re
import aiohttp
import json
import traceback
from typing import Union

import yt_dlp
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message
from youtubesearchpython.__future__ import VideosSearch

from YUKIIMUSIC.utils.database import is_on_off
from YUKIIMUSIC.utils.formatters import time_to_seconds

# SHRUTI API CONFIG
FALLBACK_API_URL = "https://shrutibots.site"
YOUR_API_URL = None

cookies_file = "YUKIIMUSIC/assets/cookies.txt"

# LOCAL MUSIC FOLDER PATH (Apne 45GB wale folder ka path yahan daal)
HELLFIRE_VAULT_DIR = "/home/ubuntu/Hellfire_Vault"

# API URL Loader (Dynamic)
async def get_api_url():
    global YOUR_API_URL
    if YOUR_API_URL: return YOUR_API_URL
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://pastebin.com/raw/rLsBhAQa", timeout=5) as resp:
                if resp.status == 200:
                    YOUR_API_URL = (await resp.text()).strip()
                else:
                    YOUR_API_URL = FALLBACK_API_URL
    except:
        YOUR_API_URL = FALLBACK_API_URL
    return YOUR_API_URL

# Direct Downloader Function
async def download_via_shruti(link: str, is_video: bool = False):
    api_url = await get_api_url()
    video_id = link.split('v=')[-1].split('&')[0] if 'v=' in link else link
    
    # Folder Setup
    folder = "downloads"
    if not os.path.exists(folder): os.makedirs(folder)
    
    ext = "mp4" if is_video else "mp3"
    file_path = os.path.join(folder, f"{video_id}.{ext}")

    # Cache Check
    if os.path.exists(file_path):
        return file_path

    try:
        async with aiohttp.ClientSession() as session:
            req_type = "video" if is_video else "audio"
            
            # Step 1: Get Token
            async with session.get(f"{api_url}/download", params={"url": video_id, "type": req_type}, timeout=20) as resp:
                if resp.status != 200: return None
                data = await resp.json()
                token = data.get("download_token")
                if not token: return None

            # Step 2: Stream & Save
            stream_url = f"{api_url}/stream/{video_id}?type={req_type}"
            async with session.get(stream_url, headers={"X-Download-Token": token}, timeout=600) as resp:
                if resp.status != 200: return None
                
                with open(file_path, "wb") as f:
                    async for chunk in resp.content.iter_chunked(16384):
                        f.write(chunk)
                
                return file_path if os.path.exists(file_path) else None
    except Exception as e:
        print(f"API Download Error: {e}")
        return None

async def shell_cmd(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    out, errorz = await proc.communicate()
    if errorz:
        if "unavailable videos are hidden" in (errorz.decode("utf-8")).lower():
            return out.decode("utf-8")
        else:
            return errorz.decode("utf-8")
    return out.decode("utf-8")

class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"
        self.listbase = "https://youtube.com/playlist?list="
        self.reg = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

    async def exists(self, link: str, videoid: Union[bool, str] = None):
        if videoid: link = self.base + link
        if re.search(self.regex, link): return True
        return False

    async def url(self, message_1: Message) -> Union[str, None]:
        messages = [message_1]
        if message_1.reply_to_message:
            messages.append(message_1.reply_to_message)
        text = ""
        offset = None
        length = None
        for message in messages:
            if offset: break
            if message.entities:
                for entity in message.entities:
                    if entity.type == MessageEntityType.URL:
                        text = message.text or message.caption
                        offset, length = entity.offset, entity.length
                        break
            elif message.caption_entities:
                for entity in message.caption_entities:
                    if entity.type == MessageEntityType.TEXT_LINK:
                        return entity.url
        if offset is None or length is None: return None
        return text[offset : offset + length]

    async def details(self, link: str, videoid: Union[bool, str] = None):
        if videoid: link = self.base + link
        if "&" in link: link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            title = result["title"]
            duration_min = result["duration"]
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            vidid = result["id"]
            if str(duration_min) == "None": duration_sec = 0
            else: duration_sec = int(time_to_seconds(duration_min))
        return title, duration_min, duration_sec, thumbnail, vidid

    async def title(self, link: str, videoid: Union[bool, str] = None):
        if videoid: link = self.base + link
        if "&" in link: link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]: return result["title"]

    async def duration(self, link: str, videoid: Union[bool, str] = None):
        if videoid: link = self.base + link
        if "&" in link: link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]: return result["duration"]

    async def thumbnail(self, link: str, videoid: Union[bool, str] = None):
        if videoid: link = self.base + link
        if "&" in link: link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]: return result["thumbnails"][0]["url"].split("?")[0]

    async def playlist(self, link, limit, user_id, videoid: Union[bool, str] = None):
        if videoid: link = self.listbase + link
        if "&" in link: link = link.split("&")[0]
        playlist = await shell_cmd(
            f"yt-dlp --cookies {cookies_file} -i --get-id --flat-playlist --playlist-end {limit} --skip-download {link}"
        )
        try:
            result = playlist.split("\n")
            result = [key for key in result if key]
        except: result = []
        return result

    @staticmethod
    def _format_duration(seconds):
        if not seconds:
            return None
        try:
            seconds = int(seconds)
        except (TypeError, ValueError):
            return None
        hours, remainder = divmod(seconds, 3600)
        minutes, secs = divmod(remainder, 60)
        if hours:
            return f"{hours}:{minutes:02d}:{secs:02d}"
        return f"{minutes}:{secs:02d}"

    async def _yt_dlp_info(self, target: str, use_search: bool = False):
        loop = asyncio.get_running_loop()
        print(
            f"[YUKI YTDLP ACTIVITY] extract_start target={target!r} "
            f"use_search={use_search} cookiefile_exists={os.path.exists(cookies_file)}",
            flush=True,
        )

        def extract(cookie_enabled):
            opts = {
                "quiet": True,
                "no_warnings": True,
                "noplaylist": True,
                "skip_download": True,
            }
            if use_search:
                # Search only needs result metadata. Flat extraction avoids
                # forcing a full YouTube player request before we have a video.
                opts["extract_flat"] = True
            if cookie_enabled and os.path.exists(cookies_file):
                opts["cookiefile"] = cookies_file
            with yt_dlp.YoutubeDL(opts) as ydl:
                return ydl.extract_info(target, download=False)

        last_error = None
        # Try the saved YouTube cookies first. Some YouTube search/player
        # requests are rejected or challenged when made anonymously. If the
        # cookie session fails, retry without cookies before giving up.
        cookie_modes = (True, False) if use_search else (True, False)
        for cookie_enabled in cookie_modes:
            try:
                result = await loop.run_in_executor(
                    None, lambda ce=cookie_enabled: extract(ce)
                )
                print(
                    f"[YUKI YTDLP ACTIVITY] extract_success "
                    f"cookiefile={cookie_enabled} "
                    f"entries={len(result.get('entries') or []) if isinstance(result, dict) else 'n/a'}",
                    flush=True,
                )
                return result
            except Exception as e:
                last_error = e
                print(
                    f"[YUKI YTDLP INFO ERROR] search={use_search} "
                    f"cookiefile={cookie_enabled} "
                    f"type={type(e).__name__}: {e}",
                    flush=True,
                )
                traceback.print_exc()
        raise last_error

    async def _videos_search_fallback(self, query: str):
        try:
            print(
                f"[YUKI YOUTUBE FALLBACK] VideosSearch start query={query!r}",
                flush=True,
            )
            results = VideosSearch(query, limit=1)
            response = await results.next()
            found = response.get("result") or []
            if not found:
                raise RuntimeError("VideosSearch returned no results")
            result = found[0]
            return {
                "title": result.get("title"),
                "link": result.get("link"),
                "id": result.get("id"),
                "duration": (
                    time_to_seconds(result["duration"])
                    if result.get("duration")
                    else None
                ),
                "thumbnail": (
                    result["thumbnails"][0]["url"].split("?")[0]
                    if result.get("thumbnails")
                    else None
                ),
            }
        except Exception as e:
            print(
                f"[YUKI YOUTUBE FALLBACK ERROR] "
                f"type={type(e).__name__}: {e}",
                flush=True,
            )
            traceback.print_exc()
            raise

    async def track(self, link: str, videoid: Union[bool, str] = None):
        original_link = link
        try:
            if videoid:
                link = self.base + link
            if "&" in link and "youtube.com" in link:
                link = link.split("&")[0]

            is_search = not bool(re.search(self.regex, link))
            target = f"ytsearch1:{link}" if is_search else link

            print(
                f"[YUKI YOUTUBE TRACE] track start "
                f"target={target!r} search={is_search}",
                flush=True,
            )

            try:
                print(
                    f"[YUKI YOUTUBE TRACE] resolving query={link!r} "
                    f"with yt-dlp search={is_search}",
                    flush=True,
                )
                info = await self._yt_dlp_info(target, use_search=is_search)
                if is_search:
                    entries = info.get("entries") or []
                    if not entries:
                        raise RuntimeError("yt-dlp YouTube search returned no results")
                    info = entries[0]
            except Exception as primary_error:
                if not is_search:
                    raise
                print(
                    f"[YUKI YOUTUBE SEARCH RETRY] yt-dlp failed, "
                    f"trying VideosSearch: {type(primary_error).__name__}: "
                    f"{primary_error}",
                    flush=True,
                )
                info = await self._videos_search_fallback(link)

            vidid = info.get("id")
            yturl = info.get("webpage_url") or info.get("original_url") or info.get("link")
            if not yturl and vidid:
                yturl = self.base + vidid
            title = info.get("title")
            duration_min = self._format_duration(info.get("duration"))
            thumbnail = info.get("thumbnail")

            if not vidid or not yturl or not title:
                raise RuntimeError(
                    f"YouTube search returned incomplete track data: "
                    f"id={vidid!r} url={yturl!r} title={title!r}"
                )

            track_details = {
                "title": title,
                "link": yturl,
                "vidid": vidid,
                "duration_min": duration_min,
                "thumb": thumbnail
                    or f"https://i.ytimg.com/vi/{vidid}/hqdefault.jpg",
            }

            print(
                f"[YUKI YOUTUBE TRACE] track success "
                f"vidid={vidid!r} title={title!r}",
                flush=True,
            )
            return track_details, vidid

        except Exception as e:
            print(
                f"[YUKI YOUTUBE ERROR] link={original_link!r} "
                f"type={type(e).__name__}: {e}",
                flush=True,
            )
            traceback.print_exc()
            raise

    async def formats(self, link: str, videoid: Union[bool, str] = None):
        if videoid: link = self.base + link
        if "&" in link: link = link.split("&")[0]
        ytdl_opts = {"quiet": True, "cookiefile": cookies_file}
        ydl = yt_dlp.YoutubeDL(ytdl_opts)
        with ydl:
            formats_available = []
            r = ydl.extract_info(link, download=False)
            for format in r["formats"]:
                try:
                    if "dash" not in str(format["format"]).lower():
                        formats_available.append({
                            "format": format["format"], "filesize": format.get("filesize"),
                            "format_id": format["format_id"], "ext": format["ext"],
                            "format_note": format["format_note"], "yturl": link
                        })
                except: continue
        return formats_available, link

    async def slider(self, link: str, query_type: int, videoid: Union[bool, str] = None):
        if videoid: link = self.base + link
        if "&" in link: link = link.split("&")[0]
        a = VideosSearch(link, limit=10)
        result = (await a.next()).get("result")
        title = result[query_type]["title"]
        duration_min = result[query_type]["duration"]
        vidid = result[query_type]["id"]
        thumbnail = result[query_type]["thumbnails"][0]["url"].split("?")[0]
        return title, duration_min, thumbnail, vidid

    # MODIFIED DOWNLOAD FOR LOCAL FILE CHECK
    async def download(
        self,
        link: str,
        mystic,
        video: Union[bool, str] = None,
        videoid: Union[bool, str] = None,
        songaudio: Union[bool, str] = None,
        songvideo: Union[bool, str] = None,
        format_id: Union[bool, str] = None,
        title: Union[bool, str] = None,
    ) -> str:
        
        # Determine video id for local search
        current_vidid = videoid
        if not current_vidid:
            current_vidid = link.split('v=')[-1].split('&')[0] if 'v=' in link else link

        is_video_req = True if video or songvideo else False
        
        # STEP 1: Check Hellfire Vault (Local 45GB Storage)
        if os.path.exists(HELLFIRE_VAULT_DIR):
            extensions = ["mp4", "mkv"] if is_video_req else ["mp3", "m4a", "webm"]
            for ext in extensions:
                local_file_path = os.path.join(HELLFIRE_VAULT_DIR, f"{current_vidid}.{ext}")
                if os.path.exists(local_file_path):
                    print(f"Playing from Hellfire Vault: {local_file_path}")
                    return local_file_path, True

        if videoid: link = self.base + link

        # STEP 2: API Download Attempt
        try:
            downloaded_file = await download_via_shruti(link, is_video=is_video_req)
            if downloaded_file:
                return downloaded_file, True
        except Exception as e:
            print(f"API Failed, trying Fallback: {e}")

        # STEP 3: Fallback (YT-DLP)
        loop = asyncio.get_running_loop()

        def audio_dl():
            ydl_optssx = {
                "format": "bestaudio/best", "outtmpl": "downloads/%(id)s.%(ext)s",
                "geo_bypass": True, "nocheckcertificate": True, "quiet": True,
                "no_warnings": True, "cookiefile": cookies_file,
            }
            x = yt_dlp.YoutubeDL(ydl_optssx)
            info = x.extract_info(link, False)
            xyz = os.path.join("downloads", f"{info['id']}.{info['ext']}")
            if os.path.exists(xyz): return xyz
            x.download([link])
            return xyz

        def video_dl():
            ydl_optssx = {
                "format": "(bestvideo[height<=?720][width<=?1280][ext=mp4])+(bestaudio[ext=m4a])",
                "outtmpl": "downloads/%(id)s.%(ext)s",
                "geo_bypass": True, "nocheckcertificate": True, "quiet": True,
                "no_warnings": True, "cookiefile": cookies_file,
            }
            x = yt_dlp.YoutubeDL(ydl_optssx)
            info = x.extract_info(link, False)
            xyz = os.path.join("downloads", f"{info['id']}.{info['ext']}")
            if os.path.exists(xyz): return xyz
            x.download([link])
            return xyz

        if video:
            direct = True
            downloaded_file = await loop.run_in_executor(None, video_dl)
        else:
            direct = True
            downloaded_file = await loop.run_in_executor(None, audio_dl)
            
        return downloaded_file, direct
