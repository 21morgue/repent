@Repent.command(description=f"Generates an image with 3Guofeng3_v34 AI. \nUsage: {config_get('prefix')}guofeng3 <prompt> [negative] [seed]", help="ai")    
async def guofeng3(ctx, prompt: str, negative: str="", seed=None):
    await aigen(ctx, prompt, model="3Guofeng3_v34.safetensors [50f420de]", negative=negative, seed=seed)

@Repent.command(description=f"Generates an image with Absolute Reality AI. \nUsage: {config_get('prefix')}absolutereality <prompt> [negative] [seed]", help="ai")    
async def absolutereality(ctx, prompt: str, negative: str="", seed=None):
    await aigen(ctx, prompt, model="absolutereality_v181.safetensors [3d9d4d2b]", negative=negative, seed=seed)

@Repent.command(description=f"Generates an image with Am I Real AI. \nUsage: {config_get('prefix')}amireal <prompt> [negative] [seed]", help="ai")    
async def amireal(ctx, prompt: str, negative: str="", seed=None):
    await aigen(ctx, prompt, model="amIReal_V41.safetensors [0a8a2e61]", negative=negative, seed=seed)

@Repent.command(description=f"Generates an image with Analog AI. \nUsage: {config_get('prefix')}analog <prompt> [negative] [seed]", help="ai")    
async def analog(ctx, prompt: str, negative: str="", seed=None):
    await aigen(ctx, prompt, model="analog-diffusion-1.0.ckpt [9ca13f02]", negative=negative, seed=seed)

@Repent.command(description=f"Generates an image with Anything AI. \nUsage: {config_get('prefix')}anything <prompt> [negative] [seed]", help="ai")    
async def anything(ctx, prompt: str, negative: str="", seed=None):
    await aigen(ctx, prompt, model="anythingV5_PrtRE.safetensors [893e49b9]", negative=negative, seed=seed)

@Repent.command(description=f"Generates an image with Abyss Orange Mix AI. \nUsage: {config_get('prefix')}abyssorangemix <prompt> [negative] [seed]", help="ai")    
async def abyssorangemix(ctx, prompt: str, negative: str="", seed=None):
    await aigen(ctx, prompt, model="AOM3A3_orangemixs.safetensors [9600da17]", negative=negative, seed=seed)

@Repent.command(description=f"Generates an image with Blazing Drive AI. \nUsage: {config_get('prefix')}blazingdrive <prompt> [negative] [seed]", help="ai")    
async def blazingdrive(ctx, prompt: str, negative: str="", seed=None):
    await aigen(ctx, prompt, model="blazing_drive_v10g.safetensors [ca1c1eab]", negative=negative, seed=seed)

@Repent.command(description=f"Generates an image with Break Domain AI. \nUsage: {config_get('prefix')}breakdomain <prompt> [negative] [seed]", help="ai")    
async def breakdomain(ctx, prompt: str, negative: str="", seed=None):
    await aigen(ctx, prompt, model="breakdomain_M2150.safetensors [15f7afca]", negative=negative, seed=seed)

@Repent.command(description=f"Generates an image with CetusMix AI. \nUsage: {config_get('prefix')}cetusmix <prompt> [negative] [seed]", help="ai")    
async def cetusmix(ctx, prompt: str, negative: str="", seed=None):
    await aigen(ctx, prompt, model="cetusMix_Version35.safetensors [de2f2560]", negative=negative, seed=seed)

@Repent.command(description=f"Generates an image with Chidlren's Stories 3D AI. \nUsage: {config_get('prefix')}stories3d <prompt> [negative] [seed]", help="ai")    
async def stories3d(ctx, prompt: str, negative: str="", seed=None):
    await aigen(ctx, prompt, model="childrensStories_v13D.safetensors [9dfaabcb]", negative=negative, seed=seed)

@Repent.command(description=f"Generates an image with Chidlren's Stories Semi-Real AI. \nUsage: {config_get('prefix')}storiessemi <prompt> [negative] [seed]", help="ai")    
async def storiessemi(ctx, prompt: str, negative: str="", seed=None):
    await aigen(ctx, prompt, model="childrensStories_v1SemiReal.safetensors [a1c56dbb]", negative=negative, seed=seed)

@Repent.command(description=f"Generates an image with Chidlren's Stories Anime AI. \nUsage: {config_get('prefix')}storiessemi <prompt> [negative] [seed]", help="ai")    
async def storiesanime(ctx, prompt: str, negative: str="", seed=None):
    await aigen(ctx, prompt, model="childrensStories_v1ToonAnime.safetensors [2ec7b88b]", negative=negative, seed=seed)

@Repent.command(description=f"Generates an image with Counterfeit AI. \nUsage: {config_get('prefix')}counterfeit <prompt> [negative] [seed]", help="ai")    
async def counterfeit(ctx, prompt: str, negative: str="", seed=None):
    await aigen(ctx, prompt, model="Counterfeit_v30.safetensors [9e2a8f19]", negative=negative, seed=seed)

@Repent.command(description=f"Generates an image with CuteYukimix AI. \nUsage: {config_get('prefix')}cuteyukimix <prompt> [negative] [seed]", help="ai")    
async def cuteyukimix(ctx, prompt: str, negative: str="", seed=None):
    await aigen(ctx, prompt, model="cuteyukimixAdorable_midchapter3.safetensors [04bdffe6]", negative=negative, seed=seed)

@Repent.command(description=f"Generates an image with Cyber Realistic AI. \nUsage: {config_get('prefix')}cyberrealistic <prompt> [negative] [seed]", help="ai")    
async def cyberrealistic(ctx, prompt: str, negative: str="", seed=None):
    await aigen(ctx, prompt, model="cyberrealistic_v33.safetensors [82b0d085]", negative=negative, seed=seed)

@Repent.command(description=f"Generates an image with Dalcefo AI. \nUsage: {config_get('prefix')}dalcefo <prompt> [negative] [seed]", help="ai")    
async def dalcefo(ctx, prompt: str, negative: str="", seed=None):
    await aigen(ctx, prompt, model="dalcefo_v4.safetensors [425952fe]", negative=negative, seed=seed)

@Repent.command(description=f"Generates an image with Deliberate AI. \nUsage: {config_get('prefix')}deliberate <prompt> [negative] [seed]", help="ai")    
async def deliberate(ctx, prompt: str, negative: str="", seed=None):
    await aigen(ctx, prompt, model="deliberate_v3.safetensors [afd9d2d4]", negative=negative, seed=seed)

@Repent.command(description=f"Generates an image with Dreamlike Anime AI. \nUsage: {config_get('prefix')}dreamlikeanime <prompt> [negative] [seed]", help="ai")    
async def dreamlikeanime(ctx, prompt: str, negative: str="", seed=None):
    await aigen(ctx, prompt, model="dreamlike-anime-1.0.safetensors [4520e090]", negative=negative, seed=seed)

@Repent.command(description=f"Generates an image with Dreamlike Diffusion AI. \nUsage: {config_get('prefix')}dreamlikediffusion <prompt> [negative] [seed]", help="ai")    
async def dreamlikediffusion(ctx, prompt: str, negative: str="", seed=None):
    await aigen(ctx, prompt, model="dreamlike-diffusion-1.0.safetensors [5c9fd6e0]", negative=negative, seed=seed)

@Repent.command(description=f"Generates an image with Dreamlike Photoreal AI. \nUsage: {config_get('prefix')}dreamlikephotoreal <prompt> [negative] [seed]", help="ai")    
async def dreamlikephotoreal(ctx, prompt: str, negative: str="", seed=None):
    await aigen(ctx, prompt, model="dreamlike-photoreal-2.0.safetensors [fdcf65e7]", negative=negative, seed=seed)

@Repent.command(description=f"Generates an image with Dreamshaper AI. \nUsage: {config_get('prefix')}dreamshaper <prompt> [negative] [seed]", help="ai")    
async def dreamshaper(ctx, prompt: str, negative: str="", seed=None):
    await aigen(ctx, prompt, model="dreamshaper_8.safetensors [9d40847d]", negative=negative, seed=seed)

@Repent.command(description=f"Generates an image with Edge of Realism AI. \nUsage: {config_get('prefix')}eor <prompt> [negative] [seed]", help="ai")    
async def eor(ctx, prompt: str, negative: str="", seed=None):
    await aigen(ctx, prompt, model="edgeOfRealism_eorV20.safetensors [3ed5de15]", negative=negative, seed=seed)

@Repent.command(description=f"Generates an image with Anime Diffusion AI. \nUsage: {config_get('prefix')}animediffusion <prompt> [negative] [seed]", help="ai")    
async def animediffusion(ctx, prompt: str, negative: str="", seed=None):
    await aigen(ctx, prompt, model="EimisAnimeDiffusion_V1.ckpt [4f828a15]", negative=negative, seed=seed)

@Repent.command(description=f"Generates an image with Elldreth's Vivid AI. \nUsage: {config_get('prefix')}vivid <prompt> [negative] [seed]", help="ai")    
async def vivid(ctx, prompt: str, negative: str="", seed=None):
    await aigen(ctx, prompt, model="elldreths-vivid-mix.safetensors [342d9d26]", negative=negative, seed=seed)

@Repent.command(description=f"Generates an image with PhotoGasm AI. \nUsage: {config_get('prefix')}photogasm <prompt> [negative] [seed]", help="ai")    
async def photogasm(ctx, prompt: str, negative: str="", seed=None):
    await aigen(ctx, prompt, model="epicphotogasm_xPlusPlus.safetensors [1a8f6d35]", negative=negative, seed=seed)

@Repent.command(description=f"Generates an image with EpiCRealism AI. \nUsage: {config_get('prefix')}epicrealism <prompt> [negative] [seed]", help="ai")    
async def epicrealism(ctx, prompt: str, negative: str="", seed=None):
    await aigen(ctx, prompt, model="epicrealism_naturalSinRC1VAE.safetensors [90a4c676]", negative=negative, seed=seed)

@Repent.command(description=f"Generates an image with EpiCRealism Pure Evolution AI. \nUsage: {config_get('prefix')}erpure <prompt> [negative] [seed]", help="ai")    
async def erpure(ctx, prompt: str, negative: str="", seed=None):
    await aigen(ctx, prompt, model="epicrealism_pureEvolutionV3.safetensors [42c8440c]", negative=negative, seed=seed)

@Repent.command(description=f"Generates an image with Seco AI. \nUsage: {config_get('prefix')}seco <prompt> [negative] [seed]", help="ai")    
async def seco(ctx, prompt: str, negative: str="", seed=None):
    await aigen(ctx, prompt, model="ICantBelieveItsNotPhotography_seco.safetensors [4e7a3dfd]", negative=negative, seed=seed)

@Repent.command(description=f"Generates an image with Indigo AI. \nUsage: {config_get('prefix')}indigo <prompt> [negative] [seed]", help="ai")    
async def indigo(ctx, prompt: str, negative: str="", seed=None):
    await aigen(ctx, prompt, model="indigoFurryMix_v75Hybrid.safetensors [91208cbb]", negative=negative, seed=seed)

@Repent.command(description=f"Generates an image with Juggernaut AI. \nUsage: {config_get('prefix')}juggernaut <prompt> [negative] [seed]", help="ai")    
async def juggernaut(ctx, prompt: str, negative: str="", seed=None):
    await aigen(ctx, prompt, model="juggernaut_aftermath.safetensors [5e20c455]", negative=negative, seed=seed)

@Repent.command(description=f"Generates an image with Lofi AI. \nUsage: {config_get('prefix')}lofi <prompt> [negative] [seed]", help="ai")    
async def lofi(ctx, prompt: str, negative: str="", seed=None):
    await aigen(ctx, prompt, model="lofi_v4.safetensors [ccc204d6]", negative=negative, seed=seed)

@Repent.command(description=f"Generates an image with Lyriel AI. \nUsage: {config_get('prefix')}lyriel <prompt> [negative] [seed]", help="ai")    
async def lyriel(ctx, prompt: str, negative: str="", seed=None):
    await aigen(ctx, prompt, model="lyriel_v16.safetensors [68fceea2]", negative=negative, seed=seed)

@Repent.command(description=f"Generates an image with MajicMix AI. \nUsage: {config_get('prefix')}majicmix <prompt> [negative] [seed]", help="ai")    
async def majicmix(ctx, prompt: str, negative: str="", seed=None):
    await aigen(ctx, prompt, model="majicmixRealistic_v4.safetensors [29d0de58]", negative=negative, seed=seed)

@Repent.command(description=f"Generates an image with MechaMix AI. \nUsage: {config_get('prefix')}mechamix <prompt> [negative] [seed]", help="ai")    
async def mechamix(ctx, prompt: str, negative: str="", seed=None):
    await aigen(ctx, prompt, model="mechamix_v10.safetensors [ee685731]", negative=negative, seed=seed)

@Repent.command(description=f"Generates an image with MeinaMix AI. \nUsage: {config_get('prefix')}meinamix <prompt> [negative] [seed]", help="ai")    
async def meinamix(ctx, prompt: str, negative: str="", seed=None):
    await aigen(ctx, prompt, model="meinamix_meinaV11.safetensors [b56ce717]", negative=negative, seed=seed)

@Repent.command(description=f"Generates an image with Neverending Dream AI. \nUsage: {config_get('prefix')}neverendingdream <prompt> [negative] [seed]", help="ai")    
async def neverendingdream(ctx, prompt: str, negative: str="", seed=None):
    await aigen(ctx, prompt, model="neverendingDream_v122.safetensors [f964ceeb]", negative=negative, seed=seed)

@Repent.command(description=f"Generates an image with Openjourney AI. \nUsage: {config_get('prefix')}openjourney <prompt> [negative] [seed]", help="ai")    
async def openjourney(ctx, prompt: str, negative: str="", seed=None):
    await aigen(ctx, prompt, model="openjourney_V4.ckpt [ca2f377f]", negative=negative, seed=seed)

@Repent.command(description=f"Generates an image with Pastek-Mix AI. \nUsage: {config_get('prefix')}pastelmix <prompt> [negative] [seed]", help="ai")    
async def pastelmix(ctx, prompt: str, negative: str="", seed=None):
    await aigen(ctx, prompt, model="pastelMixStylizedAnime_pruned_fp16.safetensors [793a26e8]", negative=negative, seed=seed)

@Repent.command(description=f"Generates an image with Portrait AI. \nUsage: {config_get('prefix')}portrait <prompt> [negative] [seed]", help="ai")    
async def portrait(ctx, prompt: str, negative: str="", seed=None):
    await aigen(ctx, prompt, model="portraitplus_V1.0.safetensors [1400e684]", negative=negative, seed=seed)

@Repent.command(description=f"Generates an image with Protogen AI. \nUsage: {config_get('prefix')}protogen <prompt> [negative] [seed]", help="ai")    
async def protogen(ctx, prompt: str, negative: str="", seed=None):
    await aigen(ctx, prompt, model="protogenx34.safetensors [5896f8d5]", negative=negative, seed=seed)

@Repent.command(description=f"Generates an image with Realistic Vision AI. \nUsage: {config_get('prefix')}realisticvision <prompt> [negative] [seed]", help="ai")    
async def realisticvision(ctx, prompt: str, negative: str="", seed=None):
    await aigen(ctx, prompt, model="Realistic_Vision_V5.0.safetensors [614d1063]", negative=negative, seed=seed)

@Repent.command(description=f"Generates an image with ReV Animated AI. \nUsage: {config_get('prefix')}rev <prompt> [negative] [seed]", help="ai")    
async def rev(ctx, prompt: str, negative: str="", seed=None):
    await aigen(ctx, prompt, model="revAnimated_v122.safetensors [3f4fefd9]", negative=negative, seed=seed)

@Repent.command(description=f"Generates an image with RunDiffusion AI. \nUsage: {config_get('prefix')}rundiffusion <prompt> [negative] [seed]", help="ai")    
async def rundiffusion(ctx, prompt: str, negative: str="", seed=None):
    await aigen(ctx, prompt, model="rundiffusionFX25D_v10.safetensors [cd12b0ee]", negative=negative, seed=seed)

@Repent.command(description=f"Generates an image with RunDiffusion Photorealistic AI. \nUsage: {config_get('prefix')}rdrealistic <prompt> [negative] [seed]", help="ai")    
async def rdrealistic(ctx, prompt: str, negative: str="", seed=None):
    await aigen(ctx, prompt, model="rundiffusionFX_v10.safetensors [cd4e694d]", negative=negative, seed=seed)

@Repent.command(description=f"Generates an image with SD AI. \nUsage: {config_get('prefix')}sd <prompt> [negative] [seed]", help="ai")    
async def sd(ctx, prompt: str, negative: str="", seed=None):
    await aigen(ctx, prompt, model="v1-5-pruned-emaonly.safetensors [d7049739]", negative=negative, seed=seed)

@Repent.command(description=f"Generates an image with SD Inpainting AI. \nUsage: {config_get('prefix')}sdinpainting <prompt> [negative] [seed]", help="ai")    
async def sdinpainting(ctx, prompt: str, negative: str="", seed=None):
    await aigen(ctx, prompt, model="v1-5-inpainting.safetensors [21c7ab71]", negative=negative, seed=seed)

@Repent.command(description=f"Generates an image with Shonin's Beautiful People AI. \nUsage: {config_get('prefix')}shonin <prompt> [negative] [seed]", help="ai")    
async def shonin(ctx, prompt: str, negative: str="", seed=None):
    await aigen(ctx, prompt, model="shoninsBeautiful_v10.safetensors [25d8c546]", negative=negative, seed=seed)

@Repent.command(description=f"Generates an image with TheAlly's Mix AI. \nUsage: {config_get('prefix')}theallysmix <prompt> [negative] [seed]", help="ai")    
async def theallysmix(ctx, prompt: str, negative: str="", seed=None):
    await aigen(ctx, prompt, model="theallys-mix-ii-churned.safetensors [5d9225a4]", negative=negative, seed=seed)

@Repent.command(description=f"Generates an image with Timeless AI. \nUsage: {config_get('prefix')}timeless <prompt> [negative] [seed]", help="ai")    
async def timeless(ctx, prompt: str, negative: str="", seed=None):
    await aigen(ctx, prompt, model="timeless-1.0.ckpt [7c4971d4]", negative=negative, seed=seed)

@Repent.command(description=f"Generates an image with ToonYou AI. \nUsage: {config_get('prefix')}toonyou <prompt> [negative] [seed]", help="ai")    
async def toonyou(ctx, prompt: str, negative: str="", seed=None):
    await aigen(ctx, prompt, model="toonyou_beta6.safetensors [980f6b15]", negative=negative, seed=seed)

def hide_console():
    if platform.system() == 'Windows':
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    elif platform.system() == 'Darwin': 
        subprocess.call(['osascript', '-e', 'tell application "Terminal" to quit'])
    else:  
        subprocess.call(['wmctrl', '-r', ':ACTIVE:', '-b', 'hidden'])

def show_console():
    if platform.system() == 'Windows':
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1)
    elif platform.system() == 'Darwin': 
        subprocess.call(['open', '-a', 'Terminal'])
    else: 
        subprocess.call(['wmctrl', '-r', ':ACTIVE:', '-b', '!hidden'])

@Repent.command(description=f"Hides the console so only the gui is visible. \nUsage: {config_get('prefix')}hideconsole", help="utility")
async def hideconsole(ctx):
    hide_console()

@Repent.command(description=f"Shows the console. \nUsage: {config_get('prefix')}showconsole", help="utility")
async def showconsole(ctx):
    show_console()
