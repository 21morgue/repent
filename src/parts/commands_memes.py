@Repent.command(description=f"Creates an ancient aliens guy meme. \nUsage: {config_get('prefix')}aliensguy [text 1] [text 2]", help="meme")
async def aliensguy(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/aag/{text1}/{text2}.png"))

@Repent.command(description=f"Creates an 'ain't got no time for that' meme. \nUsage: {config_get('prefix')}aintgottime [text 1] [text 2]", help="meme")
async def aintgottime(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/aint-got-time/{text1}/{text2}.png"))
    
@Repent.command(description=f"Creates a seal meme. \nUsage: {config_get('prefix')}seal [text 1] [text 2]", help="meme")
async def seal(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/ams/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a red penguin meme. \nUsage: {config_get('prefix')}redpenguin [text 1] [text 2]", help="meme")
async def redpenguin(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/awesome/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a blue penguin meme. \nUsage: {config_get('prefix')}bluepenguin [text 1] [text 2]", help="meme")
async def bluepenguin(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/awkward/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a bad milk meme. \nUsage: {config_get('prefix')}badmilk [text 1] [text 2]", help="meme")
async def badmilk(ctx, text1: str=None, text2: str=None):   
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/badchoice/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a Discord mod meme. \nUsage: {config_get('prefix')}discordmod [text 1] [text 2]", help="meme")
async def discordmod(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/bd/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a bender meme. \nUsage: {config_get('prefix')}bender [text 1] [text 2]", help="meme")
async def bender(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/bender/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a farmer meme. \nUsage: {config_get('prefix')}farmer [text 1] [text 2]", help="meme")
async def farmer(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/bihw/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a ginger meme. \nUsage: {config_get('prefix')}ginger [text 1] [text 2]", help="meme")
async def ginger(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/blb/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a suitcat meme. \nUsage: {config_get('prefix')}suitcat [text 1] [text 2]", help="meme")
async def suitcat(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/boat/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a bullshark meme. \nUsage: {config_get('prefix')}bullshark [text 1] [text 2]", help="meme")
async def bullshark(ctx, text1: str=None, text2: str=None):   
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/bs/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a Buzz Lightyear meme. \nUsage: {config_get('prefix')}buzz [text 1] [text 2]", help="meme")
async def buzz(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/buzz/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a bear meme. \nUsage: {config_get('prefix')}bear [text 1] [text 2]", help="meme")
async def bear(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/cb/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a comic book guy meme. \nUsage: {config_get('prefix')}comicbookguy [text 1] [text 2]", help="meme")
async def comicbookguy(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/cbg/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a cheems meme. \nUsage: {config_get('prefix')}cheems [text 1] [text 2]", help="meme")
async def cheems(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/cheems/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a chosen one meme. \nUsage: {config_get('prefix')}chosenone [text 1] [text 2]", help="meme")
async def chosenone(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/chosen/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a change my mind meme. \nUsage: {config_get('prefix')}changemymind [text 1] [text 2]", help="meme")
async def changemymind(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/cmm/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a crying on the floor meme. \nUsage: {config_get('prefix')}cryingonfloor [text 1] [text 2]", help="meme")
async def cryingonfloor(ctx, text1: str=None, text2: str=None):   
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/cryingfloor/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a distracted boyfriend meme. \nUsage: {config_get('prefix')}distractedbf [text 1] [text 2]", help="meme")
async def distractedbf(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/db/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a distracted girlfriend meme. \nUsage: {config_get('prefix')}distractedgf [text 1] [text 2]", help="meme")
async def distractedgf(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/dg/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a disaster girl meme. \nUsage: {config_get('prefix')}disastergirl [text 1] [text 2]", help="meme")
async def disastergirl(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/disastergirl/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a Doge meme. \nUsage: {config_get('prefix')}doge [text 1] [text 2]", help="meme")
async def doge(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/doge/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a drunk baby meme. \nUsage: {config_get('prefix')}drunkbaby [text 1] [text 2]", help="meme")
async def drunkbaby(ctx, text1: str=None, text2: str=None):   
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/drunk/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a Dwight meme. \nUsage: {config_get('prefix')}dwight [text 1] [text 2]", help="meme")
async def dwight(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/dwight/{text1}/{text2}.png"))

@Repent.command(description=f"Creates an elf meme. \nUsage: {config_get('prefix')}elf [text 1] [text 2]", help="meme")
async def elf(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/elf/{text1}/{text2}.png"))

@Repent.command(description=f"Creates an exit meme. \nUsage: {config_get('prefix')}exit [text 1] [text 2]", help="meme")
async def exit(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/exit/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a forever alone meme. \nUsage: {config_get('prefix')}foreveralone [text 1] [text 2]", help="meme")
async def foreveralone(ctx, text1: str=None, text2: str=None):   
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/fa/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a facepalm meme. \nUsage: {config_get('prefix')}facepalm [text 1] [text 2]", help="meme")
async def facepalm(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/facepalm/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a this is fine meme. \nUsage: {config_get('prefix')}thisisfine [text 1] [text 2]", help="meme")
async def thisisfine(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/fine/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a Futurama Fry meme. \nUsage: {config_get('prefix')}futuramafry [text 1] [text 2]", help="meme")
async def futuramafry(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/fry/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a grinds my gears meme. \nUsage: {config_get('prefix')}grindsmygears [text 1] [text 2]", help="meme")
async def grindsmygears(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/gears/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a grumpy cat meme. \nUsage: {config_get('prefix')}grumpycat [text 1] [text 2]", help="meme")
async def grumpycat(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/grumpycat/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a Hagrid meme. \nUsage: {config_get('prefix')}hagrid [text 1] [text 2]", help="meme")
async def hagrid(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/hagrid/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a Harold meme. \nUsage: {config_get('prefix')}harold [text 1] [text 2]", help="meme")
async def harold(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/harold/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a headaches meme. \nUsage: {config_get('prefix')}headaches [text 1] [text 2]", help="meme")
async def headaches(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/headaches/{text1}/{text2}.png"))

@Repent.command(description=f"Creates an 'I Can Has Cat' meme. \nUsage: {config_get('prefix')}icanhascat [text 1] [text 2]", help="meme")
async def icanhascat(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/icanhas/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a jetpack meme. \nUsage: {config_get('prefix')}jetpack [text 1] [text 2]", help="meme")
async def jetpack(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/jetpack/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a Joker meme. \nUsage: {config_get('prefix')}joker [text 1] [text 2]", help="meme")
async def joker(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/joker/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a Kermit meme. \nUsage: {config_get('prefix')}kermit [text 1] [text 2]", help="meme")
async def kermit(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/kermit/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a lizard meme. \nUsage: {config_get('prefix')}lizard [text 1] [text 2]", help="meme")
async def lizard(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/ll/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a shocked meme. \nUsage: {config_get('prefix')}shocked [text 1] [text 2]", help="meme")
async def shocked(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/michael-scott/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a mini Keanu meme. \nUsage: {config_get('prefix')}minikeanu [text 1] [text 2]", help="meme")
async def minikeanu(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/mini-keanu/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a mini Keanu meme. \nUsage: {config_get('prefix')}minikeanu [text 1] [text 2]", help="meme")
async def takemymoney(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/money/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a computer dog meme. \nUsage: {config_get('prefix')}computerdog [text 1] [text 2]", help="meme")
async def computerdog(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/noidea/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a psycho girl meme. \nUsage: {config_get('prefix')}psychogirl [text 1] [text 2]", help="meme")
async def psychogirl(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/oag/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a why monkey meme. \nUsage: {config_get('prefix')}whymonkey [text 1] [text 2]", help="meme")
async def whymonkey(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/persian/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a Philosoraptor meme. \nUsage: {config_get('prefix')}philosoraptor [text 1] [text 2]", help="meme")
async def philosoraptor(ctx, text1: str=None, text2: str=None):   
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/philosoraptor/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a smart man meme. \nUsage: {config_get('prefix')}smart [text 1] [text 2]", help="meme")
async def smart(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/rollsafe/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a sad Joe Biden meme. \nUsage: {config_get('prefix')}sadbiden [text 1] [text 2]", help="meme")
async def sadbiden(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/sad-biden/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a sad Obama meme. \nUsage: {config_get('prefix')}sadobama [text 1] [text 2]", help="meme")
async def sadobama(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/sad-obama/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a sad Pepe meme. \nUsage: {config_get('prefix')}sadpepe [text 1] [text 2]", help="meme")
async def sadpepe(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/sadfrog/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a salty meme. \nUsage: {config_get('prefix')}salty [text 1] [text 2]", help="meme")
async def salty(ctx, text1: str=None, text2: str=None):   
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/saltbae/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a suspicious snake meme. \nUsage: {config_get('prefix')}sussnake [text 1] [text 2]", help="meme")
async def willslap(ctx, text1: str=None, text2: str=None):   
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/slap/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a suspicious snake meme. \nUsage: {config_get('prefix')}sussnake [text 1] [text 2]", help="meme")
async def sussnake(ctx, text1: str=None, text2: str=None):   
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/snek/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a happy seal meme. \nUsage: {config_get('prefix')}happyseal [text 1] [text 2]", help="meme")
async def happyseal(ctx, text1: str=None, text2: str=None):   
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/soa/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a Sparta meme. \nUsage: {config_get('prefix')}sparta [text 1] [text 2]", help="meme")
async def sparta(ctx, text1: str=None, text2: str=None):   
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/sparta/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a Spiderman pointing meme. \nUsage: {config_get('prefix')}spiderpoint [text 1] [text 2]", help="meme")
async def spiderpoint(ctx, text1: str=None, text2: str=None):   
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/spiderman/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a stupid SpongeBob meme. \nUsage: {config_get('prefix')}stupidsponge [text 1] [text 2]", help="meme")
async def stupidsponge(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/spongebob/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a stonks meme. \nUsage: {config_get('prefix')}stonks [text 1] [text 2]", help="meme")
async def stonks(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/stonks/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a 'stop it get some help' meme. \nUsage: {config_get('prefix')}getsomehelp [text 1] [text 2]", help="meme")
async def getsomehelp(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/stop-it/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a success kid meme. \nUsage: {config_get('prefix')}successkid [text 1] [text 2]", help="meme")
async def successkid(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/success/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a Donald Trump meme. \nUsage: {config_get('prefix')}trump [text 1] [text 2]", help="meme")
async def trump(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/trump/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a Ugandaknuckles meme. \nUsage: {config_get('prefix')}ugandaknuckles [text 1] [text 2]", help="meme")
async def ugandaknuckles(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/ugandanknuck/{text1}/{text2}.png"))

@Repent.command(description=f"Creates a Willy Wonka meme. \nUsage: {config_get('prefix')}wonka [text 1] [text 2]", help="meme")
async def wonka(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/wonka/{text1}/{text2}.png"))

@Repent.command(description=f"Creates an angry Redditor meme. \nUsage: {config_get('prefix')}angryredditor [text 1] [text 2]", help="meme")
async def angryredditor(ctx, text1: str=None, text2: str=None):    
    if text1 == None or text1 == "":
        text1 = "-"
    elif text2 == None or text2 == "":
        text2 = "-"
    await ctx.send(urlif(f"https://api.memegen.link/images/yuno/{text1}/{text2}.png"))
