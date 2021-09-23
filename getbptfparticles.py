import requests
from requests.utils import unquote
import lxml
from lxml import html
import re


def GetParticleIds():
    resultdict = {}
    regexnum = re.compile('(#)([0-9]*)')
    r = requests.get("https://backpack.tf/developer/particles")
    root = html.fromstring(r.text)
    for i in root.xpath("//table[contains(@class, 'table table-bordered particle-table')]")[0][1:]:
        childelemtext = i.getchildren()[1].text_content()
        regexnumber = regexnum.search(childelemtext)
        effectname = childelemtext[regexnumber.span()[1] + 1:]
        resultdict[effectname[:effectname.find("\n")]] =  childelemtext[regexnumber.span()[0] + 1: regexnumber.span()[1]]
    file = open("effects.txt", "w")
    file.write(resultdict.__str__())
    print(resultdict)

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
        r = requests.get(url)
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

    #Using this tierlist: https://steamcommunity.com/sharedfiles/filedetails/?id=2230045637&searchtext=unusual+effect+tier+list+2021
    stier = [ "Arcana", "Spellbound", "Bonzo the All Gnawing", "Darkblaze", "Hellfire", "Demonflame", "Knifestorm",
    "Poisoned Shadows", "Chiroptera Venenata", "Something Burning this Way Comes", "It's a Secret to Everybody", "Stormy 13th Hour" ]
    atier = [ "Harvest Moon", "Cloudy Moon", "Antifreeze", "Roboactive", "Burning Flames", "Scorching Flames",
    "Green Black Hole", "Time Warp", "Misty Skull", "Frostbite", "Nebula", "Dark Doorway", "Galactic Gateway",
    "Eldritch Opening", "Amaranthine", "Ooze", "Stare From Beyond", "Morning Glory", "Death at Dusk" ]
    btier = [ "Sunbeams", "Green Energy", "Purple Energy", "Haunted Phantasm Jr.", "Ghastly Ghosts Jr.",
    "Sulphorous", "Phosphorus", "Frozen Icefall", "Death by Disco", "Twisted Radiance", "Fifth Dimension",
    "Abduction", "Mystical Medley", "Fragmented Photons", "Abyssal Aura", "Ring of Fire", "Vicious Circle",
    "Eerie Orbiting Fire" ]
    ctier = [ "Brain Drain", "Clairvoyance", "Fragmenting Gluons", "White Lightning", "Tesla Coil", "Sparkling Lights",
    "Snowfallen", "Circling Heart", "Ethereal Essence", "Ether Trail", "Nether Trail", "Menacing Miasma", "Fragmenting Quarks"
    "Wicked Wood", "Ancient Eldritch", "Eldritch Flame", "Vicious Vortex", "Head of Steam", "Wicked Wood", "Snowblinded",
    "Starstorm Slumber", "Starstorm Insomnia" ]
    dtier = [ "It's a Mystery To Everyone", "It's a Puzzle to Me", "Disco Beat Down", "Miami Nights", "Pyroland Daydream",
    "Fragmenting Reality", "Defragmenting Reality", "Valiant Vortex", "Haunted Ghosts", "Molted Mallard", "Omniscient Orb",
    "Neutron Star", "Blizzardy Storm", "Open Mind", "Violet Vortex", "Cloud 9", "Flaming Lantern", "Stormy Storm", "Atomic",
    "Subatomic", "Vivid Plasma", "Verdant Vortex" ]
    etier = [ "Circling TF Logo", "Circling Peace Sign", "Cauldron Bubbles", "Searing Plasma", "Refragmenting Reality",
    "Smoking", "Steaming", "Bubbling", "Purple Confetti", "Green Confetti", "Electrostatic", "Power Surge" ]
    ftier = [ "Orbiting Fire", "Electric Hat Protector", "Magnetic Hat Protector", "Voltaic Hat Protector",
    "Nuts N' Bolts", "Orbiting Planets", "Kill-a-Watt", "Terror-Watt", "Massed Flies", "Aces High", "Dead Presidents",
    "Memory Leak", "Overclocked", "Ancient Codex", "Galactic Codex" ]
GetParticlePrices()
