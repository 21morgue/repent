# repent.wtf is fork of [cheddlatron selfbot](https://github.com/Cheddlar/Cheddlatron-Source)

# Honorable mention
[Keira](https://github.com/KeiraOMG0): sponsoring claude code,cdn server and make this project doable\
[Grabify](https://github.com/Gr4bify/): retired developer of cheddlatron & helped me fix the bot\
[Cheddlar](https://github.com/Cheddlar): retired developer of cheddlatron\
Wraith: retired developer of cheddlatron

> **Disclaimer:** Selfbots (automating a normal user account instead of a proper bot account) violate [Discord's Terms of Service](https://discord.com/terms) and can get the account banned. This project is provided for educational purposes. Use it on an account you're willing to lose, and never on your primary account.

## Features

- **500+ commands** across `account`, `utility`, `fun`, `meme`, `moderation`, `ai`, `hacking`, `codeblock`, `raid`, `dumping`, `spotify`, and `music`
- **YouTube music playback** - `mplay`, `mskip`, `mstop`, `mqueue`, `mnowplaying`, `mloop`, `mautoplay`, `mvolume` stream real audio into a voice channel via [ytqueue](https://github.com/KeiraOMG0/ytqueue), with automatic cookie refresh via the [musicbot-cookie-sync](https://github.com/KeiraOMG0/musicbot-cookie-sync) Chrome extension
- **Clean dashboard** - account info, live console, rich presence editor, command list, and settings, all in a desktop window.
- **Customization** - customize every thing you want with repent
- **Custom badges** - extra stuff i added because i have a lot of free time
- **Safe** - its an open sourced project ofc its gonna be safe
## Requirements

- Python 3.10+ (tested on 3.11)
- Windows, macOS, or Linux (some conveniences — console font/codepage handling, `chcp`-equivalent fixes — are Windows-specific)
- A Discord account token
- [ffmpeg](https://ffmpeg.org/download.html) on your `PATH` (only needed for music playback)

## Music setup

Music commands (`mplay`, `mskip`, `mstop`, `mqueue`, `mnowplaying`, `mloop`, `mautoplay`, `mvolume`) need a couple of one-time setup steps:

1. Install [ffmpeg](https://ffmpeg.org/download.html) and make sure it's on your system `PATH`.
2. `pip install -r req.txt` (this pulls in `ytqueue` and `PyNaCl`, both required for voice audio).
3. (Optional, recommended) Load the cookie-sync Chrome extension so age/sign-in-gated YouTube videos keep working without manually re-exporting cookies:
   - Open `chrome://extensions`, enable **Developer mode**
   - Click **Load unpacked** and select `extras/musicbot-cookie-sync/extension/`
   - In the extension's options, set **Server origin** to `http://127.0.0.1:8999` and **Cookie domain** to `youtube.com`
   - Leave Chrome open (any window in the same profile keeps the poll loop alive)

## Previews
> main menu & console
<img width="1359" height="638" alt="image" src="https://github.com/user-attachments/assets/257c56aa-4f52-4e80-b68a-7b3643939c74" />

> RPC settings
<img width="1361" height="629" alt="image" src="https://github.com/user-attachments/assets/e4b70eb1-fc0a-4eea-bf9c-2c5e867bb513" />

> info tab 
<img width="1357" height="635" alt="image" src="https://github.com/user-attachments/assets/93ed6921-775c-46da-8822-9695881a278b" />

> config tab
<img width="1360" height="629" alt="image" src="https://github.com/user-attachments/assets/a95fddac-4f35-4c13-94a9-ed9cf1c8974f" />

