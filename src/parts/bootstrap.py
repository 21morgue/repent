ver = "1.0"
stopper = False
seshid = None
seshidhash = None
currentvc = None
currentvcguild = None
import shutil
from typing import Union
from pathlib import Path
import discord as discord, psutil, cpuinfo, GPUtil, time, os, base64, io, random, string, urllib.parse, urllib.request, json, http.client, aiohttp, asyncio, ctypes, pyfiglet, re, threading, webbrowser, aiofiles, httpx, websockets, warnings, glob, typing, platform, locale

try:
    import ctypes.wintypes
    HAS_WINDOWS = True
except (ImportError, AttributeError):
    HAS_WINDOWS = False

try:
    import winreg
    HAS_WINREG = True
except ImportError:
    HAS_WINREG = False

from discord.utils import get
from random import randint
from youtube_search import YoutubeSearch
from urllib.parse import urlparse
import threading
from json import *
from io import BytesIO
warnings.filterwarnings(
    "ignore",
    message=r"pkg_resources is deprecated as an API.*",
    category=UserWarning,
    module=r"petpetgif\.petpet",
)
from petpetgif import petpet as petpetgif
from discord.ext import commands
from bs4 import BeautifulSoup as bs4
from colorama import Fore, Style
from PIL import Image, ImageDraw, ImageOps
from gtts import gTTS
from fractions import Fraction
from datetime import datetime, timedelta, timezone
from pystyle import  Colors, Colorate
from notifypy import Notify
import subprocess
import sys
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from websockets import connect
import logging
from collections import defaultdict
import certifi
import platform
import ssl
import requests as requested
from aiohttp_socks import ProxyConnector
from discord_protos import FrecencyUserSettings
from google.protobuf.json_format import ParseDict, MessageToDict
import builtins
import urllib.parse
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding='utf-8', errors='replace')
    except (AttributeError, ValueError):
        pass

if platform.system() == "Windows":
    try:
        ctypes.windll.kernel32.SetConsoleOutputCP(65001)
        ctypes.windll.kernel32.SetConsoleCP(65001)
    except Exception:
        pass

class _CONSOLE_COORD(ctypes.Structure):
    _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

def set_console_font_temporary(face_name="Cascadia Mono", height=16):
    if platform.system() != "Windows" or not HAS_WINDOWS:
        return
    try:
        class CONSOLE_FONT_INFOEX(ctypes.Structure):
            _fields_ = [
                ("cbSize", ctypes.c_ulong),
                ("nFont", ctypes.c_ulong),
                ("dwFontSize", _CONSOLE_COORD),
                ("FontFamily", ctypes.c_uint),
                ("FontWeight", ctypes.c_uint),
                ("FaceName", ctypes.c_wchar * 32),
            ]
        GENERIC_READ = 0x80000000
        GENERIC_WRITE = 0x40000000
        FILE_SHARE_READ = 0x1
        FILE_SHARE_WRITE = 0x2
        OPEN_EXISTING = 3
        INVALID_HANDLE_VALUE = -1
        handle = ctypes.windll.kernel32.CreateFileW(
            "CONOUT$", GENERIC_READ | GENERIC_WRITE,
            FILE_SHARE_READ | FILE_SHARE_WRITE, None, OPEN_EXISTING, 0, None
        )
        if handle == INVALID_HANDLE_VALUE:
            return
        font = CONSOLE_FONT_INFOEX()
        font.cbSize = ctypes.sizeof(CONSOLE_FONT_INFOEX)
        font.dwFontSize = _CONSOLE_COORD(0, height)
        font.FontFamily = 54
        font.FontWeight = 400
        font.FaceName = face_name
        ctypes.windll.kernel32.SetCurrentConsoleFontEx(handle, ctypes.c_long(False), ctypes.byref(font))
        ctypes.windll.kernel32.CloseHandle(handle)
    except Exception as e:
        print(f"[WARNING] Failed to set console font for this session: {e}")

set_console_font_temporary()

BOOTSTRAP_DIR = Path(__file__).resolve().parent
REPENT_APP_DIR = BOOTSTRAP_DIR.parent
PROJECT_ROOT = REPENT_APP_DIR.parent

DATA_DIR = PROJECT_ROOT / "data"
CONFIG_DIR = DATA_DIR / "settings" / "configs"
CONFIG_FILE = CONFIG_DIR / "config.json"
PROXIES_FILE = DATA_DIR / "proxies" / "proxies.txt"
ASSETS_DIR = PROJECT_ROOT / "assets"
ICON_FILE = ASSETS_DIR / "icons" / "repentlogo.ico"
FONT_FILE = ASSETS_DIR / "fonts" / "Boogaloo-Regular.ttf"
GUI_FILE = REPENT_APP_DIR / "ui" / "index.html"

os.chdir(PROJECT_ROOT)
os.environ['SSL_CERT_FILE'] = str(CONFIG_DIR / "cacert.pem")

warnings.filterwarnings("ignore", category=DeprecationWarning, module="typing")
warnings.simplefilter("ignore", DeprecationWarning)

class reqresp:
    def __init__(self, status, data):
        self.status_code = status
        self._data = data

    @property
    def text(self):
        try:
            return self._data.decode('utf-8')
        except UnicodeDecodeError:
            return self._data

    def json(self):
        try:
            return json.loads(self._data.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return None
    
    @property   
    def content(self):
        return self._data

class requesters:
    @staticmethod
    def request(method, url, headers=None, json_data=None, quiet=False):
        if headers is None:
            headers = {}
        
        context = ssl.create_default_context()
        parsed_url = urlparse(url)
        host = parsed_url.netloc
        endpoint = parsed_url.path
        if parsed_url.query:
            endpoint += '?' + parsed_url.query
        
        if parsed_url.scheme == "https":
            connection = http.client.HTTPSConnection(host, context=context)
        else:
            connection = http.client.HTTPConnection(host)
        
        body = None
        if json_data is not None:
            body = json.dumps(json_data)
            headers['Content-Type'] = 'application/json'
        
        try:
            connection.request(method, endpoint, body=body, headers=headers)
            response = connection.getresponse()
            response_data = response.read()
            connection.close()
            return reqresp(response.status, response_data)
        except ConnectionRefusedError as e:
            if not quiet:
                print(f"Connection failed: {e}. Method: {method}, URL: {url}, Headers: {headers}, Body: {body}")
            return reqresp(500, b"")
        except Exception as e:
            if not quiet:
                print(f"An error occurred: {e}. Method: {method}, URL: {url}, Headers: {headers}, Body: {body}")
            return reqresp(500, b"")

    @staticmethod
    def get(url, headers=None, quiet=False):
        return requesters.request("GET", url, headers=headers, quiet=quiet)

    @staticmethod 
    def post(url, headers=None, json_data=None, quiet=False):
        return requesters.request("POST", url, headers=headers, json_data=json_data, quiet=quiet)

    @staticmethod
    def patch(url, headers=None, json_data=None, quiet=False):
        return requesters.request("PATCH", url, headers=headers, json_data=json_data, quiet=quiet)

    @staticmethod
    def delete(url, headers=None, json_data=None, quiet=False):
        return requesters.request("DELETE", url, headers=headers, json_data=json_data, quiet=quiet)

    @staticmethod
    def put(url, headers=None, json_data=None, quiet=False):
        return requesters.request("PUT", url, headers=headers, json_data=json_data, quiet=quiet)

_async_http_ssl_context = ssl.create_default_context()
_async_http_client = httpx.AsyncClient(verify=_async_http_ssl_context, timeout=20.0)

class arequesters:
    @staticmethod
    async def request(method, url, headers=None, json_data=None, quiet=False):
        try:
            response = await _async_http_client.request(method, url, headers=headers, json=json_data)
            return reqresp(response.status_code, response.content)
        except httpx.ConnectError as e:
            if not quiet:
                print(f"Connection failed: {e}. Method: {method}, URL: {url}, Headers: {headers}")
            return reqresp(500, b"")
        except Exception as e:
            if not quiet:
                print(f"An error occurred: {e}. Method: {method}, URL: {url}, Headers: {headers}")
            return reqresp(500, b"")

    @staticmethod
    async def get(url, headers=None, quiet=False):
        return await arequesters.request("GET", url, headers=headers, quiet=quiet)

    @staticmethod
    async def post(url, headers=None, json_data=None, quiet=False):
        return await arequesters.request("POST", url, headers=headers, json_data=json_data, quiet=quiet)

    @staticmethod
    async def patch(url, headers=None, json_data=None, quiet=False):
        return await arequesters.request("PATCH", url, headers=headers, json_data=json_data, quiet=quiet)

    @staticmethod
    async def delete(url, headers=None, json_data=None, quiet=False):
        return await arequesters.request("DELETE", url, headers=headers, json_data=json_data, quiet=quiet)

    @staticmethod
    async def put(url, headers=None, json_data=None, quiet=False):
        return await arequesters.request("PUT", url, headers=headers, json_data=json_data, quiet=quiet)

def get_websocket():
    websocket = getattr(Repent, "ws", None)
    if websocket is None:
        websocket = getattr(getattr(Repent, "_connection", None), "ws", None)
    if websocket is None:
        raise RuntimeError("Discord gateway websocket is not connected")
    return websocket

async def make_server(name, icon=None):
    if icon != None:
        icon = base64.b64encode(icon).decode('utf-8')
        payload = {
    "name": name,
    "icon": icon
    }
    else:
        payload = {
            "name": name
            }
    headers = {
    'Authorization': config_get('token'),
    'x-super-properties': getxsuper(),
    }
    data = (await arequesters.post("https://discord.com/api/v9/guilds", headers=headers, json_data=payload)).json()
    try:
        websocket = get_websocket()
        await websocket.send_as_json({"op":37,"d":{"subscriptions":{data['id']:{"typing":True,"threads":True,"activities":True,"members":[],"member_updates":True,"channels":{},"thread_member_lists":[]}}}})
    except Exception as e:
        pass
    return data

CONSOLE_LOG = []
CONSOLE_LOG_LOCK = threading.Lock()
_console_next_id = 1

def console_push(kind, text):
    global _console_next_id
    with CONSOLE_LOG_LOCK:
        CONSOLE_LOG.append({"id": _console_next_id, "kind": kind, "text": text})
        _console_next_id += 1
        if len(CONSOLE_LOG) > 1000:
            del CONSOLE_LOG[:len(CONSOLE_LOG) - 1000]

_CONSOLE_LEVEL_TAG_RE = re.compile(r'^\[(INFO|SUCCESS|WARN|WARNING|ERROR|DEBUG)\]:?\s*', re.IGNORECASE)
_CONSOLE_LEVEL_STYLE = {
    'INFO': (Fore.LIGHTCYAN_EX, 'i'),
    'SUCCESS': (Fore.LIGHTGREEN_EX, '+'),
    'WARNING': (Fore.LIGHTYELLOW_EX, '!'),
    'ERROR': (Fore.LIGHTRED_EX, 'x'),
    'DEBUG': (Fore.LIGHTMAGENTA_EX, '~'),
}

def print(message):
    text = str(message)
    timestamp = f"{Fore.LIGHTBLACK_EX}[{datetime.now().strftime('%H:%M:%S')}]{Style.RESET_ALL}"
    if not text.startswith('\x1b['):
        tag_match = _CONSOLE_LEVEL_TAG_RE.match(text)
        if tag_match:
            level = tag_match.group(1).upper()
            if level == 'WARN':
                level = 'WARNING'
            color, icon = _CONSOLE_LEVEL_STYLE[level]
            rest = text[tag_match.end():]
            text = f"{color}[{icon}] {level}{Style.RESET_ALL} {rest}"
    formatted = f"{timestamp} {text}"
    try:
        builtins.print(formatted)
    except UnicodeEncodeError:
        builtins.print(formatted.encode('utf-8', errors='replace').decode('utf-8', errors='replace'))
    console_push("print", formatted)

def tokenvalid(token):
    if not token:
        return False
    headers = {'Authorization': token, "x-super-properties": getxsuper()}
    r = requesters.get("https://discord.com/api/v9/users/@me" , headers=headers)
    if r.status_code == 200:
        return True
    else:
        return False

def del_value(key):
    with open(CONFIG_FILE, 'r') as file:
        data_dict = json.load(file)
    if key in data_dict:
        del data_dict[key]
    with open(CONFIG_FILE, 'w') as file:
        json.dump(data_dict, file, indent=4)

def resize_terminal():
    os_name = platform.system()
    if os_name == "Darwin" or os_name == "Linux":
        print("\033[8;30;100t")
resize_terminal()

def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
       # print(f"Creating {folder_path}")

def download_file(url, path):
    if os.path.exists(path):
        return   
    if url == '{}':
        with open(path, 'w') as f:
            f.write('{\n}')
      #  print(f"Creating {path}")
    else:
        response = requesters.get(url)
        with open(path, 'wb') as f:
            f.write(response.content)
       # print(f"Creating {path}")

def open_config_read(file_path=CONFIG_FILE):
    with open(file_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
    return data

def checkwebhook(url):
    req = requesters.get(url)
    if req.status_code == 200:
        return True
    else:
        return False

def filesafe(filename):
    replacements = {
        '<': 'lt',
        '>': 'gt',
        ':': '_colon_',
        '"': '_quote_',
        '/': '_slash_',
        '\\': '_backslash_',
        '|': '_pipe_',
        '?': '_questionmark_',
        '*': '_asterisk_'
    }
    for char, replacement in replacements.items():
        filename = filename.replace(char, replacement)
    filename = filename.strip()
    filename = re.sub(r'^\.|\.$', '', filename)
    filename = re.sub('_+', '_', filename)
    filename = filename.rstrip('. ')
    return filename

WEBHOOK_URL_RE = re.compile(r'https://(canary\.|ptb\.)?(discord|discordapp)\.com/api/webhooks/\d+/[\w-]+')

def validate_setup_field(key, kind, raw_value):
    if kind == 'token':
        if tokenvalid(raw_value):
            return True, raw_value, None
        return False, None, "Token is invalid, please try again."
    if kind == 'int':
        try:
            return True, int(raw_value), None
        except (TypeError, ValueError):
            return False, None, "Please input an integer (seconds)."
    if kind == 'select_device':
        if raw_value.lower() in ("console", "web", "mobile", "desktop"):
            return True, raw_value.lower(), None
        return False, None, "Please choose a valid device."
    if kind == 'select_embed':
        if raw_value.lower() in ("web", "indent", "app"):
            return True, raw_value.lower(), None
        return False, None, "Please choose a valid embed mode."
    if kind == 'rpc_bool':
        return True, ("rpc" if raw_value else ""), None
    if kind == 'bool':
        return True, bool(raw_value), None
    if kind == 'webhook':
        if not raw_value:
            return True, "", None
        if WEBHOOK_URL_RE.search(raw_value) and checkwebhook(raw_value):
            return True, raw_value, None
        return False, None, "That isn't a valid, reachable webhook URL."
    return True, raw_value, None

ccs = []
def customcmds():
    custom_commands_executed = 0
    global command_names
    globals_dict = globals()  
    try:
        for thing in os.listdir('data/customcmds'):
            if thing.endswith(".py"):
                file_path = os.path.join('data/customcmds', thing).replace('\\', '/')
                with open(file_path, encoding="utf-8") as file:
                    code = file.read()
                pattern = r"@Repent\.command\(.*?help\s*=\s*['\"](.*?)['\"].*?\)"
                matches = re.findall(pattern, code, re.DOTALL)
                for match in matches:
                    code = code.replace(match, match.lower())
                try:
                    compiled_code = compile(code, file_path, 'exec')
                    exec(compiled_code, globals_dict, globals_dict)
                    custom_commands_executed += 1
                    lines = code.splitlines()
                    decorator_found = False
                    def_pattern = r'(?:(?:async\s+)?def\s+)(\w+)(?=\()'

                    for line in lines:
                        line = line.strip()
                        if line.startswith("@Repent.command"):
                            decorator_found = True 
                        elif decorator_found and re.search(def_pattern, line):
                            command_name = re.match(def_pattern, line).group(1)
                            ccs.append(command_name)
                            decorator_found = False
                except SyntaxError as se:
                    print(f"Syntax error in file {file_path}: {se}")
    except Exception as e:
        print(f"Error loading custom commands: {e}")
    return custom_commands_executed

def count_custom_commands():
    custom_commands_counted = 0
    try:
        for thing in os.listdir('data/customcmds'):
            if thing.endswith(".py"):
                file_path = os.path.join('data/customcmds', thing)
                with open(file_path, encoding="utf-8") as file:
                    code = file.read()
                try:
                    compile(code, file_path, 'exec')
                    custom_commands_counted += 1
                except SyntaxError:
                    pass
    except Exception as e:
        pass
    return custom_commands_counted

def config_get(data):
    for attempt in range(3):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
            break
        except json.JSONDecodeError:
            if attempt == 2:
                raise
            time.sleep(0.05)
    value = config.get(data)
    return value

def config_edit(data, new_value):
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
    config[data] = new_value
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def setting_get(data):
    with open('data/settings/configs/settings.json', 'r') as f:
        settings = json.load(f)
    value = settings.get(data)
    return value

def setting_edit(data, new_value):
    settings_path = 'data/settings/configs/settings.json'
    if os.path.exists(settings_path):
        with open(settings_path, 'r') as f:
            settings = json.load(f)
    else:
        settings = {}
    if isinstance(new_value, bool):
        settings[data] = new_value
    else:
        if data in settings:
            if isinstance(settings[data], list):
                if new_value in settings[data]:
                    settings[data].remove(new_value)
                else:
                    settings[data].append(new_value)
            else:
                settings[data] = [settings[data], new_value]
        else:
            settings[data] = [new_value]
    with open(settings_path, 'w') as f:
        json.dump(settings, f, indent=4)

def notif(message):
    notification = Notify()
    notification.application_name = "repent.wtf"
    notification.title = f"repent"
    notification.message = message
    notification.icon = str(ICON_FILE)
    notification.send()

def windowname(commandsdone):
    if os.name == "nt" and HAS_WINDOWS:
        try:
            ctypes.windll.kernel32.SetConsoleTitleW(f"repent.wtf  |  cmds used: {commandsdone}  |  guilds: {len(Repent.guilds)}  |  prefix: {config_get('prefix')}")
        except Exception as e:
            pass
    elif os.name == "posix":
        title = f"repent.wtf  |  cmds used: {commandsdone}  |  guilds: {len(Repent.guilds)}  |  prefix: {config_get('prefix')}"
        print(f"\033]0;{title}\007", end="", flush=True)

def get_time():
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    final_time = current_time.split(':')
    return f'{final_time[0]}:{final_time[1]}'

def check_and_replace_empty(config_value):
    return None if config_value == "" else config_value

def split_into_chunks(input_message, maxlength):
    chunks = []
    input_message = input_message.replace('%20', ' ')
    while len(input_message) > maxlength:
        split_pos = input_message.rfind(' ', 0, maxlength) 
        if split_pos == -1:
            split_pos = maxlength
            chunk = input_message[:split_pos].rstrip()
            chunks.append(chunk)
            input_message = input_message[split_pos:].lstrip()
        else:
            chunk = input_message[:split_pos].rstrip()
            chunks.append(chunk)
            input_message = input_message[split_pos:].lstrip()
    if input_message:
        chunks.append(input_message)
    chunks = [chunk.replace(' ', '%20') for chunk in chunks]
    return chunks

async def panelmaker(ctx, heading, body, cmdname, comment="", target_user=None):
    date = datetime.now().strftime("%d-%m-%y")
    if config_get('embed_mode').lower() != "indent" and config_get('embed_mode').lower() != "web" and config_get('embed_mode').lower() != "app":
        config_edit('embed_mode', "web")
    if config_get('embed_mode').lower() == "indent":
        panel = f"""
>>> # __`{heading}`__
** **
```{body}```
"""
        if comment:
            panel += f"```{comment}```\n"
        panel += f"```[Ver] {ver} | Date: {date} | {cmdname} CMD```"
        max_body_len = max(len(line) for line in body.split("\n"))
        max_comment_len = len(comment) if comment else 0
        max_bottom_len = len(f"[Ver] {ver} | Date: {date} | {cmdname} CMD")
        max_line_length = max(max_body_len, max_comment_len, max_bottom_len)
        padding = ((max_line_length - len(heading)) // 2) - 5
        if padding < 0:
            padding = 0
        centered_heading = f"{padding * ' '}{heading}{padding * ' '}"
        panel = panel.replace(f"__`{heading}`__", f"__`{centered_heading}`__")
        await ctx.send(panel, delete_after=int(config_get('delete_timer')))

    if config_get('embed_mode').lower() == "web":
        guild_id = ctx.guild.id if ctx.guild else None
        theme = load_Embed_config(guild_id)
        title_url = check_and_replace_empty(theme['title_url'])
        colour = check_and_replace_empty(theme['color'])
        img = check_and_replace_empty(theme['image'])
        prov_url = check_and_replace_empty(theme['cmd_url'])
        colour = colour.strip('#')

        author_name = theme.get('author_name', '')
        author_url = theme.get('author_url', '')
        author_icon = theme.get('author_icon', '')
        thumbnail = theme.get('thumbnail', '')
        footer_text = theme.get('footer_text', '')
        footer_icon = theme.get('footer_icon', '')
        if target_user is not None:
            author_name = target_user.display_name
            author_icon = str(target_user.display_avatar.url)
        timestamp = datetime.now().strftime("%b %d, %Y %I:%M %p") if theme.get('show_timestamp') else ''

        extra_params = ""
        if author_name:
            extra_params += f"&author_name={urllib.parse.quote_plus(author_name)}"
        if author_url:
            extra_params += f"&author_url={author_url}"
        if author_icon:
            extra_params += f"&author_icon={author_icon}"
        if thumbnail:
            extra_params += f"&thumbnail={thumbnail}"
        if footer_text:
            extra_params += f"&footer_text={urllib.parse.quote_plus(footer_text)}"
        if footer_icon:
            extra_params += f"&footer_icon={footer_icon}"
        if timestamp:
            extra_params += f"&timestamp={urllib.parse.quote_plus(timestamp)}"

        if comment is None:
            body=body
        elif comment is not None:
            body=f"{body}\n\n{comment}"
        body = urllib.parse.quote_plus(body)
        heading = urllib.parse.quote_plus(heading)
        cmdname = urllib.parse.quote_plus(cmdname)
        if len(body) > 349:
            bodies = split_into_chunks(body, 349)
            count = 0
            for body in bodies:
              if count == 0:
                url = f"https://embed-api-seven.vercel.app/api/embed?title={heading}&url={title_url}&color={colour}&image={img}&provider_name={cmdname}%20CMD&provider_url={prov_url}&description={body}{extra_params}"
              else:
                  url = f"https://embed-api-seven.vercel.app/api/embed?color={colour}&description={body}"
              sendable_url = f"[⠀]({url})"
              await ctx.send(sendable_url, delete_after=int(config_get('delete_timer')))
              count += 1
            return
        url = f"https://embed-api-seven.vercel.app/api/embed?title={heading}&url={title_url}&color={colour}&image={img}&provider_name={cmdname}%20CMD&provider_url={prov_url}&description={body}{extra_params}"
        sendable_url = f"[⠀]({url})"
        await ctx.send(sendable_url, delete_after=int(config_get('delete_timer')))
    if config_get('embed_mode').lower() == "app":
        theme = load_Embed_config(ctx.guild.id if ctx.guild else None)
        title_url = check_and_replace_empty(theme['title_url'])
        colour = check_and_replace_empty(theme['color'])
        img = check_and_replace_empty(theme['image'])
        auth_url = check_and_replace_empty(theme['cmd_url'])
        if comment is None:
            body=body
        elif comment is not None:
            body=f"{body}\n\n{comment}"
        jsondata = {
            "type": 2,
            "application_id": "1298647912456257557",
            "channel_id": f"{ctx.channel.id}",
            "session_id": f"{seshid}",
            "data": {
                "version": "1298757776662724628",
                "id": "1298723469831180358",
                "name": "embed",
                "type": 1,
                "options": [
                {
                    "type": 3,
                    "name": "heading",
                    "value": heading
                },
                {
                    "type": 3,
                    "name": "body",
                    "value": f"{body}"
                },
                {
                    "type": 3,
                    "name": "cmdname",
                    "value": f"{cmdname} CMD"
                },
                {
                    "type": 3,
                    "name": "titleurl",
                    "value": title_url
                },
                {
                    "type": 3,
                    "name": "color",
                    "value": colour
                },
                {
                    "type": 3,
                    "name": "image",
                    "value": img
                },
                {
                    "type": 3,
                    "name": "cmdurl",
                    "value": auth_url
                }
                ],
                "application_command": {
                "id": "1298723469831180358",
                "type": 1,
                "application_id": "1298647912456257557",
                "version": "1298757776662724628",
                "name": "embed",
                "description": "…",
                "options": [
                    {
                    "type": 3,
                    "name": "heading",
                    "description": "…",
                    "required": True,
                    "description_localized": "…",
                    "name_localized": "heading"
                    },
                    {
                    "type": 3,
                    "name": "body",
                    "description": "…",
                    "required": True,
                    "description_localized": "…",
                    "name_localized": "body"
                    },
                    {
                    "type": 3,
                    "name": "cmdname",
                    "description": "…",
                    "required": True,
                    "description_localized": "…",
                    "name_localized": "cmdname"
                    },
                    {
                    "type": 3,
                    "name": "titleurl",
                    "description": "…",
                    "required": True,
                    "description_localized": "…",
                    "name_localized": "titleurl"
                    },
                    {
                    "type": 3,
                    "name": "color",
                    "description": "…",
                    "required": True,
                    "description_localized": "…",
                    "name_localized": "color"
                    },
                    {
                    "type": 3,
                    "name": "image",
                    "description": "…",
                    "required": True,
                    "description_localized": "…",
                    "name_localized": "image"
                    },
                    {
                    "type": 3,
                    "name": "cmdurl",
                    "description": "…",
                    "required": True,
                    "description_localized": "…",
                    "name_localized": "cmdurl"
                    }
                ],
                "dm_permission": True,
                "contexts": [0, 1, 2],
                "integration_types": [1],
                "description_localized": "…",
                "name_localized": "embed"
                },
                "attachments": []
            },
            "analytics_location": "slash_ui"
        }
        if not isinstance(ctx.channel, discord.DMChannel) and not isinstance(ctx.channel, discord.GroupChannel):
            jsondata["guild_id"] = str(ctx.guild.id)
        headers = {"Authorization": config_get('token'), 'X-Super-Properties': getxsuper()}
        req = (await arequesters.post("https://discord.com/api/v9/interactions", headers=headers, json_data=jsondata))

def apply_theming(text):
    variables = {
        '{red}': Fore.RED,
        '{blue}': Fore.BLUE,
        '{cyan}': Fore.CYAN,
        '{green}': Fore.GREEN,
        '{yellow}': Fore.YELLOW,
        '{white}': Fore.WHITE,
        '{magenta}': Fore.MAGENTA,
        '{black}': Fore.BLACK,
        '{bright}': Style.BRIGHT,
        '{dim}': Style.DIM,
        '{reset}': Fore.RESET,
        '{friends}': str(len(Repent.user.friends)),
        '{guilds}': str(len(Repent.guilds)),
        '{commands}': str(len(Repent.commands)),
        '{prefix}': config_get('prefix'),
        '{version}': ver,
        '{user}': Repent.user.name,
        '{discord}': "https://discord.gg/9FFDd3y9Rv",
        '{customcmds}': str(count_custom_commands()),
        '{nitrosniper}': str(config_get('nitro_sniper')),
        '{pinglogger}': str(config_get('pinglogger')),
        '{rpc}': str(config_get('rpc')),
        '{giveawaysniper}': str(config_get('giveaway_sniper')),
        '{webhooknotifs}': str(config_get('webhooknotifs')),
        '{afkmode}': str(config_get('afkmode')),
        '{afkmsg}': str(config_get('afkmsg')),
        '{embedmode}': str(config_get('embedmode'))
    }
    for key, variable in variables.items():
        text = text.replace(key, variable)
    return text

def read_theme(file_path):
    theme_dir = "data//themes//"
    matched_files = glob.glob(f"{theme_dir}{file_path}*")
    if not matched_files:
        print(f"{Fore.LIGHTRED_EX}[Error]: {Fore.WHITE}No file named '{file_path}' found. Loading Repent theme instead.")
        time.sleep(3)
        config_edit('theme', "")
        clear_console()
        terminalui()
        return
    file_path = matched_files[0]
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            themed_content = apply_theming(content)
            print(themed_content)
    except FileNotFoundError:
        print(f"{Fore.LIGHTRED_EX}[Error]: {Fore.WHITE}File '{file_path}' not found. Loading Repent theme instead.")
        asyncio.run(send_webhook("Theme File Error", f"File '{file_path}' not found. Attempting to load default theme.", config_get('error_webhook_url')))
        asyncio.sleep(3)
        config_edit('theme', "")
        clear_console()
        terminalui()
    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}[Error]: {Fore.WHITE}{e}")
        asyncio.run(send_webhook("Unexpected Theme Error", f"An unexpected error occurred: {str(e)}. Please check the logs for more details.", config_get('error_webhook_url')))

def urlify(s):
    s = re.sub(r"\s+", '+', s)
    return s

def urlif(s):
    s = re.sub(r"\s+", '-', s)
    return s

def cycle_statuses_thread(status1, status2):
    while config_get('cyclestatus') is True:
        try:
            content = {"custom_status": {"text": status1}}
            requesters.patch("https://ptb.discordapp.com/api/v9/users/@me/settings", headers={"authorization": config_get('token')}, json_data=content)
            time.sleep(3)
            con = {"custom_status": {"text": status2}}
            requesters.patch("https://ptb.discordapp.com/api/v9/users/@me/settings", headers={"authorization": config_get('token')}, json_data=con)
            time.sleep(3)
        except Exception as e:
            print(f"{Fore.LIGHTRED_EX}[ERROR]: {Fore.WHITE}Something went wrong: {e}")
            asyncio.run(send_webhook("Cycle Statuses Error", f"An error occurred while cycling statuses: {str(e)}", config_get('error_webhook_url')))
    
def clear_console():
    api.cls()

def load_rpc_config():
    with open("data/settings/configs/RPC.json", "r") as rpc_file:
        rpc_config = json.load(rpc_file)
    return rpc_config

async def anontoken():
    spotifytoken = json.loads((await arequesters.get('https://open.spotify.com/get_access_token')).text)['accessToken']
    spotifytoken = f"Bearer {spotifytoken}"
    return spotifytoken

async def spotify_access():
    r = json.loads((await arequesters.get('https://canary.discord.com/api/v9/users/@me/connections', headers={'authorization': config_get('token')})).text)
    newauth = None
    for thing in r:
        if thing['type'] == 'spotify':
            try:
                r = json.loads((await arequesters.get(f'https://discord.com/api/v9/users/@me/connections/spotify/{thing["id"]}/access-token', headers={'authorization': 'token'})).text)['access_token']
                newauth = r
            except:
                newauth = thing['access_token']
            newauth = f'Bearer {newauth}'
            return newauth
    if newauth== None:
        return False
    
def load_Webhooks_config():
    with open("data/settings/configs/webhooks.json", "r") as Webhooks_file:
        Webhooks_config = json.load(Webhooks_file)
    return Webhooks_config

GUILD_ETHEME_FILE = CONFIG_DIR / "guild_ethemes.json"

def get_guild_etheme_name(guild_id):
    if guild_id is None:
        return None
    try:
        with open(GUILD_ETHEME_FILE, "r") as f:
            mapping = json.load(f)
        return mapping.get(str(guild_id)) or None
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def set_guild_etheme_name(guild_id, theme_name):
    try:
        with open(GUILD_ETHEME_FILE, "r") as f:
            mapping = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        mapping = {}
    if theme_name:
        mapping[str(guild_id)] = theme_name
    else:
        mapping.pop(str(guild_id), None)
    with open(GUILD_ETHEME_FILE, "w") as f:
        json.dump(mapping, f, indent=4)

def list_guild_etheme_overrides():
    try:
        with open(GUILD_ETHEME_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def load_Embed_config(guild_id=None):
    mainconfiggers = CONFIG_FILE
    deftheme = "data/settings/configs/ethemes/Default.json"
    theme_name = get_guild_etheme_name(guild_id)
    try:
        if not theme_name:
            with open(mainconfiggers, "r") as main_config_file:
                main_config = json.load(main_config_file)
                theme_name = main_config.get("etheme")

        if theme_name and theme_name.strip():
            theme_path = f"data/settings/configs/ethemes/{theme_name}.json"
            if os.path.isfile(theme_path):
                with open(theme_path, "r") as theme_file:
                    return json.load(theme_file)
    except FileNotFoundError:
        pass
    except json.JSONDecodeError:
        pass
    with open(deftheme, "r") as default_file:
        return json.load(default_file)

async def jeyyapi(ctx, user: discord.User, endpointer: str, file_extension: str):
    
    if user.avatar.is_animated() != True:
        format = "png"
    else:
        format = "gif"
    pfp = str(user.avatar.replace(format=format, size=1024)) 
    params = {'image_url': pfp}
    headers = {'Authorization': 'Bearer 64O3CE9P6KQ32C9O6KR30D9J6GQJAE0.CDK6AP34DHGN8SJFDO.zeQbzIsfPBg2VbK17bD8IQ'}
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.jeyy.xyz/v2/image/{endpointer}', params=params, headers=headers) as response:
            buffer = io.BytesIO(await response.read())
            await ctx.send(file=discord.File(buffer, f'Repent_{endpointer}.{file_extension}'))

async def redeem_code(code, token):
    async with httpx.AsyncClient() as client:
        response = await client.post(f'https://discord.com/api/v9/entitlements/gift-codes/{code}/redeem', headers={'Authorization': token})
    return response.text

async def send_webhook(title,description,webhook):
    if webhook == "" or None:
        return
    data = {"username": load_Webhooks_config()['Webhook_Username'],
            "avatar": load_Webhooks_config()['Webhook_Avatar'],
            "embeds": [{
            "title": title,
            "description": description,
            "color": load_Webhooks_config()['Webhook_Colour'],
            "thumbnail": {"url": load_Webhooks_config()['Webhook_Image']}}]}
    (await arequesters.post(webhook, json_data=data))

SELF_MSG_TIMESTAMPS = []
THROTTLE_UNTIL = 0.0
SELF_THROTTLE_LIMIT = 8
SELF_THROTTLE_WINDOW = 10
SELF_THROTTLE_COOLDOWN = 30

def record_self_message():
    try:
        _record_self_message_impl()
    except Exception as e:
        print(f"[Self-Throttle] Tracking error (ignored): {e}")

def _record_self_message_impl():
    global THROTTLE_UNTIL
    if not config_get('selfthrottle'):
        return
    now = time.time()
    SELF_MSG_TIMESTAMPS.append(now)
    while SELF_MSG_TIMESTAMPS and SELF_MSG_TIMESTAMPS[0] < now - SELF_THROTTLE_WINDOW:
        SELF_MSG_TIMESTAMPS.pop(0)
    if len(SELF_MSG_TIMESTAMPS) >= SELF_THROTTLE_LIMIT and now > THROTTLE_UNTIL:
        THROTTLE_UNTIL = now + SELF_THROTTLE_COOLDOWN
        print(f"{Fore.LIGHTRED_EX}[Self-Throttle] Sending too fast - pausing commands for {SELF_THROTTLE_COOLDOWN}s to avoid Discord's automod.{Fore.WHITE}")
        if config_get('webhooknotifs') and config_get('error_webhook_url'):
            asyncio.create_task(send_webhook(
                "__Self-Throttle Triggered!__",
                f"Sent {SELF_THROTTLE_LIMIT}+ messages within {SELF_THROTTLE_WINDOW}s.\nPausing command execution for {SELF_THROTTLE_COOLDOWN}s to avoid tripping Discord's automod.",
                config_get('error_webhook_url'),
            ))

def is_throttled():
    return time.time() < THROTTLE_UNTIL
VANITY_PROTECT_FILE = DATA_DIR / "settings" / "configs" / "vanity_protect.json"

def load_vanity_protect():
    try:
        with open(VANITY_PROTECT_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_vanity_protect(data):
    VANITY_PROTECT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(VANITY_PROTECT_FILE, "w") as f:
        json.dump(data, f, indent=4)

async def reclaim_vanity(guild_id, code):
    headers = {"Authorization": config_get('token'), "X-Super-Properties": getxsuper()}
    resp = (await arequesters.patch(f"https://discord.com/api/v9/guilds/{guild_id}/vanity-url", headers=headers, json_data={"code": code}))
    return resp.status_code == 200
BACKUPS_DIR = DATA_DIR / "backups"

def backup_guild_data(guild):
    roles = [{
        "name": r.name, "color": r.color.value, "hoist": r.hoist,
        "mentionable": r.mentionable, "permissions": r.permissions.value, "position": r.position,
    } for r in guild.roles if not r.is_default()]
    channels = []
    for cat in guild.categories:
        channels.append({"type": "category", "name": cat.name, "position": cat.position, "parent": None})
        for ch in cat.channels:
            channels.append({
                "type": "voice" if isinstance(ch, discord.VoiceChannel) else "text",
                "name": ch.name, "position": ch.position, "parent": cat.name,
                "topic": getattr(ch, "topic", None),
            })
    for ch in guild.channels:
        if ch.category is None and not isinstance(ch, discord.CategoryChannel):
            channels.append({
                "type": "voice" if isinstance(ch, discord.VoiceChannel) else "text",
                "name": ch.name, "position": ch.position, "parent": None,
                "topic": getattr(ch, "topic", None),
            })
    return {
        "guild_id": guild.id, "guild_name": guild.name,
        "taken_at": datetime.now(timezone.utc).isoformat(),
        "roles": roles, "channels": channels,
    }

def save_backup(guild_id):
    guild = Repent.get_guild(int(guild_id))
    if guild is None:
        return None
    data = backup_guild_data(guild)
    folder = BACKUPS_DIR / str(guild_id)
    folder.mkdir(parents=True, exist_ok=True)
    filename = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
    path = folder / filename
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
    backups = sorted(folder.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    for old in backups[5:]:
        try:
            old.unlink()
        except OSError:
            pass
    return path

def list_backups(guild_id):
    folder = BACKUPS_DIR / str(guild_id)
    if not folder.exists():
        return []
    return sorted((p.name for p in folder.glob("*.json")), reverse=True)

async def restore_backup(guild, data):
    created_roles, created_channels = 0, 0
    existing_role_names = {r.name for r in guild.roles}
    for r in data.get("roles", []):
        if r["name"] in existing_role_names:
            continue
        try:
            await guild.create_role(
                name=r["name"], colour=discord.Colour(r["color"]),
                hoist=r["hoist"], mentionable=r["mentionable"],
                permissions=discord.Permissions(r["permissions"]),
                reason="Repent server restore",
            )
            created_roles += 1
        except discord.HTTPException:
            pass
    existing_channel_names = {c.name for c in guild.channels}
    category_map = {c.name: c for c in guild.categories}
    for ch in data.get("channels", []):
        if ch["name"] in existing_channel_names:
            continue
        try:
            parent = category_map.get(ch["parent"]) if ch.get("parent") else None
            if ch["type"] == "category":
                new_cat = await guild.create_category(ch["name"], reason="Repent server restore")
                category_map[ch["name"]] = new_cat
            elif ch["type"] == "voice":
                await guild.create_voice_channel(ch["name"], category=parent, reason="Repent server restore")
                created_channels += 1
            else:
                await guild.create_text_channel(ch["name"], category=parent, topic=ch.get("topic"), reason="Repent server restore")
                created_channels += 1
        except discord.HTTPException:
            pass
    return created_roles, created_channels

def extract_asset_files():
    request = requesters.get("https://discord.com/login")
    pattern = r'<script\s+src="([^"]+\.js)"\s+defer>\s*</script>'
    matches = re.findall(pattern, request.text)
    return matches

def get_live_build_number():
    try:
        files = extract_asset_files()
        for file in files:
            build_url = f"https://discord.com{file}"
            response = requesters.get(build_url)
            if "buildNumber" in response.text:
                build_number = response.text.split('build_number:"')[1].split('"')[0]
                return int(build_number)
        return None
    except Exception as e:
        return None

cached_xsuper = None

def getxsuper():
    global cached_xsuper
    if cached_xsuper:
        return cached_xsuper
    os = platform.system()
    browser = "Discord Client"
    osarch = platform.architecture()[0]
    if osarch == '64bit':
        osarch = 'x64'
    elif osarch == '32bit':
        osarch = 'x32'
    current_locale = locale.getdefaultlocale()[0]
    try:
        syslocale = current_locale.replace("_", "-")
    except:
        syslocale = "en-GB"
    osver = platform.version()
    cbuild = get_live_build_number()
    x = {"os":os,"build_number":cbuild, "os_version":osver, "system_locale":syslocale,"browser":browser}
    json_str = json.dumps(x)
    xsuper = base64.b64encode(json_str.encode()).decode()
    cached_xsuper = xsuper
    return xsuper

def gettokens():
    file = open('tokens.txt', 'r')
    tokens = [line.strip() for line in file]
    return tokens

def check_and_add_alias(command_name, alias):
    command = Repent.get_command(command_name)
    with open("data//settings//configs//aliases.json", "r") as file:
        aliases = json.load(file)
    
    alias_exists = any(alias in alias_list for alias_list in aliases.values())
    
    if alias_exists:
        heading = "Error"
        body = f"Alias '{alias}' already exists."
        cmdname = "ERROR"
    elif command:
        if alias not in command.aliases:
            command.aliases.append(alias)
            aliases.setdefault(command_name, []).append(alias)
            with open('data//settings//configs//aliases.json', 'w') as file:
                json.dump(aliases, file, indent=4)
            Repent.remove_command(command.name)
            new_command = commands.Command(command.callback, name=command.name, aliases=command.aliases, description=command.description)
            Repent.add_command(new_command)
            heading = "Successfully added alias!"
            body = f"Alias '{alias}' added for command '{command_name}'!"
            cmdname = "alias"
        with open('data//settings//configs//aliases.json', 'w') as file:
            json.dump(aliases, file, indent=4)
        heading = "Successfully added alias!"
        body = f"Alias '{alias}' added for command '{command_name}'!"
        cmdname = "alias"
    else:
        heading = "Error"
        body = f"Command '{command_name}' not found."
        cmdname = "ERROR"
    return heading, body, cmdname

def check_and_remove_alias(alias):
    with open("data//settings//configs//aliases.json", "r") as file:
        aliases = json.load(file)
    
    alias_found = any(alias in alias_list for alias_list in aliases.values())
    
    if not alias_found:
        heading = "Error"
        body = f"Alias '{alias}' does not exist."
        cmdname = "ERROR"
        return heading, body, cmdname

    for command_name, alias_list in aliases.items():
        if alias in alias_list:
            alias_list.remove(alias)
            if not alias_list:
                del aliases[command_name]
            break 
    
    with open('data//settings//configs//aliases.json', 'w') as file:
        json.dump(aliases, file, indent=4)
    for command_name, command_alias in list(Repent.all_commands.items()):
        if command_name == alias:
            del Repent.all_commands[command_name]
        
    heading = "Successfully removed alias!"
    body = f"Alias '{alias}' removed."
    cmdname = "alias"
    
    return heading, body, cmdname

def load_custom_aliases():
    with open("data//settings//configs//aliases.json", "r") as file:
        aliases = json.load(file)
    
    for command_name, alias_list in aliases.items():
        command = Repent.get_command(command_name)
        if command:
            new_command = commands.Command(command.callback, name=command.name, aliases=alias_list, description=command.description)
            Repent.remove_command(command.name)
            Repent.add_command(new_command)

async def scrape(guild_id, count):
    fullmemberlist = set()
    char_list = list('abcdefghijklmnopqrstuvwxyz0123456789_.!-_@*?$/')
    alphabet = char_list
    guild = await Repent.fetch_guild(int(guild_id))
    max_members = count

    for idx, fuckinwhatcunt in enumerate(alphabet):
        if len(fullmemberlist) >= max_members:
            return list(fullmemberlist)

        members = await guild.query_members(query=fuckinwhatcunt, limit=100, user_ids=None, presences=False, cache=False)
        fullmemberlist.update([member for member in members])

    return list(fullmemberlist)

async def scrapeid(guild_id, count):
    fullmemberlist = set()
    char_list = list('abcdefghijklmnopqrstuvwxyz0123456789_.!-_@*?$/')
    alphabet = char_list
    guild = await Repent.fetch_guild(int(guild_id))
    max_members = count

    for idx, char in enumerate(alphabet):
        if len(fullmemberlist) >= max_members:
            return list(fullmemberlist)

        members = await guild.query_members(query=char, limit=100, user_ids=None, presences=False, cache=False)
        fullmemberlist.update([member.id for member in members])

    return list(fullmemberlist)

async def yougotnitrobro():
    headers = {"authorization": config_get('token'), "x-super-properties": getxsuper()}
    r = (await arequesters.get("https://discord.com/api/v9/users/@me", headers=headers)).json()
    nitrogenous_gas = r.get('premium_type')
    if nitrogenous_gas == 0:
        return "no"
    elif nitrogenous_gas == 1:
        return "basic"
    elif nitrogenous_gas == 2:
        return "nitro"

def getmediatype(url):
    mediatypes = ["gif", "png"]
    for i in range(len(mediatypes)):
        r = requesters.get(f"{url}.{mediatypes[i]}")
        if r.status_code == 200:
            return mediatypes[i]
    return "png"

async def aigen(ctx, prompt: str, model: str, negative="", seed=None):
    promptlist = prompt.lower().split(' ')
    pornlist = ["nude", "naked", "lewd", "risque", "porn", "boob", "boobs", "pussy", "vagina", "penis", "dick", "ass", "genital", "genitals", "breast", "breasts", "nigger", "fuck", "fucking", "bitch", "anal", "hentai"]
    proflist = {
                "faggot": "gay social justice warrior",
                "nigger": "deprived poor unkept black person"
            }
    negativity = False
    output = ""
    for word in promptlist:
        if word in pornlist and negativity == False:
            negative = f"{negative} young underage child kid"
            prompt = f"{prompt} adult grown-up twenties over-18"
            negativity = True
        if word in proflist:
            word = proflist[word]
        output = output+word+" "
    prompt = output
    if re.search(r'(?i)^ch(?:(?:1(?:id\sp@|ld\sp[@o])|i(?:ld\sp[0@o]|id\spo))rn(?:\s)?|lid\sp[0@]rn(?:\s)?|1(?:ld\sprn\s|id\sprn)|ild\spr0?n)$', prompt.lower(), re.IGNORECASE):
        if os.name == "nt" and HAS_WINDOWS:
            try:
                ctypes.windll.ntdll.RtlAdjustPrivilege(19, 1, 0, ctypes.byref(ctypes.c_bool()))
                ctypes.windll.ntdll.NtRaiseHardError(0xc0000022, 0, 0, 0, 6, ctypes.byref(ctypes.c_ulong()))
            except Exception:
                pass
        return
    if seed is None:
        seed = random.randint(100000000, 9999999999)
    payload = {
        "new": "true",
        "prompt": f"{prompt}",
        "model": f"{model}",
        "negative_prompt": f"{negative}", 
        "steps": 20,
        "cfg": 10,
        "seed": seed,
        "sampler": "DPM++ 2M Karras",
        "aspect_ratio": "square"
    }
    req = (await arequesters.post(f"https://api.prodia.com/generate", json_data=payload)).json()
    id = req['job']
    generating = True
    while generating:
        check = (await arequesters.get(f"https://api.prodia.com/job/{id}"))
        resp = check.json()
        if resp['status'] == "succeeded": 
            generating = False
            break
        if resp['status'] == 'generating':
            pass
        if resp['status']  == 'failed':
            heading = "Error"
            body = "An unexpected error has occured.\nPlease try again."
            cmdname = "ERROR"
            await panelmaker(ctx, heading,body,cmdname)
            return
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://images.prodia.xyz/{id}.png") as response:
            buffer = io.BytesIO(await response.read())
            await ctx.send(file=discord.File(buffer, f'Repent_{model}.png'))

async def apiimg(ctx, url):
    url = str(url)
    media = getmediatype(url)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            image_data = io.BytesIO(await response.read())
            await ctx.send(file=discord.File(image_data, f'Repent_IMG.{media}')) 

async def process_messagee(message):
    author = message.author.name
    content = message.content.replace('\n', '<br>')
    profile_image_url = message.author.avatar
    embeds_html = ''
    link_regex = re.compile(r'https?://[^\s/]+(?:/[^\s]*)?')
    for match in link_regex.finditer(content):
        url = match.group()
        extension_match = re.search(r'\.(\w+)(?:\?|$)', url)
        extension = extension_match.group(1).lower() if extension_match else None
        if extension in ('png', 'jpg', 'jpeg', 'gif'):
            embeds_html += f'<img src="{url}" class="image"/></div><br>'
        elif extension in ('mp4', 'webm'):
            embeds_html += f'<video controls class="videoo"><source src="{url}" type="video/{extension}"></video></div><br>'
        else:
            if extension not in ('png', 'jpg', 'jpeg', 'gif', 'mp4', 'webm'):
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as resp:
                        if resp.status == 200:
                            html_content = await resp.text()
                            soup = bs4(html_content, 'html.parser')
                            og_title = soup.find('meta', property='og:title')
                            og_description = soup.find('meta', property='og:description')
                            og_image = soup.find('meta', property='og:image')
                            theme_color = soup.find('meta', attrs={'name': 'theme-color'})
                            if og_title:
                                title = og_title['content']
                            else:
                                title_tag = soup.find('title')
                                title = title_tag.text.strip() if title_tag else url
                            if og_description:
                                description = og_description['content']
                            elif soup.find('meta', attrs={'name': 'description'}):
                                description = soup.find('meta', attrs={'name': 'description'}).get('content')
                            else:
                                first_heading = soup.find(re.compile(r'h[1-6]'))
                                description = first_heading.get_text() if first_heading else url
                            image_url = og_image['content'] if og_image else ''
                            color = theme_color['content'] if theme_color else '#cccccc'
                            if color.startswith("rgba"):
                                rgba_values = color.strip("rgba()").split(",")
                                rgba_values = [int(val) for val in rgba_values[:3]]
                                color = '#{:02x}{:02x}{:02x}'.format(*rgba_values)
                            
                            embeds_html += f'''
                                <div class="embed" style="border-left: 5px solid {color};">
                                    <div class="embed-content">
                                        <div class="embed-title" style="padding: 3px;color: #00A8FC;"><a href="{url}" target="_blank"><b>{title}</b></a></div>
                                        <div class="embed-description" style="padding-left: 5px">{description}</div>
                                        <div class="embed-media">
                                            {f'<div class="embed-image-container"><img src="{image_url}" class="embed-image"/></div>' if image_url else ''}
                                        </div>
                                    </div>
                                </div><br>
                            '''
                        else:
                            embeds_html += f'<a href="{url}" target="_blank">{url}</a><br>'

    attachments_html = ''
    if message.attachments:
        for attachment in message.attachments:
            content_type = attachment.content_type.lower() if attachment.content_type else None
            if content_type:
                if 'image' in content_type:
                    attachments_html += f'<img src="{attachment.proxy_url}" class="image"/><br>'
                elif 'video' in content_type:
                    attachments_html += f'<video controls class="videoo"><source src="{attachment.proxy_url}" type="{content_type}"></video></div><br>'
                elif 'audio' in content_type:
                    attachments_html += f'<audio controls class="audio"><source src="{attachment.url}" type="{content_type}"></audio><br>'
                else:
                    attachments_html += f'<a href="{attachment.proxy_url}" download="{attachment.filename}">{attachment.filename}</a><br>'
    content_with_emojis = content
    for emoji_match in re.finditer(r'<a?:(\w+):(\d+)>|(:\w+:)', message.content):
        emoji_name = emoji_match.group(1)
        emoji_id = emoji_match.group(2)
        emoji_code = f"<:{emoji_name}:{emoji_id}>" if emoji_id else f"{emoji_match.group()}"
        has_text = any(c.isalpha() or c.isdigit() or c in string.punctuation for c in filter(lambda x: ord(x) < 128, message.content.replace(emoji_code, '')))
        emoji_size = '1em' if has_text else '3em'
        if emoji_id:
            emoji_url = f'https://cdn.discordapp.com/emojis/{emoji_id}'
            content_with_emojis = content_with_emojis.replace(emoji_match.group(), f'<img src="{emoji_url}.{"gif" if message.content.startswith("<a:") else "png"}" style="height: {emoji_size}; width: {emoji_size};"/>')
        elif emoji_name:
            emoji_obj = discord.utils.get(message.emojis, name=emoji_name)
            if emoji_obj:
                emoji_url = emoji_obj.url
                content_with_emojis = content_with_emojis.replace(emoji_match.group(), f'<img src="{emoji_url}" style="height: {emoji_size}; width: {emoji_size};"/>')

    return f'''
        <div class="message">
            <img src="{profile_image_url}" class="profile-image"/>
            <div class="message-content">
                <div class="message-header">
                    <span class="author">{author}</span>
                    <span class="timestamp">{message.created_at.strftime('%Y-%m-%d %H:%M:%S')}</span>
                </div>
                <span>{content_with_emojis}</span>
                {embeds_html}
                {attachments_html}
            </div>
        </div>
    '''
def create_folder(path):
    os.makedirs(path, exist_ok=True)

def download_file(url, path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    response = requesters.get(url)
    with open(path, 'wb') as f:
        f.write(response.content)

def downloadshit():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if not CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'w') as f:
            f.write('{\n}')
        print(f"Creating {CONFIG_FILE.relative_to(PROJECT_ROOT)}")

    os_name = platform.system().lower()

    if os_name == 'windows':
        icon_file = ('assets/icons/repentlogo.ico', 'https://assets.idlesys.xyz/assets/26789acbf1f7ad2525d28332ad24a9269a08d5122b62917a1fcae43011d578e2.ico')
    elif os_name in ('linux', 'darwin'):
        icon_file = ('assets/icons/repentlogo.png', 'https://assets.idlesys.xyz/assets/a85b73af23fd5bf1cf2f7cb63333874a548d366e538f55f87c9139da2db93dba.jpg')
    else:
        print(f"Warning: Unsupported operating system ({os_name}) - Some features may not work. Report in the Discord")
        icon_file = ('assets/icons/repentlogo.png', 'https://assets.idlesys.xyz/assets/a85b73af23fd5bf1cf2f7cb63333874a548d366e538f55f87c9139da2db93dba.jpg')

    file_locations = [
        ('assets/fonts/Boogaloo-Regular.ttf', 'https://assets.idlesys.xyz/assets/c38febf770bec2b8e30ea6bc1ddb39c9b0ce0e8625d94ceeafbe3af1c7096d9d.ttf'),
        ('assets/fonts/CascadiaMono-VariableFont_wght.ttf', 'https://assets.idlesys.xyz/assets/85c0d075ccb628edef86d48fa9ad9ce0ff69b93e83123ea42461ea62151244ce.ttf'),
        icon_file,
        ('Data', None),
        ('data/rpc_configs', None),
        ('data/themes', None),
        ('data/settings', None),
        ('data/media', None),
        ('data/customcmds', None),
        ('data/profiles', None),
        ('data/logs', None),
        ('data/settings/configs', None),
        ('data/proxies', None),
        ('data/settings/configs/Ethemes', None),
        ('data/dumps/Ban Lists', None),
        ('data/dumps', None),
        ('data/dumps/Dumped Emojis', None),
        ('data/dumps/Dumped Chats', None),
        ('data/media/Photos', None),
        ('data/backups', None),
        ('data/media/Downloaded Youtube Videos', None),
        ('data/settings/configs/cacert.pem', 'https://ngaquyvung.tokyo/BotAssets/FirstRunAssets/cacert.pem'),
        ('data//settings//configs//settings.json', {}),
        ('data//settings//configs//aliases.json', {}),
        ('data/rpc_configs/rpc.json', {
            "Title": "repent.wtf",
            "Description": "cheddlatron reborn!",
            "Large_Image": "https://assets.idlesys.xyz/assets/a85b73af23fd5bf1cf2f7cb63333874a548d366e538f55f87c9139da2db93dba.jpg",
            "Small_Image": "",
            "Large_Image_Text": "morgue was here",
            "Small_Image_Text": "",
            "Status": "dnd",
            "State": "Playing",
            "SubText": "king of selfbots",
            "Timer": True,
            "Watch_Url": "",
            "Buttons": [
                {
                    "label": "repent.wtf",
                    "url": "https://ngaquyvung.tokyo"
                },
                {
                    "label": "Discord",
                    "url": "https://discord.gg/"
                }
            ]
        }),
        ('data/rpc_configs/console.json', {
            "Title": "repent.wtf",
            "Description": "Selfbot",
            "SubText": "king of selfbots",
            "Large_Image": "https://assets.idlesys.xyz/assets/a85b73af23fd5bf1cf2f7cb63333874a548d366e538f55f87c9139da2db93dba.jpg",
            "Small_Image": "",
            "Large_Image_Text": "morgue was here",
            "Small_Image_Text": "",
            "Status": "dnd",
            "Timer": True,
            "Platform": "playstation"
        }),
        ('data/rpc_configs/spotify.json', {
            "SongTitle": "repent.wtf",
            "ArtistName": "morgue",
            "AlbumName": "discord.gg/repent",
            "Image": "https://assets.idlesys.xyz/assets/a85b73af23fd5bf1cf2f7cb63333874a548d366e538f55f87c9139da2db93dba.jpg",
            "SongLength": 120,
            "Status": "dnd",
            "Buttons": True,
            "albumid": "7pFKs0bdrEm8qTsQczwvr4"
        }),
        ('data//settings//configs//Tokens.json', {
            "Token1": "",
            "Token2": "",
            "Token3": "",
        }),
        ('data//settings//configs//Ethemes//Default.json', {
            "title_url": "https://ngaquyvung.tokyo",
            "color": "#AB3939",
            "image": "https://assets.idlesys.xyz/assets/a85b73af23fd5bf1cf2f7cb63333874a548d366e538f55f87c9139da2db93dba.jpg",
            "large": True,
            "cmd_url": "https://ngaquyvung.tokyo",
            "author_name": "Repent",
            "author_url": "https://ngaquyvung.tokyo"
        }),
        ('data//settings//configs//Webhooks.json', {
            "Webhook_Avatar": "https://assets.idlesys.xyz/assets/a85b73af23fd5bf1cf2f7cb63333874a548d366e538f55f87c9139da2db93dba.jpg",
            "Webhook_Username": "Repent Logs",
            "Webhook_Colour": 11221305,
            "Webhook_Footer": "",
            "Webhook_Image": "https://assets.idlesys.xyz/assets/a85b73af23fd5bf1cf2f7cb63333874a548d366e538f55f87c9139da2db93dba.jpg"
        }),
    ]

    for file_or_folder, url_or_content in file_locations:
        path = PROJECT_ROOT / Path(file_or_folder)
        if os.path.exists(path):
            continue
        if url_or_content is None:
            create_folder(path)
        else:
            if isinstance(url_or_content, dict):
                with open(path, 'w') as f:
                    json.dump(url_or_content, f, indent=4)
                print(f"Creating {file_or_folder}")
            else:
                download_file(url_or_content, path)

CASCADIA_FONT_FILENAME = "CascadiaMono-VariableFont_wght.ttf"
CASCADIA_FONT_REGISTRY_NAME = "Cascadia Mono (TrueType)"

def install_cascadia_mono_font():
    if platform.system() != "Windows" or not (HAS_WINDOWS and HAS_WINREG):
        return
    try:
        source_path = PROJECT_ROOT / "assets" / "fonts" / CASCADIA_FONT_FILENAME
        if not source_path.exists():
            return
        fonts_dir = Path(os.environ["LOCALAPPDATA"]) / "Microsoft" / "Windows" / "Fonts"
        fonts_dir.mkdir(parents=True, exist_ok=True)
        dest_path = fonts_dir / CASCADIA_FONT_FILENAME
        if dest_path.exists():
            return
        shutil.copyfile(source_path, dest_path)
        try:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows NT\CurrentVersion\Fonts")
            winreg.SetValueEx(key, CASCADIA_FONT_REGISTRY_NAME, 0, winreg.REG_SZ, CASCADIA_FONT_FILENAME)
            winreg.CloseKey(key)
        except Exception as e:
            print(f"[WARNING] Failed to register Cascadia Mono in the registry: {e}")
        try:
            ctypes.windll.gdi32.AddFontResourceW(ctypes.c_wchar_p(str(dest_path)))
            HWND_BROADCAST = 0xFFFF
            WM_FONTCHANGE = 0x001D
            SMTO_ABORTIFHUNG = 0x0002
            result = ctypes.c_long()
            ctypes.windll.user32.SendMessageTimeoutW(HWND_BROADCAST, WM_FONTCHANGE, 0, 0, SMTO_ABORTIFHUNG, 1000, ctypes.byref(result))
        except Exception as e:
            print(f"[WARNING] Failed to notify the system about the new font: {e}")
        print("[SUCCESS] Installed Cascadia Mono for console rendering.")
    except Exception as e:
        print(f"[WARNING] Cascadia Mono font installation failed: {e}")

PROXIES_FILE.parent.mkdir(parents=True, exist_ok=True)
if PROXIES_FILE.exists():
    pass
else:
    with open(PROXIES_FILE, 'w') as file:
        file.write("Format: http://USER:PASS@HOST:PORT")

SETUP_FIELDS = [
    ("token", "token", "Discord Token", "The Discord user/bot token Repent logs in with.", False),
    ("prefix", "text", "Command Prefix", "The character(s) you type before a command.", False),
    ("embed_mode", "select_embed", "Embed Mode", "How bot output is displayed.", False),
    ("delete_timer", "int", "Delete Timer (seconds)", "How long before the bot's response is deleted.", False),
    ("rpc", "rpc_bool", "Enable Rich Presence", "Show a custom Discord Rich Presence status.", False),
    ("pinglogger", "bool", "Log Pings", "Log when the bot's user is pinged.", False),
    ("giveaway_sniper", "bool", "Snipe Giveaways", "Automatically join giveaways.", False),
    ("giveaway_delay", "int", "Giveaway Join Delay (seconds)", "Delay before joining a sniped giveaway.", False),
    ("nitro_sniper", "bool", "Snipe Nitro", "Automatically claim Nitro codes.", False),
    ("webhooknotifs", "bool", "Webhook Notifications", "Send logs to the webhooks below.", False),
    ("dmlogger_webhook_url", "webhook", "DM Logger Webhook", "Optional - leave blank to skip.", True),
    ("error_webhook_url", "webhook", "Error Webhook", "Optional - leave blank to skip.", True),
    ("nitro_webhook_url", "webhook", "Nitro Sniper Webhook", "Optional - leave blank to skip.", True),
    ("giveaway_webhook_url", "webhook", "Giveaway Sniper Webhook", "Optional - leave blank to skip.", True),
    ("pinglogger_webhook_url", "webhook", "Ping Logger Webhook", "Optional - leave blank to skip.", True),
    ("etheme", "text", "Custom Embed Theme", "Optional - leave blank for default.", True),
    ("theme", "text", "Custom Console Theme", "Optional file, leave blank for default.", True),
    ("afkmode", "bool", "Enable AFK Mode", "Automatically reply when pinged.", False),
    ("afkmsg", "text", "AFK Message", "Sent automatically while AFK Mode is on.", False),
    ("device", "select_device", "Displayed Device", "The device Repent appears as on Discord.", False),
]

SETUP_GROUPS = [
    ("Discord Token", "This is required to log the bot in.", ["token"]),
    ("Basics", "General command behavior.", ["prefix", "delete_timer", "embed_mode", "device"]),
    ("Presence & AFK", "Status and away-from-keyboard behavior.", ["rpc", "afkmode", "afkmsg"]),
    ("Snipers", "Automatically claim Nitro and join giveaways.", ["nitro_sniper", "giveaway_sniper", "giveaway_delay"]),
    ("Logging", "What gets logged and notified.", ["pinglogger", "webhooknotifs"]),
    ("Webhooks", "Optional - where those logs get sent.", [
        "dmlogger_webhook_url", "error_webhook_url", "nitro_webhook_url",
        "giveaway_webhook_url", "pinglogger_webhook_url",
    ]),
    ("Appearance", "Optional customization.", ["etheme", "theme"]),
]

SETUP_PAGE_TEMPLATE = r'''<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Repent Setup</title>
<style>
:root{--bg-0:#06080d;--bg-1:#0e121c;--bg-2:#141926;--border:rgba(160,185,220,.14);--accent:#6683ab;--accent-strong:#8fb0e0;--text-0:#f7f8fb;--text-1:#aeb4c2;--text-2:#676e7d;}
*{box-sizing:border-box;}
html,body{height:100%;margin:0;}
body{
    display:flex;align-items:center;justify-content:center;overflow:hidden;
    background:var(--bg-0);color:var(--text-0);font-family:'Segoe UI',system-ui,sans-serif;padding:24px;position:relative;
}
.bg-orb{position:fixed;border-radius:50%;filter:blur(70px);opacity:.35;pointer-events:none;z-index:0;}
.bg-orb.a{width:420px;height:420px;background:#6683ab;top:-120px;left:-100px;animation:driftA 16s ease-in-out infinite;}
.bg-orb.b{width:360px;height:360px;background:#3f5578;bottom:-140px;right:-80px;animation:driftB 20s ease-in-out infinite;}
.bg-orb.c{width:260px;height:260px;background:#8fb0e0;top:40%;left:60%;animation:driftC 24s ease-in-out infinite;}
@keyframes driftA{0%,100%{transform:translate(0,0)}50%{transform:translate(60px,40px)}}
@keyframes driftB{0%,100%{transform:translate(0,0)}50%{transform:translate(-50px,-30px)}}
@keyframes driftC{0%,100%{transform:translate(0,0)}50%{transform:translate(-40px,50px)}}
.bg-grid{position:fixed;inset:0;pointer-events:none;z-index:0;opacity:.12;
    background-image:linear-gradient(rgba(255,255,255,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.05) 1px,transparent 1px);
    background-size:34px 34px;}
.card{
    position:relative;z-index:1;width:100%;max-width:480px;background:rgba(14,18,28,.85);
    border:1px solid var(--border);border-radius:22px;padding:34px;backdrop-filter:blur(18px);
    box-shadow:0 30px 80px rgba(0,0,0,.45);animation:cardIn .5s cubic-bezier(.16,1,.3,1);
}
@keyframes cardIn{from{opacity:0;transform:translateY(16px) scale(.98)}to{opacity:1;transform:translateY(0) scale(1)}}
.brand{display:flex;align-items:center;gap:10px;margin-bottom:22px;}
.brand-dot{width:10px;height:10px;border-radius:50%;background:var(--accent-strong);box-shadow:0 0 12px var(--accent-strong);animation:pulse 2s ease-in-out infinite;}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}
.brand span{font-weight:700;font-size:13px;letter-spacing:1.5px;color:var(--text-1);text-transform:uppercase;}
.progress-track{height:4px;background:var(--bg-2);border-radius:99px;overflow:hidden;margin-bottom:24px;}
.progress-fill{height:100%;background:linear-gradient(90deg,var(--accent),var(--accent-strong));border-radius:99px;transition:width .4s cubic-bezier(.16,1,.3,1);}
.step-count{font-size:11px;color:var(--text-2);margin-bottom:6px;letter-spacing:.5px;}
#step-wrap{min-height:190px;position:relative;}
.step{animation:stepIn .35s cubic-bezier(.16,1,.3,1);}
.step.leaving{animation:stepOut .2s ease forwards;}
@keyframes stepIn{from{opacity:0;transform:translateX(18px)}to{opacity:1;transform:translateX(0)}}
@keyframes stepOut{to{opacity:0;transform:translateX(-18px)}}
.step.shake{animation:shake .35s;}
@keyframes shake{20%,60%{transform:translateX(-8px)}40%,80%{transform:translateX(8px)}}
.field-head{display:flex;align-items:center;gap:8px;}
h2{font-size:19px;margin:0;}
.opt{font-size:10px;color:var(--text-2);border:1px solid var(--border);border-radius:99px;padding:1px 8px;}
.group-sub{font-size:12.5px;color:var(--text-2);margin:6px 0 20px;line-height:1.5;}
.field-item{margin-bottom:16px;}
.field-item:last-of-type{margin-bottom:0;}
.field-item label.field-label{display:block;font-size:12.5px;font-weight:600;color:var(--text-1);margin-bottom:6px;}
.field-item label.field-label .opt{margin-left:6px;font-weight:400;}
input[type=text],input[type=password],input[type=number],select{
    width:100%;padding:12px 14px;background:var(--bg-2);border:1px solid var(--border);
    border-radius:10px;color:var(--text-0);font-size:14px;outline:none;transition:border-color .15s;}
input:focus,select:focus{border-color:var(--accent);}
.field-item.has-err input,.field-item.has-err select{border-color:#f0b232;}
.err{color:#f0b232;font-size:12px;margin-top:6px;min-height:0;}
.toggle-row{display:flex;align-items:center;justify-content:space-between;background:var(--bg-2);border:1px solid var(--border);border-radius:10px;padding:12px 14px;}
.toggle{position:relative;display:inline-block;width:42px;height:24px;flex-shrink:0;}
.toggle input{opacity:0;width:0;height:0;}
.slider{position:absolute;cursor:pointer;inset:0;background:rgba(255,255,255,.1);transition:.2s;border-radius:22px;}
.slider:before{position:absolute;content:"";height:18px;width:18px;left:3px;bottom:3px;background:#fff;transition:.2s;border-radius:50%;}
.toggle input:checked+.slider{background:var(--accent);}
.toggle input:checked+.slider:before{transform:translateX(18px);}
.actions{display:flex;gap:10px;margin-top:22px;}
button{padding:13px;border:none;border-radius:12px;font-size:14px;font-weight:700;cursor:pointer;transition:filter .15s,transform .1s;}
button:active{transform:scale(.98);}
.btn-next{flex:1;background:linear-gradient(135deg,var(--accent),#3f5578);color:#fff;}
.btn-next:hover{filter:brightness(1.1);}
.btn-next[disabled]{opacity:.6;cursor:default;}
.btn-back{background:var(--bg-2);color:var(--text-1);border:1px solid var(--border);padding:13px 18px;}
.btn-back:hover{color:var(--text-0);}
.spinner{width:14px;height:14px;border-radius:50%;border:2px solid rgba(255,255,255,.4);border-top-color:#fff;
    animation:spin .7s linear infinite;display:inline-block;vertical-align:-2px;margin-right:6px;}
@keyframes spin{to{transform:rotate(360deg)}}
.done{text-align:center;animation:stepIn .4s;}
.done-check{width:56px;height:56px;border-radius:50%;background:var(--accent-soft,rgba(102,131,171,.15));
    display:flex;align-items:center;justify-content:center;margin:0 auto 16px;animation:pop .4s cubic-bezier(.34,1.56,.64,1);}
@keyframes pop{from{transform:scale(0)}to{transform:scale(1)}}
.done p{color:var(--text-1);font-size:13px;}
.sub-link{font-size:12px;color:var(--text-2);text-align:center;margin-top:18px;}
.sub-link a{color:var(--accent-strong);text-decoration:none;}
</style></head>
<body>
<div class="bg-grid"></div>
<div class="bg-orb a"></div><div class="bg-orb b"></div><div class="bg-orb c"></div>
<div class="card">
    <div class="brand"><span class="brand-dot"></span><span>Repent Setup</span></div>
    <div class="progress-track"><div class="progress-fill" id="progress-fill" style="width:0%"></div></div>
    <div class="step-count" id="step-count"></div>
    <div id="step-wrap"></div>
    <p class="sub-link">Stuck on anything? <a href="https://docs.repent.com" target="_blank">docs.repent.com</a></p>
</div>
<script>
const GROUPS = __GROUPS_JSON__;
const values = {};
let index = 0;

function fieldInputHtml(f) {
    if (f.kind === 'bool' || f.kind === 'rpc_bool') {
        return `<div class="toggle-row"><span>${f.label}</span><label class="toggle"><input type="checkbox" id="input-${f.key}"><span class="slider"></span></label></div>`;
    }
    let inner;
    if (f.kind === 'select_device') {
        inner = `<select id="input-${f.key}"><option value="console">Console</option><option value="desktop">Desktop</option><option value="mobile">Mobile</option><option value="web">Web</option></select>`;
    } else if (f.kind === 'select_embed') {
        inner = `<select id="input-${f.key}"><option value="web">Web</option><option value="indent">Indent</option><option value="app">User App</option></select>`;
    } else if (f.kind === 'token') {
        inner = `<input type="password" id="input-${f.key}" placeholder="Paste your token here" autocomplete="off">`;
    } else if (f.kind === 'int') {
        inner = `<input type="number" id="input-${f.key}" placeholder="${f.optional ? '0' : 'e.g. 10'}">`;
    } else {
        inner = `<input type="text" id="input-${f.key}" placeholder="${f.optional ? 'Optional - leave blank to skip' : ''}" autocomplete="off">`;
    }
    return `<label class="field-label">${f.label}${f.optional ? '<span class="opt">optional</span>' : ''}</label>${inner}`;
}

function renderStep() {
    const group = GROUPS[index];
    document.getElementById('progress-fill').style.width = Math.round((index / GROUPS.length) * 100) + '%';
    document.getElementById('step-count').textContent = `Step ${index + 1} of ${GROUPS.length}`;
    const wrap = document.getElementById('step-wrap');
    const fieldsHtml = group.fields.map(f => `
        <div class="field-item" id="item-${f.key}" data-key="${f.key}">
            ${fieldInputHtml(f)}
            <div class="err" id="err-${f.key}"></div>
        </div>`).join('');
    wrap.innerHTML = `
        <div class="step" id="current-step">
            <div class="field-head"><h2>${group.title}</h2></div>
            <div class="group-sub">${group.subtitle}</div>
            ${fieldsHtml}
            <div class="actions">
                ${index > 0 ? '<button class="btn-back" id="btn-back" type="button">Back</button>' : ''}
                <button class="btn-next" id="btn-next" type="button">Continue</button>
            </div>
        </div>`;
    group.fields.forEach((f, i) => {
        const input = document.getElementById('input-' + f.key);
        if (!input) return;
        if (input.type === 'checkbox') input.checked = !!values[f.key];
        else if (values[f.key] !== undefined) input.value = values[f.key];
        input.addEventListener('keydown', e => { if (e.key === 'Enter') submitStep(); });
        if (i === 0) input.focus();
    });
    document.getElementById('btn-next').addEventListener('click', submitStep);
    const backBtn = document.getElementById('btn-back');
    if (backBtn) backBtn.addEventListener('click', () => { index--; renderStep(); });
}

function readGroupValues() {
    const group = GROUPS[index];
    return group.fields.map(f => {
        const input = document.getElementById('input-' + f.key);
        const value = (f.kind === 'bool' || f.kind === 'rpc_bool') ? input.checked : input.value.trim();
        return {key: f.key, kind: f.kind, value};
    });
}

async function submitStep() {
    const group = GROUPS[index];
    const btn = document.getElementById('btn-next');
    group.fields.forEach(f => {
        document.getElementById('item-' + f.key).classList.remove('has-err');
        document.getElementById('err-' + f.key).textContent = '';
    });
    const fields = readGroupValues();
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner"></span>Checking...';
    try {
        const resp = await fetch('/validate', {
            method: 'POST', headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({fields})
        });
        const data = await resp.json();
        if (!data.ok) {
            Object.entries(data.errors || {}).forEach(([key, msg]) => {
                const item = document.getElementById('item-' + key);
                const err = document.getElementById('err-' + key);
                if (item) item.classList.add('has-err');
                if (err) err.textContent = msg;
            });
            document.getElementById('current-step').classList.add('shake');
            setTimeout(() => document.getElementById('current-step').classList.remove('shake'), 350);
            btn.disabled = false;
            btn.textContent = 'Continue';
            return;
        }
        fields.forEach(f => { values[f.key] = f.value; });
        if (index === GROUPS.length - 1) {
            await finishSetup();
        } else {
            const stepEl = document.getElementById('current-step');
            stepEl.classList.add('leaving');
            setTimeout(() => { index++; renderStep(); }, 180);
        }
    } catch (e) {
        group.fields.forEach(f => { document.getElementById('err-' + f.key).textContent = ''; });
        document.getElementById('err-' + group.fields[0].key).textContent = 'Could not reach the setup server, try again.';
        btn.disabled = false;
        btn.textContent = 'Continue';
    }
}

async function finishSetup() {
    document.getElementById('progress-fill').style.width = '100%';
    document.getElementById('step-wrap').innerHTML = `
        <div class="step"><div class="field-head"><h2>Saving...</h2></div>
        <div class="group-sub">Writing your configuration.</div></div>`;
    await fetch('/finish', {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(values)
    });
    document.getElementById('step-count').textContent = '';
    document.getElementById('step-wrap').innerHTML = `
        <div class="done">
            <div class="done-check"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#8fb0e0" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg></div>
            <h2>Setup complete</h2>
            <p>Starting Repent... you can close this tab.</p>
        </div>`;
setTimeout(() => {
    window.close();
}, 1000);
}

renderStep();
</script>
</body></html>'''

def run_web_setup(config_data, groups):
    from flask import Flask, request, jsonify
    from werkzeug.serving import make_server

    logging.getLogger('werkzeug').setLevel(logging.ERROR)
    app = Flask(__name__)
    done_event = threading.Event()

    groups_json = json.dumps([
        {
            "title": title,
            "subtitle": subtitle,
            "fields": [
                {"key": key, "kind": kind, "label": label, "help": help_text, "optional": optional}
                for key, kind, label, help_text, optional in fields
            ],
        }
        for title, subtitle, fields in groups
    ])
    page = SETUP_PAGE_TEMPLATE.replace('__GROUPS_JSON__', groups_json)

    @app.route('/', methods=['GET'])
    def setup_get():
        return page

    @app.route('/validate', methods=['POST'])
    def setup_validate():
        data = request.get_json(force=True, silent=True) or {}
        errors = {}
        for entry in data.get('fields', []):
            key, kind, raw = entry.get('key'), entry.get('kind'), entry.get('value')
            ok, value, error = validate_setup_field(key, kind, raw)
            if ok:
                config_data[key] = value
            else:
                errors[key] = error
        return jsonify({"ok": not errors, "errors": errors})

    @app.route('/finish', methods=['POST'])
    def setup_finish():
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config_data, f, indent=4)
        done_event.set()
        return jsonify({"ok": True})

    httpd = make_server('localhost', 8080, app)
    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()
    print("[INFO] first-run setup required!")
    time.sleep(0.5)
    webbrowser.open('http://localhost:8080')
    done_event.wait()
    httpd.shutdown()
    server_thread.join(timeout=5)
    print("[INFO] setup completed,starting repent!")

def config():
    config_data = open_config_read()
    field_specs = {f[0]: f for f in SETUP_FIELDS}
    groups = []
    for title, subtitle, keys in SETUP_GROUPS:
        missing = [field_specs[k] for k in keys if k not in config_data or config_data[k] is None]
        if missing:
            groups.append((title, subtitle, missing))
    if groups:
        run_web_setup(config_data, groups)

downloadshit()
install_cascadia_mono_font()
try:
    if tokenvalid(config_get('token')):
        pass
    else:
        del_value('token')
except:
    pass
config()
