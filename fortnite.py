class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

try:
    import fortnitepy
    from fortnitepy.errors import *
    import BenBotAsync
    import asyncio
    import time as delay
    import datetime
    import json
    import aiohttp
    import time
    import logging
    import functools
    import sys
    import os
    import random
    from colorama import init
    init(autoreset=True)
    from colorama import Fore, Back, Style
except ModuleNotFoundError:
    print(Fore.RED + f'[FORTNITEPY] [N/A] [ERROR] Impossible dimporter un ou plusieurs modules, exécutez "INSTALL PACKAGES.bat".')
    exit()

print(f'  ') 
print(color.YELLOW + f'██████╗  █████╗ ██╗██████╗ ██╗  ██╗ ██████╗  ██████╗ ███████╗    ██╗  ██╗    ██╗  ██╗██╗███████╗██╗   ██╗ ')
print(color.YELLOW + f'██╔══██╗██╔══██╗██║██╔══██╗██║ ██╔╝██╔═══██╗██╔═══██╗██╔════╝    ╚██╗██╔╝    ██║ ██╔╝██║╚══███╔╝██║   ██║ ')
print(color.YELLOW + f'██║  ██║███████║██║██████╔╝█████╔╝ ██║   ██║██║   ██║███████╗     ╚███╔╝     █████╔╝ ██║  ███╔╝ ██║   ██║ ')
print(color.YELLOW + f'██║  ██║██╔══██║██║██╔══██╗██╔═██╗ ██║   ██║██║   ██║╚════██║     ██╔██╗     ██╔═██╗ ██║ ███╔╝  ██║   ██║ ')
print(color.YELLOW + f'██████╔╝██║  ██║██║██║  ██║██║  ██╗╚██████╔╝╚██████╔╝███████║    ██╔╝ ██╗    ██║  ██╗██║███████╗╚██████╔╝ ')
print(color.YELLOW + f'╚═════╝ ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚══════╝    ╚═╝  ╚═╝    ╚═╝  ╚═╝╚═╝╚══════╝ ╚═════╝  ')
print(f'  ')

def debugOn():
    logger = logging.getLogger('fortnitepy.xmpp')
    logger.setLevel(level=logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

def getTime():
    time = datetime.datetime.now().strftime('%H:%M:%S')
    return time

with open('config.json') as f:
    print(f' [DairkXkizu] [{getTime()}] Chargement de la configuration by Dairkoos x Kizu.')
    data = json.load(f)
    print(f' [DairkXkizu] [{getTime()}] Config chargé by Dairkoos x Kizu.')
    
debug = 'False'
if debug == 'True':
    print(f' [DairkXkizu] [{getTime()}] La journalisation du débogage est activée by Kizu x Dairkoos.')
    debugOn()
else:
    print(f' [DairkXkizu] [{getTime()}] La journalisation du débogage est désactivée by Dairkoos x Kizu.')

def get_device_auth_details():
    if os.path.isfile('auths.json'):
        with open('auths.json', 'r') as fp:
            return json.load(fp)
    return {}

def store_device_auth_details(email, details):
    existing = get_device_auth_details()
    existing[email] = details

    with open('auths.json', 'w') as fp:
        json.dump(existing, fp)

device_auth_details = get_device_auth_details().get(data['email'], {})
client = fortnitepy.Client(
    auth=fortnitepy.AdvancedAuth(
        email=data['email'],
        password=data['password'],
        prompt_authorization_code=True,
        delete_existing_device_auths=True,
        **device_auth_details
    ),
    status=data['status'],
    platform=fortnitepy.Platform(data['platform'])
)

@client.event
async def event_device_auth_generate(details, email):
    store_device_auth_details(email, details)

@client.event
async def event_ready():
    print(Fore.GREEN + ' [DairkXkizu] [' + getTime() + '] Client prêt en tant que {0.user.display_name}.'.format(client))

    member = client.party.me

    await member.edit_and_keep(
        functools.partial(
            fortnitepy.ClientPartyMember.set_outfit,
            asset=data['cid']
        ),
        functools.partial(
            fortnitepy.ClientPartyMember.set_backpack,
            asset=data['bid']
        ),
        functools.partial(
            fortnitepy.ClientPartyMember.set_pickaxe,
            asset=data['pid']
        ),
        functools.partial(
            fortnitepy.ClientPartyMember.set_banner,
            icon=data['banner'],
            color=data['banner_color'],
            season_level=data['level']
        ),
        functools.partial(
            fortnitepy.ClientPartyMember.set_battlepass_info,
            has_purchased=True,
            level=data['bp_tier']
        )
    )

@client.event
async def event_party_invite(invite):
    if data['joinoninvite'].lower() == 'true':
        if invite.sender.display_name not in data['BlockList']:
            try:
                await invite.accept()
                print(Fore.GREEN + f' [DairkXkizu] [{getTime()}] Invitation de groupe acceptée de {invite.sender.display_name}')
            except Exception as e:
                pass
        elif invite.sender.display_name in data['BlockList']:
            print(Fore.GREEN + f' [DairkXkizu] [{getTime()}] Invitation de groupe jamais acceptée de' + Fore.RED + f' {invite.sender.display_name}')
    if data['joinoninvite'].lower() == 'false':
        if invite.sender.display_name in data['FullAccess']:
            await invite.accept()
            print(Fore.GREEN + f' [DairkXkizu] [{getTime()}] Invitation de groupe acceptée de {invite.sender.display_name}')
        else:
            print(Fore.GREEN + f' [DairkXkizu] [{getTime()}] Invitation de groupe jamais acceptée de {invite.sender.display_name}')
            await invite.sender.send(f"Je ne peux pas te rejoindre maintenant.")

@client.event
async def event_friend_request(request):
    if data['friendaccept'].lower() == 'true':
        if request.display_name not in data['BlockList']:
            try:
                await request.accept()
                print(f" [DairkXkizu] [{getTime()}] Demande d'amis acceptée de: {request.display_name}")
            except Exception as e:
                pass
        elif request.display_name in data['BlockList']:
            print(f" [DairkXkizu] [{getTime()}] Demande d'amis jamais accepté de: " + Fore.RED + f"{request.display_name}")
    if data['friendaccept'].lower() == 'false':
        if request.display_name in data['FullAccess']:
            try:
                await request.accept()
                print(f" [DairkXkizu] [{getTime()}] Demande d'amis acceptée de: {request.display_name}")
            except Exception as e:
                pass
        else:
            print(f" [DairkXkizu] [{getTime()}] Jamais accepté la demande d'amis de: {request.display_name}")

@client.event
async def event_party_member_join(member):
    if client.user.display_name != member.display_name:
        print(f" [DairkXkizu] [{getTime()}] {member.display_name} a rejoint le lobby.")

@client.event
async def event_friend_message(message):
    args = message.content.split()
    split = args[1:]
    joinedArguments = " ".join(split)
    print(' [DairkXkizu] [' + getTime() + '] {0.author.display_name}: {0.content}'.format(message))

    if "!skin" in args[0].lower():
        if message.author.display_name in data['BlockList']:
            await message.reply("Vous n'avez pas accès à cette commande!")
        else:
            try:
                cosmetic = await BenBotAsync.get_cosmetic(
                    lang="en",
                    searchLang="en",
                    matchMethod="contains",
                    name=joinedArguments,
                    backendType="AthenaCharacter"
                )
                await client.party.me.set_outfit(asset=cosmetic.id)
                await message.reply('Skin définis sur ' + f'{cosmetic.name}')
            except BenBotAsync.exceptions.NotFound:
                await message.reply(f'Impossible de trouver un skins nommé: {joinedArguments}')
                
        
    if "!backpack" in args[0].lower():
        if message.author.display_name in data['BlockList']:
            await message.reply("Vous n'avez pas accès à cette commande!")
        else:
            if len(args) == 1:
                await client.party.me.set_backpack(asset='none')
                await message.reply('Sac à dos définis sur Aucun')
            else:
                try:
                    cosmetic = await BenBotAsync.get_cosmetic(
                        lang="en",
                        searchLang="en",
                        matchMethod="contains",
                        name=joinedArguments,
                        backendType="AthenaBackpack"
                    )
                    await client.party.me.set_backpack(asset=cosmetic.id)
                    await message.reply('Sac à dos définis sur ' + f'{cosmetic.name}')
                except BenBotAsync.exceptions.NotFound:
                    await message.reply(f'Impossible de trouver un sac à dos nommé: {joinedArguments}')

    if "!random" in args[0].lower():
        if message.author.display_name in data['BlockList']:
            await message.reply("Vous n'avez pas accès à cette commande!")
        else:
            if len(args) == 1:
                skins = await BenBotAsync.get_cosmetics(
                    lang="en",
                    searchLang="en",
                    backendType="AthenaCharacter"
                )
                skin = random.choice(skins)

                backpacks = await BenBotAsync.get_cosmetics(
                    lang="en",
                    searchLang="en",
                    backendType="AthenaBackpack"
                )
                backpack = random.choice(backpacks)

                pickaxes = await BenBotAsync.get_cosmetics(
                    lang="en",
                    searchLang="en",
                    backendType="AthenaPickaxe"
                )
                pickaxe = random.choice(pickaxes)

                await client.party.me.set_outfit(
                    asset=skin.id
                )

                await client.party.me.set_backpack(
                    asset=backpack.id
                )

                await client.party.me.set_pickaxe(
                    asset=pickaxe.id
                )

                await message.reply(f'Chargement défini sur: {skin.name}, {backpack.name}, {pickaxe.name}')
            if len(args) == 2:
                if args[1].lower() == 'skin':
                    skins = await BenBotAsync.get_cosmetics(
                    lang="en",
                    searchLang="en",
                    backendType="AthenaCharacter"
                    )
                    skin = random.choice(skins)

                    await client.party.me.set_outfit(
                        asset=skin.id
                    )

                    await message.reply(f"Skin définis sur: {skin.name}")

                if args[1].lower() == 'backpack':
                    backpacks = await BenBotAsync.get_cosmetics(
                    lang="en",
                    searchLang="en",
                    backendType="AthenaBackpack"
                    )
                    backpack = random.choice(backpacks)

                    await client.party.me.set_backpack(
                        asset=backpack.id
                    )

                    await message.reply(f"Sac a dos définis sur: {backpack.name}")

                if args[1].lower() == 'emote':
                    emotes = await BenBotAsync.get_cosmetics(
                    lang="en",
                    searchLang="en",
                    backendType="AthenaDance"
                    )
                    emote = random.choice(emotes)

                    await client.party.me.set_emote(
                        asset=emote.id
                    )

                    await message.reply(f"Emote définis sur: {emote.name}")

                if args[1].lower() == 'pickaxe':
                    pickaxes = await BenBotAsync.get_cosmetics(
                    lang="en",
                    searchLang="en",
                    backendType="AthenaPickaxe"
                    )
                    pickaxe = random.choice(pickaxes)

                    await client.party.me.set_pickaxe(
                        asset=pickaxe.id
                    )

                    await message.reply(f"Pioche définis sur: {pickaxe.name}")
        
    if "!cid" in args[0].lower():
        if message.author.display_name in data['BlockList']:
            await message.reply("Vous n'avez pas accès à cette commande!")
        else:
            try:
                cosmetic = await BenBotAsync.get_cosmetic(
                    lang="en",
                    searchLang="en",
                    matchMethod="contains",
                    name=joinedArguments,
                    backendType="AthenaCharacter"
                )
                await message.reply(f'Le CID pour {cosmetic.name} est: ' + f'{cosmetic.id}')
                print(f" [DairkXkizu] [{getTime()}] CID pour {cosmetic.name}: {cosmetic.id}")
            except BenBotAsync.exceptions.NotFound:
                await message.reply(f'Impossible de trouver un cid pour le skin: {joinedArguments}')
    
    if "!bid" in args[0].lower():
        if message.author.display_name in data['BlockList']:
            await message.reply("Vous n'avez pas accès à cette commande!")
        else:
            try:
                cosmetic = await BenBotAsync.get_cosmetic(
                    lang="en",
                    searchLang="en",
                    matchMethod="contains",
                    name=joinedArguments,
                    backendType="AthenaBackpack"
                )
                await message.reply(f'Le BID pour {cosmetic.name} est: ' + f'{cosmetic.id}')
                print(f" [DairkXkizu] [{getTime()}] BID pour {cosmetic.name}: {cosmetic.id}")
            except BenBotAsync.exceptions.NotFound:
                await message.reply(f'Impossible de trouver un BID pour le sac à dos: {joinedArguments}')
    
    if "!eid" in args[0].lower():
        if message.author.display_name in data['BlockList']:
            await message.reply("Vous n'avez pas accès à cette commande!")
        else:
            try:
                cosmetic = await BenBotAsync.get_cosmetic(
                    lang="en",
                    searchLang="en",
                    matchMethod="contains",
                    name=joinedArguments,
                    backendType="AthenaDance"
                )
                await message.reply(f'LE EID pour {cosmetic.name} est: ' + f'{cosmetic.id}')
                print(f" [DairkXkizu] [{getTime()}] EID pour {cosmetic.name}: {cosmetic.id}")
            except BenBotAsync.exceptions.NotFound:
                await message.reply(f'Impossible de trouver un eid pour lemote: {joinedArguments}')

    if "!pid" in args[0].lower():
        if message.author.display_name in data['BlockList']:
            await message.reply("Vous n'avez pas accès à cette commande!")
        else:
            try:
                cosmetic = await BenBotAsync.get_cosmetic(
                    lang="en",
                    searchLang="en",
                    matchMethod="contains",
                    name=joinedArguments,
                    backendType="AthenaPickaxe"
                )
                await message.reply(f'Le PID pour {cosmetic.name} est: ' + f'{cosmetic.id}')
                print(f" [DairkXkizu] [{getTime()}] PID pour {cosmetic.name}: {cosmetic.id}")
            except BenBotAsync.exceptions.NotFound:
                await message.reply(f'Impossible de trouver un pid pour la pioche: {joinedArguments}')

    if "!emote" in args[0].lower():
        if message.author.display_name in data['BlockList']:
            await message.reply("Vous n'avez pas accès à cette commande!")
        else:
            try:
                cosmetic = await BenBotAsync.get_cosmetic(
                    lang="en",
                    searchLang="en",
                    matchMethod="contains",
                    name=joinedArguments,
                    backendType="AthenaDance"
                )
                await client.party.me.clear_emote()
                await client.party.me.set_emote(asset=cosmetic.id)
                await message.reply('Emote définis sur ' + f'{cosmetic.name}')
            except BenBotAsync.exceptions.NotFound:
                await message.reply(f'Impossible de trouver un emote nommé: {joinedArguments}')
    
    if "!pickaxe" in args[0].lower():
        if message.author.display_name in data['BlockList']:
            await message.reply("Vous n'avez pas accès à cette commande!")
        else:
            try:
                cosmetic = await BenBotAsync.get_cosmetic(
                    lang="en",
                    searchLang="en",
                    matchMethod="contains",
                    name=joinedArguments,
                    backendType="AthenaPickaxe"
                )
                await client.party.me.set_pickaxe(asset=cosmetic.id)
                await message.reply('Pioche définis sur' + f'{cosmetic.name}')
            except BenBotAsync.exceptions.NotFound:
                await message.reply(f'Impossible de trouver une pioche nommée: {joinedArguments}')

    if "!point" in args[0].lower():
        if message.author.display_name in data['BlockList']:
            await message.reply("Vous n'avez pas accès à cette commande!")
        else:
            await client.party.me.clear_emote()
            if len(args) == 1:
                await client.party.me.set_emote(asset="/Game/Athena/Items/Cosmetics/Dances/EID_IceKing.EID_IceKing")
                await message.reply('Faire un emote: le signaler')
            else:
                if len(args) == 2:
                    if args[1].lower() == 'random':
                        pickaxes = await BenBotAsync.get_cosmetics(
                        lang="en",
                        searchLang="en",
                        backendType="AthenaPickaxe"
                        )
                        pickaxe = random.choice(pickaxes)

                        await client.party.me.set_pickaxe(
                            asset=pickaxe.id
                        )

                        await client.party.me.clear_emote()
                        await client.party.me.set_emote(asset="/Game/Athena/Items/Cosmetics/Dances/EID_IceKing.EID_IceKing")

                        await message.reply(f"Pointant avec: {pickaxe.name}")
                    else:
                        try:
                            cosmetic = await BenBotAsync.get_cosmetic(
                                lang="en",
                                searchLang="en",
                                matchMethod="contains",
                                name=joinedArguments,
                                backendType="AthenaPickaxe"
                            )
                            await client.party.me.set_pickaxe(asset=cosmetic.id)
                            await client.party.me.clear_emote()
                            await client.party.me.set_emote(asset="/Game/Athena/Items/Cosmetics/Dances/EID_IceKing.EID_IceKing")
                            await message.reply('Pointant avec: ' + f'{cosmetic.name}')
                        except BenBotAsync.exceptions.NotFound:
                            await message.reply(f'Impossible de trouver une pioche nommée: {joinedArguments}')

    if "!pet" in args[0].lower():
        if message.author.display_name in data['BlockList']:
            await message.reply("Vous n'avez pas accès à cette commande!")
        else:
            try:
                cosmetic = await BenBotAsync.get_cosmetic(
                    lang="en",
                    searchLang="en",
                    matchMethod="contains",
                    name=joinedArguments,
                    backendType="AthenaPet"
                )
                await client.party.me.set_pet(asset=cosmetic.id)
                await message.reply('Pet set to ' + f'{cosmetic.name}')
            except BenBotAsync.exceptions.NotFound:
                await message.reply(f'Impossible de trouver un animal nommé: {joinedArguments}')

    if "!emoji" in args[0].lower():
        if message.author.display_name in data['BlockList']:
            await message.reply("Vous n'avez pas accès à cette commande!")
        else:
            try:
                cosmetic = await BenBotAsync.get_cosmetic(
                    lang="en",
                    searchLang="en",
                    matchMethod="contains",
                    name=joinedArguments,
                    backendType="AthenaEmoji"
                )
                await client.party.me.set_emoji(asset=cosmetic.id)
                await message.reply('Emoji set to ' + f'{cosmetic.name}')
            except BenBotAsync.exceptions.NotFound:
                await message.reply(f'Impossible de trouver un Emojis nommé: {joinedArguments}')

    if "!skullviolet" in args[0].lower():
        if message.author.display_name in data['BlockList']:
            await message.reply("Vous n'avez pas accès à cette commande!")
        else:
            try:
                variants = client.party.me.create_variants(
                   clothing_color=1
                )

                await client.party.me.set_outfit(
                    asset='CID_030_Athena_Commando_M_Halloween',
                    variants=variants
                )

                await message.reply('skins définis sur Skull Trooper violet!')
                print(f" [DairkXkizu] [{getTime()}] Skin du client défini sur Skull Trooper violet")
            except Exception as e:
                pass

    if "!ghoulrose" in args[0].lower():
        if message.author.display_name in data['BlockList']:
            await message.reply("Vous n'avez pas accès à cette commande!")
        else:
            try:
                variants = client.party.me.create_variants(
                   material=3
                )

                await client.party.me.set_outfit(
                    asset='CID_029_Athena_Commando_F_Halloween',
                    variants=variants
                )

                await message.reply("Skins définis sur ghoul rose!")
                print(f" [DairkXkizu] [{getTime()}] Skin du client défini sur ghoul rose")
            except Exception as e:
                pass
               
    if "!goldenpeely" in args[0].lower():
        await client.party.me.set_outfit(
            asset='CID_701_Athena_Commando_M_BananaAgent',
            variants=client.party.me.create_variants(
                progressive=4
                ),
            enlightenment=(2, 350)
        )

        await message.reply(f'Skin définis sur Golden Peely')
        
    if "!peelyshadow" in args[0].lower():
        await client.party.me.set_outfit(
            asset='CID_701_Athena_Commando_M_BananaAgent',
            variants=client.party.me.create_variants(
                progressive=3
                ),
            enlightenment=(2, 350)
        )

        await message.reply(f'Skin définis sur shadow Peely')
        
    if "!peelyghost" in args[0].lower():
        await client.party.me.set_outfit(
            asset='CID_701_Athena_Commando_M_BananaAgent',
            variants=client.party.me.create_variants(
                progressive=2
                ),
            enlightenment=(2, 350)
        )

        await message.reply(f'Skin définis sur ghost Peely')
        
    if "!goldenmidas" in args[0].lower():
        await client.party.me.set_outfit(
            asset='CID_694_Athena_Commando_M_Catburglar',
            variants=client.party.me.create_variants(
                progressive=4
                ),
            enlightenment=(2, 350)
        )

        await message.reply(f'Skin définis sur Golden Peely')
        
    if "!midasshadow" in args[0].lower():
        await client.party.me.set_outfit(
            asset='CID_694_Athena_Commando_M_Catburglar',
            variants=client.party.me.create_variants(
                progressive=3
                ),
            enlightenment=(2, 350)
        )

        await message.reply(f'Skin définis sur shadow midas')
        
    if "!midasghost" in args[0].lower():
        await client.party.me.set_outfit(
            asset='CID_694_Athena_Commando_M_Catburglar',
            variants=client.party.me.create_variants(
                progressive=2
                ),
            enlightenment=(2, 350)
        )

        await message.reply(f'Skin définis sur ghost Peely')
        
    if "!goldenbrutus" in args[0].lower():
        await client.party.me.set_outfit(
            asset='CID_692_athena_commando_m_henchmantough',
            variants=client.party.me.create_variants(
                progressive=4
                ),
            enlightenment=(2, 350)
        )

        await message.reply(f'Skin définis sur golden brutus')
        
    if "!brutusshadow" in args[0].lower():
        await client.party.me.set_outfit(
            asset='CID_692_athena_commando_m_henchmantough',
            variants=client.party.me.create_variants(
                progressive=3
                ),
            enlightenment=(2, 350)
        )

        await message.reply(f'Skin définis shadow brutus')
        
    if "!brutusghost" in args[0].lower():
        await client.party.me.set_outfit(
            asset='CID_692_athena_commando_m_henchmantough',
            variants=client.party.me.create_variants(
                progressive=2
                ),
            enlightenment=(2, 350)
        )

        await message.reply(f'Skin définis sur ghost brutus')
        
    if "!goldenskye" in args[0].lower():
        await client.party.me.set_outfit(
            asset='CID_690_athena_commando_f_photographer',
            variants=client.party.me.create_variants(
                progressive=4
                ),
            enlightenment=(2, 350)
        )

        await message.reply(f'Skin définis sur golden skye')
        
    if "!skyeshadow" in args[0].lower():
        await client.party.me.set_outfit(
            asset='CID_690_athena_commando_f_photographer',
            variants=client.party.me.create_variants(
                progressive=3
                ),
            enlightenment=(2, 350)
        )

        await message.reply(f'Skin définis sur shadow skye')
        
    if "!skyeghost" in args[0].lower():
        await client.party.me.set_outfit(
            asset='CID_690_athena_commando_f_photographer',
            variants=client.party.me.create_variants(
                progressive=2
                ),
            enlightenment=(2, 350)
        )

        await message.reply(f'Skin définis sur ghost skye')
        
    if "!goldenbuffcat" in args[0].lower():
        await client.party.me.set_outfit(
            asset='CID_693_athena_commando_m_buffcat',
            variants=client.party.me.create_variants(
                progressive=4
                ),
            enlightenment=(2, 350)
        )

        await message.reply(f'Skin définis sur golden Mewscles')
        
    if "!buffcatghost" in args[0].lower():
        await client.party.me.set_outfit(
            asset='CID_693_athena_commando_m_buffcat',
            variants=client.party.me.create_variants(
                progressive=2
                ),
            enlightenment=(2, 350)
        )

        await message.reply(f'Skin définis sur Ghost Mewscles')
        
    if "!buffcatshadow" in args[0].lower():
        await client.party.me.set_outfit(
            asset='CID_693_athena_commando_m_buffcat',
            variants=client.party.me.create_variants(
                progressive=3
                ),
            enlightenment=(2, 350)
        )

        await message.reply(f'Skin définis sur shadow Mewscles')

    if "!brainiacghoul" in args[0].lower():
        if message.author.display_name in data['BlockList']:
            await message.reply("Vous n'avez pas accès à cette commande!")
        else:
            try:
                variants = client.party.me.create_variants(
                   material=2
                )

                await client.party.me.set_outfit(
                    asset='CID_029_Athena_Commando_F_Halloween',
                    variants=variants
                )

                await message.reply('Skin définis sur Brainiac Ghoul Trooper!')
                print(f" [DairkXkizu] [{getTime()}] Client du skins définis sur Brainiac Ghoul Trooper")
            except Exception as e:
                pass

    if "!purpleportal" in args[0].lower():
        if message.author.display_name in data['BlockList']:
            await message.reply("Vous n'avez pas accès à cette commande!")
        else:
            variants = client.party.me.create_variants(
                item='AthenaBackpack',
                particle_config='Particle',
                particle=1
            )

            await client.party.me.set_backpack(
                asset='BID_105_GhostPortal',
                variants=variants
            )

            await message.reply('Sac a dos définis sur Purple Ghost Portal!')
            print(f" [DairkXkizu] [{getTime()}] Client sac a dos définis sur Purple Ghost Portal")

    if "!banner" in args[0].lower():
        if message.author.display_name in data['BlockList']:
            await message.reply("Vous n'avez pas accès à cette commande!")
        else:
            if len(args) == 1:
                await message.reply('Vous devez spécifier la bannière, la couleur et le niveau auxquels vous souhaitez définir la bannière.')
            if len(args) == 2:
                await client.party.me.set_banner(icon=args[1], color=data['banner_color'], season_level=data['level'])
            if len(args) == 3:
                await client.party.me.set_banner(icon=args[1], color=args[2], season_level=data['level'])
            if len(args) == 4:
                await client.party.me.set_banner(icon=args[1], color=args[2], season_level=args[3])

            await message.reply(f'Banner définis sur; {args[1]} {args[2]} {args[3]}')
            print(f" [DairkXkizu] [{getTime()}] Banner définis sur; {args[1]} {args[2]} {args[3]}")

    if "CID_" in args[0]:
        if message.author.display_name in data['BlockList']:
            await message.reply("Vous n'avez pas accès à cette commande!")
        else:
            await client.party.me.set_outfit(
                asset=args[0]
            )
            await message.reply(f'Skin définis sur {args[0]}')
            print(f' [DairkXkizu] [{getTime()}] Skin définis sur ' + args[0])

    if "!variants" in args[0]:
        if message.author.display_name in data['BlockList']:
            await message.reply("Vous n'avez pas accès à cette commande!")
        else:
            args3 = int(args[3])

            if 'CID' in args[1]:
                variants = client.party.me.create_variants(**{args[2]: args3})
                await client.party.me.set_outfit(
                    asset=args[1],
                    variants=variants
                )
            elif 'BID' in args[1]:
                variants = client.party.me.create_variants(item='AthenaBackpack', **{args[2]: args3})
                await client.party.me.set_backpack(
                    asset=args[1],
                    variants=variants
                )
            elif 'PICKAXE_ID' in args[1]:
                variants = client.party.me.create_variants(item='AthenaPickaxe', **{args[2]: args3})
                await client.party.me.set_pickaxe(
                    asset=args[1],
                    variants=variants
                )

            await message.reply(f'Définir des variantes de {args[1]} to {args[2]} {args[3]}.')
            print(f' [DairkXkizu] [{getTime()}] SDéfinir des variantes de {args[1]} to {args[2]} {args[3]}.')

    if "!checkeredrenegade" in args[0].lower():
        if message.author.display_name in data['BlockList']:
            await message.reply("Vous n'avez pas accès à cette commande!")
        else:
            variants = client.party.me.create_variants(
               material=2
            )

            await client.party.me.set_outfit(
                asset='CID_028_Athena_Commando_F',
                variants=variants
            )

            await message.reply('Skin définis sur Checkered Renegade 2!')
            print(f" [DairkXkizu] [{getTime()}] Client du skins définis sur Checkered Renegade")

    if "!mintyelf" in args[0].lower():
        if message.author.display_name in data['BlockList']:
            await message.reply("YVous n'avez pas accès à cette commande!")
        else:
            variants = client.party.me.create_variants(
                   material=2
                )

            await client.party.me.set_outfit(
                asset='CID_051_Athena_Commando_M_HolidayElf',
                variants=variants
                )

            await message.reply('Skin définis sur Minty Elf!')
            print(f" [DairkXkizu] [{getTime()}] Client du skins définis sur Minty Elf")
            
    if "!hologram" in args[0].lower():
        if message.author.display_name in data['BlockList']:
            await message.reply("Vous n'avez pas accès à cette commande!")
        else:
            variants = client.party.me.create_variants(
                   material=2
                )

            await client.party.me.set_outfit(
                asset='CID_VIP_Athena_Commando_M_GalileoGondola_SG',
                variants=variants
                )

            await message.reply('Skin définis sur hologram!')
            print(f" [DairkXkizu] [{getTime()}] Client'du skins definis sur hologram")
            
    if "!ghost" in args[0].lower():
        if message.author.display_name in data['BlockList']:
            await message.reply("Vous n'avez pas accès à cette commande!")
        else:
            variants = client.party.me.create_variants(
                   material=2
                )

            await client.party.me.set_outfit(
                asset='CID_NPC_Athena_Commando_M_HenchmanGood',
                variants=variants
                )

            await message.reply('Skin définis sur ghost henchman!')
            print(f" [DairkXkizu] [{getTime()}] Client du skins définis sur ghost henchman")
            
    if "!shadow" in args[0].lower():
        if message.author.display_name in data['BlockList']:
            await message.reply("Vous n'avez pas accès à cette commande!")
        else:
            variants = client.party.me.create_variants(
                   material=2
                )

            await client.party.me.set_outfit(
                asset='CID_NPC_Athena_Commando_M_Henchmanbad',
                variants=variants
                )

            await message.reply('Skin définis sur shadow henchman!')
            print(f" [DairkXkizu] [{getTime()}] Client du skins définis sur shadow henchman")
            
    if "!oil" in args[0].lower():
        if message.author.display_name in data['BlockList']:
            await message.reply("Vous n'avez pas accès à cette commande!")
        else:
            variants = client.party.me.create_variants(
                   material=2
                )

            await client.party.me.set_outfit(
                asset='CID_NPC_Athena_Commando_M_tacticalfishermanoil',
                variants=variants
                )

            await message.reply('Skin définis sur dirty henchman!')
            print(f" [DairkXkizu] [{getTime()}] Client du skins définis sur dirty henchman")
            
    if "!arctic" in args[0].lower():
        if message.author.display_name in data['BlockList']:
            await message.reply("Vous n'avez pas accès à cette commande!")
        else:
            variants = client.party.me.create_variants(
                   material=2
                )

            await client.party.me.set_outfit(
                asset='CID_NPC_Athena_Commando_M_paddedarmorarctic',
                variants=variants
                )

            await message.reply('Skin définis sur cold henchman!')
            print(f" [DairkXkizu] [{getTime()}] Client du skins définis sur cold henchman")
            
    if "!bot" in args[0].lower():
        if message.author.display_name in data['BlockList']:
            await message.reply("Vous n'avez pas accès à cette commande!")
        else:
            variants = client.party.me.create_variants(
                   material=2
                )

            await client.party.me.set_outfit(
                asset='CID_005_Athena_Commando_M_DEFAULT',
                variants=variants
                )

            await message.reply('Skin définis sur BOT :)')
            print(f" [DairkXkizu] [{getTime()}] Client du skins définis sur bot")
            
    if "!bot1" in args[0].lower():
        if message.author.display_name in data['BlockList']:
            await message.reply("Vous n'avez pas accès à cette commande!")
        else:
            variants = client.party.me.create_variants(
                   material=2
                )

            await client.party.me.set_outfit(
                asset='CID_001_Athena_Commando_F_DEFAULT',
                variants=variants
                )

            await message.reply('Skin définis sur BOT :)')
            print(f" [DairkXkizu[{getTime()}] Client du skins définis sur bot")
            
    if "!bot2" in args[0].lower():
        if message.author.display_name in data['BlockList']:
            await message.reply("Vous n'avez pas accès à cette commande!")
        else:
            variants = client.party.me.create_variants(
                   material=2
                )

            await client.party.me.set_outfit(
                asset='CID_002_Athena_Commando_F_DEFAULT',
                variants=variants
                )

            await message.reply('Skin définis sur BOT :)')
            print(f" [DairkXkizu] [{getTime()}] Client du skins définis sur bot")
            
    if "!bot3" in args[0].lower():
        if message.author.display_name in data['BlockList']:
            await message.reply("Vous n'avez pas accès à cette commande!")
        else:
            variants = client.party.me.create_variants(
                   material=2
                )

            await client.party.me.set_outfit(
                asset='CID_003_Athena_Commando_F_DEFAULT',
                variants=variants
                )

            await message.reply('Skin définis sur BOT :)')
            print(f" [DairkXkizu] [{getTime()}] Client du skins définis sur bot")
            
    if "!bot4" in args[0].lower():
        if message.author.display_name in data['BlockList']:
            await message.reply("Vous n'avez pas accès à cette commande!")
        else:
            variants = client.party.me.create_variants(
                   material=2
                )

            await client.party.me.set_outfit(
                asset='CID_004_Athena_Commando_F_DEFAULT',
                variants=variants
                )

            await message.reply('Skin définis sur BOT :)')
            print(f" [DairkXkizu] [{getTime()}] Client du skins définis sur bot")
            
    if "!bot5" in args[0].lower():
        if message.author.display_name in data['BlockList']:
            await message.reply("Vous n'avez pas accès à cette commande!")
        else:
            variants = client.party.me.create_variants(
                   material=2
                )

            await client.party.me.set_outfit(
                asset='CID_006_Athena_Commando_M_DEFAULT',
                variants=variants
                )

            await message.reply('Skin définis sur BOT :)')
            print(f" [DairkXkizu] [{getTime()}] Client du skins définis sur bot")
            
    if "!bot6" in args[0].lower():
        if message.author.display_name in data['BlockList']:
            await message.reply("Vous n'avez pas accès à cette commande!")
        else:
            variants = client.party.me.create_variants(
                   material=2
                )

            await client.party.me.set_outfit(
                asset='CID_007_Athena_Commando_M_DEFAULT',
                variants=variants
                )

            await message.reply('Skin définis sur BOT :)')
            print(f" [DairkXkizu] [{getTime()}] Client' du skins définis sur bot")
            
    if "!bot7" in args[0].lower():
        if message.author.display_name in data['BlockList']:
            await message.reply("Vous n'avez pas accès à cette commande!")
        else:
            variants = client.party.me.create_variants(
                   material=2
                )

            await client.party.me.set_outfit(
                asset='CID_008_Athena_Commando_M_DEFAULT',
                variants=variants
                )

            await message.reply('Skin définis sur BOT :)')
            print(f" [DairkXkizu] [{getTime()}] Client du skins définis sur bot")

    if "EID_" in args[0]:
        if message.author.display_name in data['BlockList']:
            await message.reply("Vous n'avez pas accès à cette commande!")
        else:
            await client.party.me.clear_emote()
            await client.party.me.set_emote(
                asset=args[0]
            )
            await message.reply('Emote définis sur ' + args[0] + '!')
        
    if "!stop" in args[0].lower():
        if message.author.display_name in data['BlockList']:
            await message.reply("Vous n'avez pas accès à cette commande!")
        else:
            await client.party.me.clear_emote()
            await message.reply('Emote stopé.')

    if "BID_" in args[0]:
        if message.author.display_name in data['BlockList']:
            await message.reply("Vous n'avez pas accès à cette commande!")
        else:
            await client.party.me.set_backpack(
                asset=args[0]
            )

            await message.reply('Sac a dos définis sur ' + message.content + '!')

    if "help" in args[0].lower():
        if message.author.display_name in data['BlockList']:
            await message.reply("Vous n'avez pas accès à cette commande!")
        else:
            await message.reply('commande bientot dispo bb dev by Kizu & dairkoos.')

    if "Pickaxe_" in args[0]:
        if message.author.display_name in data['BlockList']:
            await message.reply("Vous n'avez pas accès à cette commande!")
        else:
            await client.party.me.set_pickaxe(
                    asset=args[0]
            )

            await message.reply('Pioche définis sur ' + args[0] + '!')

    if "PetCarrier_" in args[0]:
        if message.author.display_name in data['BlockList']:
            await message.reply("Vous n'avez pas accès à cette commande!")
        else:
            await client.party.me.set_backpack(
                    asset="/Game/Athena/Items/Cosmetics/PetCarriers/" + args[0] + "." + args[0]
            )

    if "Emoji_" in args[0]:
        if message.author.display_name in data['BlockList']:
            await message.reply("Vous n'avez pas accès à cette commande!")
        else:
            await client.party.me.set_emote(asset='EID_ClearEmote')
            await client.party.me.set_emote(
                    asset="/Game/Athena/Items/Cosmetics/Dances/Emoji/" + args[0] + "." + args[0]
            )

    if "!pret" in args[0].lower():
        if message.author.display_name in data['BlockList']:
            await message.reply("Vous n'avez pas accès à cette commande!")
        else:
            await client.party.me.set_ready(fortnitepy.ReadyState.READY)
            await message.reply('Maintenant pret!')

    if ("!unpret" in args[0].lower()) or ("!attente" in args[0].lower()):
        if message.author.display_name in data['BlockList']:
            await message.reply("Vous n'avez pas accès à cette commande!")
        else:
            await client.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
            await message.reply('maintenant enlevé pret!')

    if "!attente" in args[0].lower():
        if message.author.display_name in data['BlockList']:
            await message.reply("Vous n'avez pas accès à cette commande!")
        else:
            await client.party.me.set_ready(fortnitepy.ReadyState.SITTING_OUT)
            await message.reply('maintenant en attente !')
    
    if "!bp" in args[0].lower():
        if message.author.display_name in data['BlockList']:
            await message.reply("Vous n'avez pas accès à cette commande!")
        else:
            await client.party.me.set_battlepass_info(has_purchased=True, level=args[1], self_boost_xp='0', friend_boost_xp='0')
    
    if "!level" in args[0].lower():
        if message.author.display_name in data['BlockList']:
            await message.reply("Vous n'avez pas accès à cette commande!")
        else:
            await client.party.me.set_banner(icon=client.party.me.banner[0], color=client.party.me.banner[1], season_level=args[1])
    
    if "!reset" in args[0].lower():
        if message.author.display_name in data['BlockList']:
            await message.reply("Vous n'avez pas accès à cette commande!")
        else:
            variants = client.party.me.create_variants(**{data['variants-type']: data['variants']})
            await client.party.me.set_outfit(asset=data['cid'], variants=variants)
            await client.party.me.set_backpack(asset=data['bid'])
            await client.party.me.set_banner(icon=data['banner'], color=data['banner_color'], season_level=data['level'])
            await client.party.me.set_pickaxe(asset=data['pid'])
            await client.party.me.set_battlepass_info(has_purchased=True, level=data['bp_tier'], self_boost_xp='0', friend_boost_xp='0')
            await message.reply(f"Rétablir le chargement cosmétique par défaut.")

    if "!echo" in args[0].lower():
        if message.author.display_name in data['FullAccess']:
            await client.party.send(joinedArguments)
            print(f' [DairkXkizu] [{getTime()}] ' + color.GREEN + 'message envoyé:' + color.END + f' {joinedArguments}')
        else:
            if message.author.display_name not in data['FullAccess']:
                await message.reply(f"Vous n'avez pas accès à cette command!")

    if "!admin" in args[0].lower():
        if message.author.display_name in data['FullAccess']:
            if len(args) == 1:
                await message.reply('Veuillez spécifier si vous souhaitez ajouter ou supprimer un utilisateur de la liste des administrateurs')
                print(f' [DairkXkizu] [{getTime()}] Veuillez spécifier si vous souhaitez ajouter ou supprimer un utilisateur de la liste des administrateurs, en utilisant ' + color.GREEN + '!admin add ' + color.END + 'ou ' + color.GREEN + '!admin remove' + color.END)
            if len(args) == 2:
                if args[1].lower() == 'add':
                    await message.reply('Vous êtes déjà administrateur')
                elif args[1].lower() == 'remove':
                    await message.reply('Voulez-vous vraiment être supprimé en tant que administrateur?')
                    res = await client.wait_for('friend_message')
                    content = res.content.lower()
                    user = await client.fetch_profile(message.author.id, cache=False, raw=False)
                    if content == "oui":
                        data['FullAccess'].remove(user.display_name)
                        with open('config.json', 'w') as f:
                            json.dump(data, f, indent=4)
                            print(f" [DairkXkizu] [{getTime()}] Retiré " + color.GREEN + f"{user.display_name}" + color.END + " en tant qu'administrateur")
                            await message.reply(f"Vous avez été supprimé en tant qu'administrateur.")
                    elif content == "non":
                            await message.reply(f"Vous avez été conservé en tant qu'administrateur.")
                    else:
                        await message.reply(f'Pas une réponse correcte, essayez "oui" or "non"')
                else:
                    await message.reply('Utilisation invalide, essayé !admin add <pseudo> or !admin remove <pseudo>')
            if len(args) >= 3:
                joinedArgumentsAdmin = " ".join(args[2:])
                user = await client.fetch_profile(joinedArgumentsAdmin)
                try:
                    if args[1].lower() == 'add':
                        if user.display_name not in data['FullAccess']:
                            data['FullAccess'].append(f"{user.display_name}")
                            with open('config.json', 'w') as f:
                                json.dump(data, f, indent=4)
                                print(f" [DairkXkizu] [{getTime()}] Ajouté " + color.GREEN + f"{user.display_name}" + color.END + " en tant qu'administrateur")
                                await message.reply(f"Added {user.display_name} as an admin.")
                        elif user.display_name in data['FullAccess']:               
                            print(f" [DairkXkizu] [{getTime()}]" + color.GREEN + f" {user.display_name}" + color.END + " est déjà administrateur")
                            await message.reply(f"{user.display_name} est déjà administrateur.")
                    elif args[1].lower() == 'remove':
                        if user.display_name in data['FullAccess']:
                            data['FullAccess'].remove(user.display_name)
                            with open('config.json', 'w') as f:
                                json.dump(data, f, indent=4)
                                print(f" [DairkXkizu] [{getTime()}] retiré " + color.GREEN + f"{user.display_name}" + color.END + " en tant qu'administrateur")
                                await message.reply(f"Retiré {user.display_name} en tant qu'administrateur.")
                        elif user.display_name not in data['FullAccess']:
                            print(f" [DairkXkizu] [{getTime()}]" + color.GREEN + f" {user.display_name}" + color.END + " n'est pas admin")
                            await message.reply(f"{user.display_name} iest pas admin.")
                except AttributeError:
                    pass
                    print(f" [DairkXkizu] [{getTime()}] Impossible de trouver l'utilisateur: " + color.GREEN + f"{joinedArgumentsAdmin}" + color.END)
                    await message.reply(f"Je n'ai pas trouvé de compte Epic avec le pseudo: {joinedArgumentsAdmin}.")
        if message.author.display_name not in data['FullAccess']:
            if len(args) >= 3 and args[1].lower() == 'add':
                await message.reply(f"mot de passe ?")
                res = await client.wait_for('friend_message')
                content = res.content.lower()
                joinedArgumentsAdmin = " ".join(args[2:])
                user = await client.fetch_profile(joinedArgumentsAdmin)
                if content in data['AdminPassword']:
                    if user.display_name not in data['FullAccess']:
                        data['FullAccess'].append(f"{user.display_name}")
                        with open('config.json', 'w') as f:
                            json.dump(data, f, indent=4)
                            await message.reply(f"Correct. ajouté {user.display_name} en tant que admin")
                            print(f" [DairkXkizu] [{getTime()}] Ajouté " + color.GREEN + f"{user.display_name}" + color.END + " est admin")
                    elif user.display_name in data['FullAccess']:
                        print(f" [DairkXkizu] [{getTime()}]" + color.GREEN + f" {user.display_name}" + color.END + " is already an admin")
                        await message.reply(f"{user.display_name} est deja admin.")
                else:
                    await message.reply(f"Incorrect mot de passe")
            elif len(args) == 2 and args[1].lower() == 'add':
                await message.reply('mot de passe?')
                res = await client.wait_for('friend_message')
                content = res.content.lower()
                user = await client.fetch_profile(message.author.id, cache=False, raw=False)
                if content in data['AdminPassword']:
                    data['FullAccess'].append(f"{user.display_name}")
                    with open('config.json', 'w') as f:
                        json.dump(data, f, indent=4)
                        await message.reply(f"Correct! Vous avez été ajouté en tant qu'administrateur.")
                        print(f" [DairkXkizu [{getTime()}] Ajouté " + color.GREEN + f"{user.display_name}" + color.END + " en tant que admin")
                else:
                    await message.reply(f"Incorrect mot de passe")
            else:
                await message.reply(f"Vous n'avez pas accès à cette commande!")

    if "!blocklist" in args[0].lower():
        if message.author.display_name in data['FullAccess']:
            if len(args) == 1:
                await message.reply('Veuillez spécifier si vous souhaitez ajouter ou supprimer un utilisateur du bloclist')
                print(f' [DairkXkizu] [{getTime()}] Veuillez spécifier si vous souhaitez ajouter ou supprimer un utilisateur de la liste des administrateurs, en utilisant ' + color.GREEN + '!admin add ' + color.END + 'or ' + color.GREEN + '!admin remove' + color.END)
            if len(args) == 2:
                if args[1].lower() == 'add' or args[1].lower() == 'remove':
                    await message.reply('Veuillez spécifier si vous souhaitez ajouter ou supprimer un utilisateur du bloclist')
                    print(f' [DairkXkizu] [{getTime()}] Veuillez spécifier si vous souhaitez ajouter ou supprimer un utilisateur du bloclist')
                else:
                    await message.reply('utilisation non valide, essayez !blocklist add <pseudo> or !blocklist remove <pseudo>')
                    print(f' [DairkXkizu] [{getTime()}] utilisation non valide, essayez ' + color.GREEN + '!BlockList add <pseudo> ' + color.END + 'ou ' + color.GREEN + '!BlockList remove <pseudo>' + color.END)
            if len(args) >= 3:
                joinedArgumentsAdmin = " ".join(args[2:])
                user = await client.fetch_profile(joinedArgumentsAdmin)
                if args[1].lower() == 'add':
                    if user.display_name not in data['FullAccess'] and user.display_name not in data['BlockList']:
                        data['BlockList'].append(f"{user.display_name}")
                        with open('config.json', 'w') as f:
                            json.dump(data, f, indent=4)
                            await message.reply(f"Ajouté {user.display_name} à la liste bloquée.")
                            print(f" [DairkXkizu] [{getTime()}] Ajouté " + color.GREEN + f"{user.display_name}" + color.END + " à la liste bloquée.")
                    elif user.display_name in data['FullAccess']:
                        await message.reply(f"{user.display_name} ne peut pas être ajouté à la liste bloquée.")
                        print(f" [DairkXkizu] [{getTime()}]" + color.GREEN + f" {user.display_name}" + color.END + " ne peut pas être ajouté à la liste bloquée.")
                    elif user.display_name in data['BlockList']:               
                        await message.reply(f"{user.display_name} est déja ajouté au blocklis.")
                        print(f" [DairkXkizu] [{getTime()}]" + color.GREEN + f" {user.display_name}" + color.END + " est déja ajouté au blocklis.")
                elif args[1].lower() == 'remove':
                    if user.display_name in data['BlockList']:
                        data['BlockList'].remove(user.display_name)
                        with open('config.json', 'w') as f:
                            json.dump(data, f, indent=4)
                            print(f" [DairkXkizu] [{getTime()}] Removed " + color.GREEN + f"{user.display_name}" + color.END + " du blocklist.")
                    elif user.display_name not in data['BlockList']:
                        print(f" [DairkXkizu] [{getTime()}]" + color.GREEN + f" {user.display_name}" + color.END + " n'est pas ajouté au blocklist.")
        if message.author.display_name not in data['FullAccess']:
            if len(args) >= 3 and args[1].lower() == 'add':
                await message.reply(f"mot de passe?")
                res = await client.wait_for('friend_message')
                content = res.content.lower()
                joinedArgumentsAdmin = " ".join(args[2:])
                user = await client.fetch_profile(joinedArgumentsAdmin)
                if content in data['AdminPassword']:
                    if user.display_name not in data['BlockList']:
                        data['BlockList'].append(f"{user.display_name}")
                        with open('config.json', 'w') as f:
                            json.dump(data, f, indent=4)
                            await message.reply(f"Correct. ajouté {user.display_name} au blocklist")
                            print(f" [DairkXkizu] [{getTime()}] Added " + color.GREEN + f"{user.display_name}" + color.END + " au blocklist.")
                    elif user.display_name in data['BlockList']:
                        print(f" [DairkXkizu] [{getTime()}]" + color.GREEN + f" {user.display_name}" + color.END + " ne peut pas etre ajouté au blocklust")
                        await message.reply(f"{user.display_name} ne peut pas etre ajouté au blocklist")
                elif args[1].lower() == 'remove':
                    await message.reply(f"mot de passe?")
                    res = await client.wait_for('friend_message')
                    content = res.content.lower()
                    joinedArgumentsAdmin = " ".join(args[2:])
                    user = await client.fetch_profile(joinedArgumentsAdmin)
                    if content in data['AdminPassword']:
                        if user.display_name in data['BlockList']:
                            data['BlockList'].remove(user.display_name)
                            with open('config.json', 'w') as f:
                                json.dump(data, f, indent=4)
                                print(f" [DairkXkizu] [{getTime()}] Removed " + color.GREEN + f"{user.display_name}" + color.END + " du blocklist.")
                        elif user.display_name not in data['BlockList']:
                            print(f" [DairkXkizu] [{getTime()}]" + color.GREEN + f" {user.display_name}" + color.END + " est deja retire du blocklist.")
            else:
                await message.reply(f"Vous n'avez pas accès à cette commande!")

    if "!status" in args[0].lower():
        if message.author.display_name in data['FullAccess']:
            await client.set_status(joinedArguments)
            await message.reply(f'Status définis sur {joinedArguments}')
            print(f' [DairkXkizu] [{getTime()}] Status définis sur  {joinedArguments}.')
        else:
            if message.author.display_name not in data['FullAccess']:
                await message.reply(f"Vous n'avez pas accès à cette commande!")
            
    if "!quitte" in args[0].lower():
        if message.author.display_name in data['FullAccess']:
            await client.party.me.set_emote('EID_Snap')
            delay.sleep(2)
            await client.party.me.leave()
            await message.reply('Bye!')
            print(Fore.GREEN + f' [DairkXkizu] [{getTime()}] quitte comme on me la demande.')
        else:
            if message.author.display_name not in data['FullAccess']:
                await message.reply(f"Vous n'avez pas accès à cette commande!")

    if "!kick" in args[0].lower() and message.author.display_name in data['FullAccess']:
        user = await client.fetch_profile(joinedArguments)
        member = client.party.members.get(user.id)
        if member is None:
            await message.reply("Impossible de trouver cet utilisateur, êtes-vous sûr qu'il fait partie du groupe?")
        else:
            try:
                await member.kick()
                await message.reply(f"user exclu: {member.display_name}.")
                print(Fore.GREEN + f" [DairkXkizu] [{getTime()}] user exclu: {member.display_name}")
            except Exception as e:
                pass
                await message.reply(f"Impossible de l'exclure {member.display_name}, je ne suis pas chef.")
                print(Fore.RED + f" [DairkXkizu] [{getTime()}] [ERROR] Impossible de renvoyer le membre car je n'ai pas les autorisations requises." + Fore.WHITE)
        if message.author.display_name not in data['FullAccess']:
            await message.reply(f"Vous n'avez pas accès à cette commande!")

    if "!join" in args[0] and message.author.display_name in data['FullAccess']:
        if len(args) != 1:
            user = await client.fetch_profile(joinedArguments)
            friend = client.get_friend(user.id)
        if len(args) == 1:
            user = await client.fetch_profile(message.author.id, cache=False, raw=False)
            friend = client.get_friend(user.id)
        if friend is None:
            await message.reply(f"Impossible d'inviter cet utilisateur, êtes-vous sûr que le bot les a ajoutés?")
            print(Fore.RED + f" [DairkXkizu] [{getTime()}] [ERROR] Impossible de rejoindre l'utilisateur: {joinedArguments}, êtes-vous sûr que le bot les a ajoutés?" + Fore.WHITE)
        if message.author.display_name not in data['FullAccess']:
            await message.reply(f"Vous n'avez pas accès à cette commande!")
        else:
            try:
                await friend.join_party()
                await message.reply(f"rejoins {friend.display_name} le groupe.")
            except Exception as e:
                await message.reply(f"Impossible de rejoindre le groupe d'utilisateurs.")

    if "!invite" in args[0].lower():
        if len(args) != 1:
            user = await client.fetch_profile(joinedArguments)
            friend = client.get_friend(user.id)
        if len(args) == 1:
            user = await client.fetch_profile(message.author.id, cache=False, raw=False)
            friend = client.get_friend(user.id)
        if friend is None:
            await message.reply(f"impossible d'inviter cet utilisateur, êtes-vous sûr que le bot les a ajoutés?")
            print(Fore.RED + f" [DairkXkizu] [{getTime()}] [ERROR] Impossible d'inviter l'utilisateur: {joinedArguments}, êtes-vous sûr que le bot les a ajoutés?" + Fore.WHITE)
        else:
            try:
                await friend.invite()
                await message.reply(f"user invité: {friend.display_name}.")
                print(Fore.GREEN + f" [DairkXkizu] [{getTime()}] user invité: {friend.display_name}")
            except Exception as e:
                pass
                await message.reply(f"Une erreur s'est produite lors de l'invitation {friend.display_name}")
                print(Fore.RED + f" [DairkXkizu] [{getTime()}] [ERROR] Une erreur s'est produite lors de l'invitation {friend.display_name}" + Fore.WHITE)           

    if "!add" in args[0].lower() and message.author.display_name in data['FullAccess']:
        user = await client.fetch_profile(joinedArguments)
        friends = client.friends
        if user is None:
            await message.reply(f"Je ne trouve pas de joueur avec le nom de {joinedArguments}.")
            print(Fore.RED + f" [DairkXkizu] [{getTime()}] [ERROR] Je ne trouve pas de joueur avec le nom de {joinedArguments}")
        else:
            try:
                if (user.id in friends):
                    await message.reply(f"j'ai déjà {user.display_name} en amis.")
                    print(Fore.RED + f" [DairkXkizu] [{getTime()}] [ERROR] vous avais déja  {user.display_name} amis")
                else: 
                    await client.add_friend(user.id)
                    await message.reply(f"succes demande d'amis envoyé a {user.display_name}")
                    print(Fore.GREEN + f" [DairkXkizu] [{getTime()}] {client.user.display_name} demande d'amis envoyé a  {user.display_name}" + Fore.WHITE)
            except Exception as e:
                pass
                print(Fore.RED + f" [DairkXkizu] [{getTime()}] [ERROR] Une erreur s'est produite lors de l'ajout {joinedArguments}" + Fore.WHITE)
        if message.author.display_name not in data['FullAccess']:
            await message.reply(f"Vous n'avez pas accès à cette commande!")

    if "!remove" in args[0].lower() and message.author.display_name in data['FullAccess']:
        user = await client.fetch_profile(joinedArguments)
        friends = client.friends
        if user is None:
            await message.reply(f"Je ne trouve pas de joueur avec le nom de {joinedArguments}.")
            print(Fore.RED + f" [DairkXkizu] [{getTime()}] [ERROR] Je ne trouve pas de joueur avec le nom de {joinedArguments}")
        else:
            try:
                if (user.id in friends):
                    await client.remove_or_decline_friend(user.id)
                    await message.reply(f"retiré avec succes {user.display_name} as a friend.")
                    print(Fore.GREEN + f" [DairkXkizu] [{getTime()}] {client.user.display_name} retiré {user.display_name} en tant que amis.")
                else: 
                    await message.reply(f"vous avais pas {user.display_name} aen tant que amis")
                    print(Fore.RED + f" [DairkXkizu] [{getTime()}] [ERROR] {client.user.display_name} essayé de supprimer {user.display_name} en tant qu'ami, mais le client n'a pas ajouté l'ami." + Fore.WHITE)
            except Exception as e:
                pass
                print(Fore.RED + f" [DairkXkizu] [{getTime()}] [ERROR] Une erreur s'est produite lors de la suppression {joinedArguments} de l'amis" + Fore.WHITE)
        if message.author.display_name not in data['FullAccess']:
            await message.reply(f"Vous n'avez pas accès à cette commande!")

    if "!amis" in args[0].lower() and message.author.display_name in data['FullAccess']:
        friends = client.friends
        onlineFriends = []
        offlineFriends = []
        try:
            for f in friends:
                friend = client.get_friend(f)
                if friend.is_online():
                    onlineFriends.append(friend.display_name)
                else:
                    offlineFriends.append(friend.display_name)
            print(f" [DairkXkizu] [{getTime()}] " + Fore.WHITE + "Liste d'amis: " + Fore.GREEN + f"{len(onlineFriends)} connécté " + Fore.WHITE + "/" + Fore.LIGHTBLACK_EX + f" {len(offlineFriends)} déconnecté " + Fore.WHITE + "/" + Fore.LIGHTWHITE_EX + f" {len(onlineFriends) + len(offlineFriends)} Total")
            for x in onlineFriends:
                if x is not None:
                    print(Fore.GREEN + " " + x + Fore.WHITE)
            for x in offlineFriends:
                if x is not None:
                    print(Fore.LIGHTBLACK_EX + " " + x + Fore.WHITE)
        except Exception as e:
            pass
        await message.reply("Vérifiez la fenêtre de Dairkoos x Kizu pour la liste de mes amis.")   
        if message.author.display_name not in data['FullAccess']:
            await message.reply(f"Vous n'avez pas accès à cette commande!")

    if "!members" in args[0].lower() and message.author.display_name in data['FullAccess']:
            members = client.party.members
            partyMembers = []
            for m in members:
                member = client.get_user(m)
                partyMembers.append(member.display_name)
            print(f" [DairkXkizu] [{getTime()}] " + Fore.WHITE + "There are " + Fore.LIGHTWHITE_EX + f"{len(partyMembers)} members in client's party:")
            await message.reply(f"There are {len(partyMembers)} members in {client.user.display_name}'s party:")
            for x in partyMembers:
                if x is not None:
                    print(Fore.GREEN + " " + x + Fore.WHITE)
                    await message.reply(x)

    if "!promote" in args[0].lower() and message.author.display_name in data['FullAccess']:
        if len(args) != 1:
            user = await client.fetch_profile(joinedArguments)
            member = client.party.members.get(user.id)
        if len(args) == 1:
            user = await client.fetch_profile(message.author.display_name)
            member = client.party.members.get(user.id)
        if member is None:
            await message.reply("Couldn't find that user, are you sure they're in the party?")
        else:
            try:
                await member.promote()
                await message.reply(f"Promoted user: {member.display_name}.")
                print(Fore.GREEN + f" [DairkXkizu] [{getTime()}] Promoted user: {member.display_name}")
            except Exception as e:
                pass
                await message.reply(f"Couldn't promote {member.display_name}, as I'm not party leader.")
                print(Fore.RED + f" [DairkXkizu] [{getTime()}] [ERROR] Failed to promote member as I don't have the required permissions." + Fore.WHITE)
        if message.author.display_name not in data['FullAccess']:
            await message.reply(f"You don't have access to this command!")

    if "Playlist_" in args[0]:
        try:
            await client.party.set_playlist(playlist=args[0])
        except Exception as e:
            pass
            await message.reply(f"Couldn't set gamemode to {args[0]}, as I'm not party leader.")
            print(Fore.RED + f" [DairkXkizu] [{getTime()}] [ERROR] Failed to set gamemode as I don't have the required permissions." + Fore.WHITE)

    if "!platform" in args[0] and message.author.display_name in data['FullAccess']:
        await message.reply('Setting platform to ' + args[1] + '.')
        party_id = client.party.id
        await client.party.me.leave()
        client.platform = fortnitepy.Platform(args[1])
        await message.reply('Platform set to ' + str(client.platform) + '.')
        try:
            await client.join_to_party(party_id, check_private=True)
        except Exception as e:
            pass
            await message.reply('Failed to join back as party is set to private.')
        else:
            if message.author.display_name not in data['FullAccess']:
                await message.reply(f"You don't have access to this command!")

    if args[0] == "!id":
        if message.author.display_name in data['BlockList']:
            await message.reply("You don't have access to this command!")
        else:
            user = await client.fetch_profile(joinedArguments, cache=False, raw=False)
            try:
                await message.reply(f"{joinedArguments}'s Epic ID is: {user.id}")
                print(Fore.GREEN + f" [DairkXkizu] [{getTime()}] {joinedArguments}'s Epic ID is: {user.id}")
            except AttributeError:
                await message.reply(f"I couldn't find an Epic account with the name: {joinedArguments}.")
                print(Fore.RED + f" [DairkXkizu] [{getTime()}] [ERROR] I couldn't find an Epic account with the name: {joinedArguments}.")

try:
    client.run()
except fortnitepy.AuthException as e:
    print(Fore.RED + f" [DairkXkizu] [{getTime()}] [ERROR] {e}")
