@Repent.command(description=f"Sends text in a vaporwave font. \nUsage: {config_get('prefix')}vaporwave <text>", help="fun")
async def vaporwave(ctx, *, text):     
    special_font_chars = {
        'a': 'ａ', 'b': 'ｂ', 'c': 'ｃ', 'd': 'ｄ', 'e': 'ｅ',
        'f': 'ｆ', 'g': 'ｇ', 'h': 'ｈ', 'i': 'ｉ', 'j': 'ｊ',
        'k': 'ｋ', 'l': 'ｌ', 'm': 'ｍ', 'n': 'ｎ', 'o': 'ｏ',
        'p': 'ｐ', 'q': 'ｑ', 'r': 'ｒ', 's': 'ｓ', 't': 'ｔ',
        'u': 'ｕ', 'v': 'ｖ', 'w': 'ｗ', 'x': 'ｘ', 'y': 'ｙ', 'z': 'ｚ',
        'A': 'Ａ', 'B': 'Ｂ', 'C': 'Ｃ', 'D': 'Ｄ', 'E': 'Ｅ',
        'F': 'Ｆ', 'G': 'Ｇ', 'H': 'Ｈ', 'I': 'Ｉ', 'J': 'Ｊ',
        'K': 'Ｋ', 'L': 'Ｌ', 'M': 'Ｍ', 'N': 'Ｎ', 'O': 'Ｏ',
        'P': 'Ｐ', 'Q': 'Ｑ', 'R': 'Ｒ', 'S': 'Ｓ', 'T': 'Ｔ',
        'U': 'Ｕ', 'V': 'Ｖ', 'W': 'Ｗ', 'X': 'Ｘ', 'Y': 'Ｙ', 'Z': 'Ｚ',
        '!': '！', '£': '£', '$': '＄', '%': '％', '^': '＾',
        '&': '＆', '*': '＊', '(': '（', ')': '）', '~': '～',
        '@': '＠', "'": '＇', '#': '＃', '/': '／', '?': '？',
        '.': '．', '>': '＞', '<': '＜', ',': '，', '|': '｜',
        '-': '－', '_': '＿', '=': '＝', '+': '＋',
        '1': '１', '2': '２', '3': '３', '4': '４', '5': '５',
        '6': '６', '7': '７', '8': '８', '9': '９', '0': '０',
        '\\': '＼'
    }
    translated_text = ''.join([special_font_chars.get(char, char) for char in text])
    await ctx.send(translated_text)

@Repent.command(description=f"Spoilers every character in a sentence. \nUsage: {config_get('prefix')}spoiler <text>", help="fun")
async def spoiler(ctx, *, text):     
    spoiler_text = '||'+'||||' .join(text) + '||' 
    await ctx.send(spoiler_text)

@Repent.command(name="1337", description=f"Formats text into leet speak. \nUsage: {config_get('prefix')}leet <text>", help="fun") 
async def leet(ctx, *, text):    
    leet_dict = {
    'a': '4', 'e': '3', 'l': '1', 't': '7', 'o': '0', 's': '5', 'w': '\\/\\/', 'h': '|-|',
    'A': '4', 'E': '3', 'L': '1', 'T': '7', 'O': '0', 'S': '5', 'W': '\\/\\/', 'H': '|-|'
}
    leet_text = ''.join([leet_dict.get(char, char) for char in text])
    
    await ctx.send(leet_text)

@Repent.command(description=f"Owoifys text. \nUsage: {config_get('prefix')}owoify <text>", help="fun")
async def owoify(ctx, *, text):     
    def owoify_text(text):
        text = text.replace('r', 'w')
        text = text.replace('l', 'w')
        text = text.replace('R', 'W')
        text = text.replace('L', 'W')
        text = text.replace('th', 'f')
        text = text.replace('Th', 'F')
        text = text.replace('ove', 'uv')
        text = text.replace('you', 'wu')
        text = text.replace('You', 'Wu')
        text = text.replace('u', 'uwu')
        text = text.replace('U', 'UwU')
        return text
    owo_text = owoify_text(text)
    await ctx.send(owo_text)

@Repent.command(description=f"Italicises text. \nUsage: {config_get('prefix')}italic <text>", help="fun") 
async def italic(ctx, *, text):    
    await ctx.send(f"*{text}*")

@Repent.command(description=f"Emblodens text. \nUsage: {config_get('prefix')}bold <text>", help="fun") 
async def bold(ctx, *, text):   
    await ctx.send(f"**{text}**")

@Repent.command(description=f"Makes text very large. \nUsage: {config_get('prefix')}superbold <text>", help="fun") 
async def superbold(ctx, *, text):   
    await ctx.send(f"# {text}")

@Repent.command(description=f"Quotes text. \nUsage: {config_get('prefix')}quote <text>", help="fun") 
async def quote(ctx, *, text):    
    await ctx.send(f">>> {text}")

@Repent.command(description=f"Italicises and emboldens text. \nUsage: {config_get('prefix')}italicbold <text>", help="fun") 
async def italicbold(ctx, *, text):    
    await ctx.send(f"***{text}***")

@Repent.command(description=f"Underlines text. \nUsage: {config_get('prefix')}underline <text>", help="fun") 
async def underline(ctx, *, text):    
    await ctx.send(f"__{text}__")

@Repent.command(description=f"Creates a hyperlink. \nUsage: {config_get('prefix')}hyperlink <link> <text>", help="fun") 
async def hyperlink(ctx, link, *, text):    
    await ctx.send(f"[{text}]({link})")

@Repent.command(description=f"Translates text to morse code. \nUsage: {config_get('prefix')}morse <text>", help="fun") 
async def morse(ctx, *, text):    
    morse_dict = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..',
    '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----',
    ' ': ' '}
    morse_text = ' '.join([morse_dict.get(char.upper(), char) for char in text])  
    await ctx.send(morse_text)

@Repent.command(description=f"Translates morse code to text. \nUsage: {config_get('prefix')}demorse <morse>", help="fun") 
async def demorse(ctx, *, morse_text):    
    morse_dict = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
        'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
        'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
        'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
        'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..',
        '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
        '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----',
        ' ': ' '
    }
    reverse_morse_dict = {value: key for key, value in morse_dict.items()}
    text = ''.join([reverse_morse_dict.get(char, char) for char in morse_text.split()])   
    await ctx.send(text)

@Repent.command(description=f"Translates text to hexidecimal. \nUsage: {config_get('prefix')}hex <text>", help="fun") 
async def hex(ctx, *, text):    
    hex_text = text.encode('utf-8').hex()
    await ctx.send(f'0x{hex_text}')

@Repent.command(description=f"Translates hexidecimal to text. \nUsage: {config_get('prefix')}dehex <hex>", help="fun") 
async def dehex(ctx, *, hex_text):    
    try:
        hex_text = hex_text.lstrip('0x')
        decoded_text = bytes.fromhex(hex_text).decode('utf-8')
        await ctx.send(decoded_text)
    except:
        heading = "De-Hex"
        body = "Invalid hexadecimal input."
        cmdname = "dehex"
        await panelmaker(ctx, heading, body, cmdname)

@Repent.command(description=f"Puts an emoji in place of spaces. \nUsage: {config_get('prefix')}emojispace <emoji> <text>", help="fun") 
async def emojispace(ctx, emoji, *, text):    
    emojified_text = emoji.join(text.split())
    await ctx.send(emojified_text)

@Repent.command(description=f"Translates text to binary. \nUsage: {config_get('prefix')}binary <text>", help="fun") 
async def binary(ctx, *, text):    
    binary_text = ' '.join(format(ord(char), '08b') for char in text)    
    await ctx.send(binary_text)

@Repent.command(description=f"Translates binary to text. \nUsage: {config_get('prefix')}debinary <binary>", help="fun") 
async def debinary(ctx, *, binary_text):    
    binary_chunks = binary_text.split()   
    try:
        decoded_text = ''.join(chr(int(chunk, 2)) for chunk in binary_chunks)   
        await ctx.send(decoded_text)
    except ValueError:
        heading = "De-Binary"
        body = "Invalid binary input."
        cmdname = "debinary"
        await panelmaker(ctx, heading, body, cmdname)

@Repent.command(name="base64", description=f"Translates text to base64. \nUsage: {config_get('prefix')}base64 <text>", help="fun") 
async def b64(ctx, *, text):    
    encoded_text = base64.b64encode(text.encode('utf-8')).decode('utf-8')   
    await ctx.send(encoded_text)

@Repent.command(description=f"Translates base64 to text. \nUsage: {config_get('prefix')}debase64 <base64>", help="fun") 
async def debase64(ctx, *, base64_text):    
    try:
        decoded_text = base64.b64decode(base64_text).decode('utf-8')   
        await ctx.send(decoded_text)
    except:
        heading = "De-Base64"
        body = "Invalid base64 input."
        cmdname = "debase64"
        await panelmaker(ctx, heading, body, cmdname)
