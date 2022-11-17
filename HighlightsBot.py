# HighlightsBot by daishin
#Ver.0.0 2022/10/10
#Ver.0.1 2022/10/11
#Ver.0.2 2022/10/20
#Ver.0.3 2022/10/20
#Ver.0.4 2022/11/13
#Ver.1.0 2022/11/17 Change a logic

import discord
import re
import deepl

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

TOKEN = '*****'
HLJA = "highlights-ja"
HLEN = "highlights-en"
NumOfReactions=1

MessageIdSet = set()

def is_japanese(str):
	return True if re.search(r'[ぁ-んァ-ン]', str) else False

@client.event
async def on_ready():
	print('start.')

@client.event
async def on_reaction_add(reaction, user):
	if reaction.message.author.bot:
		print("This is bot msg. Ignored.")
		return
	
	A = reaction.count
	print("A:reaction.count : " + str(A))
	
	users = [user async for user in reaction.users()]
	B = len(users)
	print(users)
	print("B:users : " + str(B))
	
	print(reaction.message.reactions)
	C = len(reaction.message.reactions)
	print("C:reaction.message.reactions : " + str(C))
	
	_s = set()
	for _reaction in reaction.message.reactions:
		_users = [user async for user in _reaction.users()]
		print(_users)
		for _user in _users:
			_s.add(_user)
	print(_s)
	D =len(_s)
	print("D:Users in set : " + str(D))
	
	print(reaction.message.content)
	
	MyCount = D
	if MyCount%NumOfReactions == 0 and reaction.message.id not in MessageIdSet:
		
		MessageIdSet.add(reaction.message.id)
		msg = reaction.message.content
		
		if msg:
			translator = deepl.Translator("*****") 
			
			t_lang = "EN-US"
			result = translator.translate_text(msg, target_lang=t_lang)
			result_txt = result.text 
			source_lang = result.detected_source_lang

			if source_lang == "JA":
				org_post = HLJA
				res_post = HLEN
			else:
				t_lang = "JA"
				result = translator.translate_text(msg, target_lang=t_lang)
				result_txt = result.text 
				source_lang = result.detected_source_lang
				org_post = HLEN
				res_post = HLJA
			  
			msgAuthor = str(reaction.message.author.id)
			msgChannel = str(reaction.message.channel.id)
			
			msg0 = "A message posted by <@" + msgAuthor + "> got more than " + str(NumOfReactions) + " reactions in the channel <#" + msgChannel + ">\n"
			msg1 = "(This message is translated by DeepL.)\n"
			liner1 = "----\n\n"
			liner2 = "\n----\n"

			channel = discord.utils.get(reaction.message.guild.text_channels, name=org_post)
			orgMes = msg0 +liner1 + msg + "\n" + liner2 + reaction.message.jump_url
			embed1 = discord.Embed(description=orgMes,color=discord.Colour.from_rgb(130, 219, 216))
			embed1.set_thumbnail(url=reaction.message.author.avatar.url)
			await channel.send(embed=embed1)
			
			channel = discord.utils.get(reaction.message.guild.text_channels, name=res_post)
			resMes = msg0 + liner1 + result_txt + "\n" +liner2 + msg1 + reaction.message.jump_url
			embed2 = discord.Embed(description=resMes,color=discord.Colour.from_rgb(130, 219, 216))
			embed2.set_thumbnail(url=reaction.message.author.avatar.url)
			await channel.send(embed=embed2)
			
client.run(TOKEN)
