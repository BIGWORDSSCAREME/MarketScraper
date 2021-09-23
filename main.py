from requests import get
from requests.utils import quote, unquote
from lxml import html
from math import ceil
from time import sleep
import re
import json
import mysql.connector

BPTFAPIKEY = ""
#There's a few weird differences between the effects. Showstopper is 3001 instead of 3002
#on bptf, etc. Maybe its just the dual team effects using one over the other
effectdict = {'Community Sparkle': '4', 'Holy Glow': '5', 'Green Confetti': '6', 'Purple Confetti': '7', 'Haunted Ghosts': '8', 'Green Energy': '9', 'Purple Energy': '10', 'Circling TF Logo': '11', 'Massed Flies': '12', 'Burning Flames': '13', 'Scorching Flames': '14', 'Sunbeams': '17', 'Map Stamps': '20', 'Stormy Storm': '29', 'Orbiting Fire': '33', 'Bubbling': '34', 'Smoking': '35', 'Steaming': '36', 'Cloudy Moon': '38', 'Kill-a-Watt': '56', 'Terror-Watt': '57', 'Cloud 9': '58', 'Time Warp': '70', 'Searing Plasma': '15', 'Vivid Plasma': '16', 'Circling Peace Sign': '18', 'Circling Heart': '19', 'Blizzardy Storm': '30', "Nuts n' Bolts": '31', 'Orbiting Planets': '32', 'Flaming Lantern': '37', 'Cauldron Bubbles': '39', 'Eerie Orbiting Fire': '40', 'Knifestorm': '43', 'Misty Skull': '44', 'Harvest Moon': '45', "It's A Secret To Everybody": '46', 'Stormy 13th Hour': '47', 'Aces High': '59', 'Dead Presidents': '60', 'Miami Nights': '61', 'Disco Beat Down': '62', 'Phosphorous': '63', 'Sulphurous': '64', 'Memory Leak': '65', 'Overclocked': '66', 'Electrostatic': '67', 'Power Surge': '68', 'Anti-Freeze': '69', 'Green Black Hole': '71', 'Roboactive': '72', 'Arcana': '73', 'Spellbound': '74', 'Chiroptera Venenata': '75', 'Poisoned Shadows': '76', 'Something Burning This Way Comes': '77', 'Hellfire': '78', 'Darkblaze': '79', 'Demonflame': '80', 'Showstopper': '3001', 'Holy Grail': '3003', "'72": '3004', 'Fountain of Delight': '3005', 'Screaming Tiger': '3006', 'Skill Gotten Gains': '3007', 'Midnight Whirlwind': '3008', 'Silver Cyclone': '3009', 'Mega Strike': '3010', 'Bonzo The All-Gnawing': '81', 'Amaranthine': '82', 'Stare From Beyond': '83', 'The Ooze': '84', 'Ghastly Ghosts Jr': '85', 'Haunted Phantasm Jr': '86', 'Haunted Phantasm': '3011', 'Ghastly Ghosts': '3012', 'Frostbite': '87', 'Molten Mallard': '88', 'Morning Glory': '89', 'Death at Dusk': '90', 'Hot': '701', 'Isotope': '702', 'Cool': '703', 'Energy Orb': '704', 'Abduction': '91', 'Atomic': '92', 'Subatomic': '93', 'Electric Hat Protector': '94', 'Magnetic Hat Protector': '95', 'Voltaic Hat Protector': '96', 'Galactic Codex': '97', 'Ancient Codex': '98', 'Nebula': '99', 'Death by Disco': '100', "It's a mystery to everyone": '101', "It's a puzzle to me": '102', 'Ether Trail': '103', 'Nether Trail': '104', 'Ancient Eldritch': '105', 'Eldritch Flame': '106', 'Tesla Coil': '108', 'Neutron Star': '107', 'Starstorm Insomnia': '109', 'Starstorm Slumber': '110', 'Infernal Flames': '3015', 'Hellish Inferno': '3013', 'Spectral Swirl': '3014', 'Infernal Smoke': '3016', 'Brain Drain': '111', 'Open Mind': '112', 'Head of Steam': '113', 'Galactic Gateway': '114', 'The Eldritch Opening': '115', 'The Dark Doorway': '116', 'Ring of Fire': '117', 'Vicious Circle': '118', 'White Lightning': '119', 'Omniscient Orb': '120', 'Clairvoyance': '121', 'Acidic Bubbles of Envy': '3017', 'Flammable Bubbles of Attraction': '3018', 'Poisonous Bubbles of Regret': '3019', 'Roaring Rockets': '3020', 'Spooky Night': '3021', 'Ominous Night': '3022', 'Fifth Dimension': '122', 'Vicious Vortex': '123', 'Menacing Miasma': '124', 'Abyssal Aura': '125', 'Wicked Wood': '126', 'Ghastly Grove': '127', 'Mystical Medley': '128', 'Ethereal Essence': '129', 'Twisted Radiance': '130', 'Violet Vortex': '131', 'Verdant Vortex': '132', 'Valiant Vortex': '133', 'Bewitched': '3023', 'Accursed': '3024', 'Enchanted': '3025', 'Static Mist': '3026', 'Eerie Lightning': '3027', 'Terrifying Thunder': '3028', 'Jarate Shock': '3029', 'Nether Void': '3030', 'Sparkling Lights': '134', 'Frozen Icefall': '135', 'Fragmented Gluons': '136', 'Fragmented Quarks': '137', 'Fragmented Photons': '138', 'Defragmenting Reality': '139', 'Fragmenting Reality': '141', 'Refragmenting Reality': '142', 'Snowfallen': '143', 'Snowblinded': '144', 'Pyroland Daydream': '145', 'Good-Hearted Goodies': '3031', 'Wintery Wisp': '3032', 'Arctic Aurora': '3033', 'Winter Spirit': '3034', 'Festive Spirit': '3035', 'Magical Spirit': '3036', 'Verdatica': '147', 'Aromatica': '148', 'Chromatica': '149', 'Prismatica': '150', 'Bee Swarm': '151', 'Frisky Fireflies': '152', 'Smoldering Spirits': '153', 'Wandering Wisps': '154', 'Kaleidoscope': '155', 'Green Giggler': '156', 'Laugh-O-Lantern': '157', 'Plum Prankster': '158', 'Pyroland Nightmare': '159', 'Gravelly Ghoul': '160', 'Vexed Volcanics': '161', 'Gourdian Angel': '162', 'Pumpkin Party': '163', 'Spectral Escort': '3037', 'Astral Presence': '3038', 'Arcane Assistance': '3039', 'Emerald Allurement': '3041', 'Pyrophoric Personality': '3042', 'Spellbound Aspect': '3043', 'Static Shock': '3044', 'Veno Shock': '3045', 'Toxic Terrors': '3046', 'Arachnid Assault': '3047', 'Creepy Crawlies': '3048', 'Frozen Fractals': '164', 'Lavender Landfall': '165', 'Special Snowfall': '166', 'Divine Desire': '167', 'Distant Dream': '168', 'Violent Wintertide': '169', 'Blighted Snowstorm': '170', 'Pale Nimbus': '171', 'Genus Plasmos': '172', 'Serenus Lumen': '173', 'Ventum Maris': '174', 'Mirthful Mistletoe': '175', 'Delightful Star': '3049', 'Frosted Star': '3050', 'Apotheosis': '3051', 'Ascension': '3052', 'Reindoonicorn Rancher': '3053', 'Twinkling Lights': '3055', 'Shimmering Lights': '3056', 'Resonation': '177', 'Aggradation': '178', 'Lucidation': '179', 'Stunning': '180', 'Ardentum Saturnalis': '181', 'Fragrancium Elementalis': '182', 'Reverium Irregularis': '183', 'Perennial Petals': '185', 'Flavorsome Sunset': '186', 'Raspberry Bloom': '187', 'Iridescence': '188'}

effectdictptf = {'Community Sparkle': '4', 'Holy Glow': '5', 'Green Confetti': '6', 'Purple Confetti': '7', 'Haunted Ghosts': '8', 'Green Energy': '9', 'Purple Energy': '10', 'Circling TF Logo': '11', 'Massed Flies': '12', 'Burning Flames': '13', 'Scorching Flames': '14', 'Sunbeams': '17', 'Map Stamps': '20', 'Stormy Storm': '29', 'Orbiting Fire': '33', 'Bubbling': '34', 'Smoking': '35', 'Steaming': '36', 'Cloudy Moon': '38', 'Kill-a-Watt': '56', 'Terror-Watt': '57', 'Cloud 9': '58', 'Time Warp': '70', 'Searing Plasma': '15', 'Vivid Plasma': '16', 'Circling Peace Sign': '18', 'Circling Heart': '19', 'Blizzardy Storm': '30', "Nuts n' Bolts": '31', 'Orbiting Planets': '32', 'Flaming Lantern': '37', 'Cauldron Bubbles': '39', 'Eerie Orbiting Fire': '40', 'Knifestorm': '43', 'Misty Skull': '44', 'Harvest Moon': '45', "It's A Secret To Everybody": '46', 'Stormy 13th Hour': '47', 'Aces High': '59', 'Dead Presidents': '60', 'Miami Nights': '61', 'Disco Beat Down': '62', 'Phosphorous': '63', 'Sulphurous': '64', 'Memory Leak': '65', 'Overclocked': '66', 'Electrostatic': '67', 'Power Surge': '68', 'Anti-Freeze': '69', 'Green Black Hole': '71', 'Roboactive': '72', 'Arcana': '73', 'Spellbound': '74', 'Chiroptera Venenata': '75', 'Poisoned Shadows': '76', 'Something Burning This Way Comes': '77', 'Hellfire': '78', 'Darkblaze': '79', 'Demonflame': '80', 'Showstopper': '3002', 'Holy Grail': '3003', "'72": '3004', 'Fountain of Delight': '3005', 'Screaming Tiger': '3006', 'Skill Gotten Gains': '3007', 'Midnight Whirlwind': '3008', 'Silver Cyclone': '3009', 'Mega Strike': '3010', 'Bonzo The All-Gnawing': '81', 'Amaranthine': '82', 'Stare From Beyond': '83', 'The Ooze': '84', 'Ghastly Ghosts Jr': '85', 'Haunted Phantasm Jr': '86', 'Haunted Phantasm': '3011', 'Ghastly Ghosts': '3012', 'Frostbite': '87', 'Molten Mallard': '88', 'Morning Glory': '89', 'Death at Dusk': '90', 'Hot': '701', 'Isotope': '702', 'Cool': '703', 'Energy Orb': '704', 'Abduction': '91', 'Atomic': '92', 'Subatomic': '93', 'Electric Hat Protector': '94', 'Magnetic Hat Protector': '95', 'Voltaic Hat Protector': '96', 'Galactic Codex': '97', 'Ancient Codex': '98', 'Nebula': '99', 'Death by Disco': '100', "It's a mystery to everyone": '101', "It's a puzzle to me": '102', 'Ether Trail': '103', 'Nether Trail': '104', 'Ancient Eldritch': '105', 'Eldritch Flame': '106', 'Tesla Coil': '108', 'Neutron Star': '107', 'Starstorm Insomnia': '109', 'Starstorm Slumber': '110', 'Infernal Flames': '3015', 'Hellish Inferno': '3013', 'Spectral Swirl': '3014', 'Infernal Smoke': '3016', 'Brain Drain': '111', 'Open Mind': '112', 'Head of Steam': '113', 'Galactic Gateway': '114', 'The Eldritch Opening': '115', 'The Dark Doorway': '116', 'Ring of Fire': '117', 'Vicious Circle': '118', 'White Lightning': '119', 'Omniscient Orb': '120', 'Clairvoyance': '121', 'Acidic Bubbles of Envy': '3017', 'Flammable Bubbles of Attraction': '3018', 'Poisonous Bubbles of Regret': '3019', 'Roaring Rockets': '3020', 'Spooky Night': '3021', 'Ominous Night': '3022', 'Fifth Dimension': '122', 'Vicious Vortex': '123', 'Menacing Miasma': '124', 'Abyssal Aura': '125', 'Wicked Wood': '126', 'Ghastly Grove': '127', 'Mystical Medley': '128', 'Ethereal Essence': '129', 'Twisted Radiance': '130', 'Violet Vortex': '131', 'Verdant Vortex': '132', 'Valiant Vortex': '133', 'Bewitched': '3023', 'Accursed': '3024', 'Enchanted': '3025', 'Static Mist': '3026', 'Eerie Lightning': '3027', 'Terrifying Thunder': '3028', 'Jarate Shock': '3029', 'Nether Void': '3030', 'Sparkling Lights': '134', 'Frozen Icefall': '135', 'Fragmented Gluons': '136', 'Fragmented Quarks': '137', 'Fragmented Photons': '138', 'Defragmenting Reality': '139', 'Fragmenting Reality': '141', 'Refragmenting Reality': '142', 'Snowfallen': '143', 'Snowblinded': '144', 'Pyroland Daydream': '145', 'Good-Hearted Goodies': '3031', 'Wintery Wisp': '3032', 'Arctic Aurora': '3033', 'Winter Spirit': '3034', 'Festive Spirit': '3035', 'Magical Spirit': '3036', 'Verdatica': '147', 'Aromatica': '148', 'Chromatica': '149', 'Prismatica': '150', 'Bee Swarm': '151', 'Frisky Fireflies': '152', 'Smoldering Spirits': '153', 'Wandering Wisps': '154', 'Kaleidoscope': '155', 'Green Giggler': '156', 'Laugh-O-Lantern': '157', 'Plum Prankster': '158', 'Pyroland Nightmare': '159', 'Gravelly Ghoul': '160', 'Vexed Volcanics': '161', 'Gourdian Angel': '162', 'Pumpkin Party': '163', 'Spectral Escort': '3037', 'Astral Presence': '3038', 'Arcane Assistance': '3040', 'Emerald Allurement': '3041', 'Pyrophoric Personality': '3042', 'Spellbound Aspect': '3043', 'Static Shock': '3044', 'Veno Shock': '3045', 'Toxic Terrors': '3046', 'Arachnid Assault': '3047', 'Creepy Crawlies': '3048', 'Frozen Fractals': '164', 'Lavender Landfall': '165', 'Special Snowfall': '166', 'Divine Desire': '167', 'Distant Dream': '168', 'Violent Wintertide': '169', 'Blighted Snowstorm': '170', 'Pale Nimbus': '171', 'Genus Plasmos': '172', 'Serenus Lumen': '173', 'Ventum Maris': '174', 'Mirthful Mistletoe': '175', 'Delightful Star': '3049', 'Frosted Star': '3050', 'Apotheosis': '3051', 'Ascension': '3052', 'Reindoonicorn Rancher': '3054', 'Twinkling Lights': '3055', 'Shimmering Lights': '3056', 'Resonation': '177', 'Aggradation': '178', 'Lucidation': '179', 'Stunning': '180', 'Ardentum Saturnalis': '181', 'Fragrancium Elementalis': '182', 'Reverium Irregularis': '183', 'Perennial Petals': '185', 'Flavorsome Sunset': '186', 'Raspberry Bloom': '187', 'Iridescence': '188'}

def GetParticlePrices():
    #Makes a dictionary that orders the prices of effects. Looks like that V.
    #'Mega Strike': {'avgprice': 5.76, 'lastnode': 'Silver Cyclone', 'nextnode': 'Midnight Whirlwind'}
    url = "https://backpack.tf/effects"
    pricedictreverse = {}
    pricelist = []
    priceregex = re.compile('([0-9]*)(.)([0-9]*)')
    resultdict = {}
    r = None
    while r == None or r.status_code != 200:
        r = get(url, timeout = 15)
        print(r.status_code)
    root = html.fromstring(r.text)
    for i in root.xpath("//ul[contains(@id, 'unusual-pricelist')]")[0].getchildren():
        #print(i.getchildren()[0].text_content())
        #Sometimes fails, probably being rate limited or something
        anode = i.getchildren()[0]
        price = anode.text_content()[4:]
        price = priceregex.search(price)
        price = float(price.group())
        pricedictreverse[price] = unquote(anode.get('href')[8:])
        pricelist.append(price)
    pricelist.sort()
    resultdict = {}
    lastnode = None
    for i in pricelist:
        if lastnode != None:
            resultdict[lastnode]['nextnode'] = pricedictreverse[i]
        resultdict[pricedictreverse[i]] = {'avgprice': i, 'lastnode': lastnode, 'nextnode': None }
        lastnode = pricedictreverse[i]
    return resultdict

#https://api.steampowered.com/IEconItems_440/GetSchemaOverview/v0001/?key=C4578A47DE1AE104CE097BFD4730C801
#Can use the above link to update effect dict. Also marketplace.tf

def RemoveNotNumberLetter(string):
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    result = ""
    for i in string:
        if i in letters:
            result += i
    return result

def JSONFromUrl(url, wait = 3):
    print("getting json from {}".format(url))
    sleep(wait)
    scode = 429
    try:
        r = get(url, timeout = 15)
        scode = r.status_code
    except Exception as e:
        print(e)
    if  scode == 429:
        #limit to 10 tries
        wait = wait + 1
        print("rate limit status code, waiting {} seconds".format(wait))
        return JSONFromUrl(url, wait)
    elif scode != 200:
        print("Status code {} on url {}".format(scode, url))
        return None
    else:
        return json.loads(r.text)

def GetItemList():
    itemstosearch = []
    currentpage = 0
    totalpages = 1
    #Searches taunts and cosmetics. Not anything else
    url = "https://steamcommunity.com/market/search/render/?search_descriptions=0&sort_column=default&sort_dir=desc&appid=440&norender=1&count=100&category_440_Quality%5B%5D=tag_rarity4&sort_column=price&sort_dir=asc&start={}00&category_440_Type%5B%5D=tag_misc&category_440_Type%5B%5D=tag_taunt"
    while currentpage < totalpages:
        jsondata = JSONFromUrl(url.format(currentpage))
        wait = 2
        while (jsondata == None or jsondata['success'] != True or jsondata['total_count'] == 0.0) and wait < 8:
            jsondata = JSONFromUrl(url.format(currentpage), wait)
            wait += 1
        totalpages = jsondata['total_count'] / 100
        print(totalpages)
        itemstosearch.extend(jsondata['results'])
        currentpage += 1
    print(len(itemstosearch))
    return itemstosearch

def CollectItemInfoBPTF(item):
    bptfurl = "https://backpack.tf/api/classifieds/search/v1?key={}&item={}&particle={}&intent=buy&page_size=3"
    resultdict = {}
    #previoussearches probably should be a dict with another dict inside of it instead of lists, but im too lazy to change everything :/
    #did i change this? i have no idea
    previoussearches = {}
    currentpage = 0
    totalpages = 1
    bestdeal = None
    itemname = item['name']
    itemnamequoted = quote(itemname)
    url = "https://steamcommunity.com/market/listings/440/{}/render/?query=&start={}0&count=10&country=US&language=english&currency=1"
    #This is really the only place where I need need to get the "unusual" out of the itemname
    #Idc elsewhere. But after its been quoted, the space is %20 so I need to get rid of 2 extra characters (line below)
    bptfurl = bptfurl.format(BPTFAPIKEY, itemnamequoted[10:], "{}")
    print(bptfurl)
    url = url.format(itemnamequoted, "{}")
    priceregex = re.compile("(\$)([0-9]*)(\.)([0-9]*)")
    while currentpage < totalpages:
        jsondata = None
        while jsondata == None or jsondata['success'] != True:
            jsondata = JSONFromUrl(url.format(currentpage))
        print("TOTALCOUNT {}".format(jsondata["total_count"]))
        if jsondata['total_count'] == 0:
            print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        totalpages = ceil(jsondata["total_count"] / 10)
        Assets = jsondata['assets']
        ListingInfo = jsondata['listinginfo']
        root = html.fromstring(jsondata['results_html'])
        #First check if price has already been gotten, then put it in here.
        itemcount = 0
        for i in root.xpath("//div[contains(@class, 'market_listing_row')]"):
            itemcount += 1
            iteminfo = {}
            profitmargin = 0
            listingid = i.get('class')[53:]
            price = priceregex.search(i.text_content())
            if price == None:
                #if no match is found, continue to next iteration of for
                continue
            price = price.group()[1:]
            effect = None
            for i in Assets['440']['2'][ListingInfo[listingid]['asset']['id']]['descriptions']:
                if i['value'].find("★ Unusual Effect:") == 0:
                    effect = i['value'][18:]
                    break
            if effect in previoussearches.keys():
                iteminfo["bptfprice"] = previoussearches[effect]
            else:
                if effect in effectdict.keys():
                    bptfjson = JSONFromUrl(bptfurl.format(effectdict[effect]))
                    iteminfo["bptfprice"] = 0
                    previoussearches[effect] = 0
                    try:
                        if bptfjson == None:
                            print(bptfjson)
                            iteminfo["bptfprice"] = 0
                        elif bptfjson['buy']['total'] != 0:
                            for i in range(bptfjson['buy']['total']):
                                if not ("Strange" in bptfjson['buy']['listings'][i]['item']['name'] and not "Strange" in itemname):
                                    #Just make sure that it doesn't get prices for strange unusuals
                                    #When searching for only unusuals
                                    iteminfo["bptfprice"] = bptfjson['buy']['listings'][i]['currencies']['keys']
                                    previoussearches[effect] = iteminfo["bptfprice"]
                                    break
                        elif bptfjson['sell']['total'] != 0:
                            for i in range(bptfjson['sell']['total']):
                                if not ("Strange" in bptfjson['sell']['listings'][i]['item']['name'] and not "Strange" in itemname):
                                    #Just make sure that it doesn't get prices for strange unusuals
                                    #When searching for only unusuals
                                    iteminfo["bptfprice"] = bptfjson['sell']['listings'][i]['currencies']['keys']
                                    previoussearches[effect] = iteminfo["bptfprice"]
                                    break
                        else:
                            print(bptfjson)
                            iteminfo["bptfprice"] = 0
                    except Exception as e:
                        print(e)
                        print(bptfjson)
                else:
                    print("EFFECT {} NOT IN EFFECTDICT".format(effect))
            profitmargin = (iteminfo["bptfprice"] * 2) / float(price)
            if bestdeal == None or profitmargin > bestdeal:
                bestdeal = profitmargin
            resultdict[listingid] = [price, effect, iteminfo["bptfprice"], profitmargin]

        currentpage += 1
    print("{} {}s found.".format(len(resultdict), itemname))
    return resultdict, itemname, bestdeal

def CreateConnection():
    conn = None
    cur = None
    try:
        conn = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "admin"
        )
        cur = conn.cursor(buffered = True)
        cur.execute("CREATE DATABASE IF NOT EXISTS items")
        cur.execute("USE items")
    except Exception as e:
        print(e)
        print("b")
    return (conn, cur)

def ItemListToDB(conn, cur, items):
    cur.execute("""CREATE TABLE itemlist2(
    id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name TEXT,
    imgurl TEXT)""")
    for i in items:
        cur.execute("INSERT INTO itemlist2(name, imgurl) VALUES(%s, %s)", (i["name"], i["asset_description"]["icon_url"]))
    cur.execute("DROP TABLE IF EXISTS itemlist")
    cur.execute("RENAME TABLE itemlist2 TO itemlist")
    conn.commit()

def ItemToDB(conn, cur, items, itemname):
    #MUST REMOVE SPACES IN ITEM NAME
    itemname = RemoveNotNumberLetter(itemname)
    cur.execute("""CREATE TABLE {}2(
    id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    price TEXT,
    effect TEXT,
    replacementeffect TEXT,
    sku TEXT,
    cheapestsell INT(11),
    highestbuy INT(11),
    profitmargin FLOAT)
    """.format(itemname))
    for i in items:
        cur.execute("""INSERT INTO {}2(price, effect, replacementeffect, sku, cheapestsell, highestbuy, profitmargin)
        VALUES(%s, %s, %s, %s, %s, %s, %s)""".format(itemname), (items[i]))
    cur.execute("DROP TABLE IF EXISTS {}".format(itemname))
    cur.execute("RENAME TABLE {}2 TO {}".format(itemname, itemname))
    conn.commit()

def ItemToDBBPTF(conn, cur, items, itemname):
    #MUST REMOVE SPACES IN ITEM NAME
    itemname = RemoveNotNumberLetter(itemname)
    cur.execute("DROP TABLE IF EXISTS {}2".format(itemname))
    cur.execute("""CREATE TABLE {}2(
    id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    price TEXT,
    effect TEXT,
    bptfprice INT(11),
    profitmargin FLOAT)
    """.format(itemname))
    for i in items:
        cur.execute("""INSERT INTO {}2(price, effect, bptfprice, profitmargin)
        VALUES(%s, %s, %s, %s)""".format(itemname), (items[i]))
    cur.execute("DROP TABLE IF EXISTS {}".format(itemname))
    cur.execute("RENAME TABLE {}2 TO {}".format(itemname, itemname))
    conn.commit()

def UpdateDealTable(conn, cur, itemname, bestdeal):
    cur.execute("REPLACE INTO profitlist(itemname, bestprofit) VALUES(%s, %s)", (itemname, bestdeal))
    conn.commit()

def GetProfitableItems(conn, curr):
    cur.execute("use items")
    cur.execute("select * from profitlist")
    cur.execute("select itemname from profitlist group by itemname having max(bestprofit) > 1")
    conn.commit()
    items = cur.fetchall()
    resultdict = {}
    for i in items:
        currentitem = RemoveNotNumberLetter(i[0])
        cur.execute("select * from {}".format(currentitem))
        conn.commit()
        resultdict[currentitem] = cur.fetchall()
    return resultdict

if __name__ == "__main__":
    conn, cur = CreateConnection()
    while 1:
        particlepricedict = GetParticlePrices()
        count = 0
        items = GetItemList()
        profititems = GetProfitableItems(conn, cur)
        file = open('profititems.txt', 'w')
        file.truncate(0)
        for i in profititems:
            file.write("{}\n".format(i))
            for j in profititems[i]:
                file.write(j.__str__())
                if j[4] > 1:
                    file.write("PROFIT>1")
                file.write("\n")
            file.write("\n")
        file.close()
        for i in items:
            listings, itemname, bestdeal = CollectItemInfoBPTF(i)
            ItemToDBBPTF(conn, cur, listings, itemname)
            UpdateDealTable(conn, cur, itemname, bestdeal)
            count += 1
            print("{} out of {} items collected".format(count, len(items)))
        print("done")
    conn.close()
