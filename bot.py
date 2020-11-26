#!/usr/bin/env python3
import discord
from discord.ext import commands
import datetime
from pysyllables import get_syllable_count
import json

TEST = True

try:
    conf = json.load(open("config.json"))
    if conf['token'] is None:
        raise Exception
    token = conf['token']
    if TEST:
        token = conf['token_test']
except Exception:
    print("Failed to open config, check it exists and is valid.")

bot = commands.Bot(command_prefix='>', description="Haiku Bot")

check_reaction = '✅'


dmfailed = discord.Embed(
    title="DM Failed",
    description='',
    timestamp=datetime.datetime.utcnow(),
    color=discord.Color.from_rgb(240, 71, 71)
)


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


@bot.command()
async def pingdm(ctx):
    try:
        await ctx.author.send('pong')
        await ctx.message.add_reaction(check_reaction)
    except discord.Forbidden:
        await ctx.send(embed=dmfailed)


@bot.command()
async def debughaiku(ctx):  # WIP
    try:
        msg_list = ctx.message.content.strip().split(" ")[1:]
        print(msg_list)
        syl = []
        sum = 0
        i = 0
        combined = [[] for _ in range(len(msg_list))]
        for word in msg_list:
            try:
                syl.append(get_syllable_count(word))
                combined[i].append(get_syllable_count(word))
                combined[i].append(word)
                sum += combined[i][0]
                i += 1
            except Exception:
                syl_error = word
        keep_going = True
        haiku = [[], [], []]
        combined_save = combined
        if sum == 17:
            flip = False
            for line in [5, 7, 5]:
                if keep_going:
                    for num in syl:
                        if line < 0:
                            keep_going = False
                            break
                        if flip:
                            temp = num
                            break
                        if line > 0:
                            if flip:
                                line -= temp
                                line -= num
                                flip = False
                            if line - num == 0:
                                flip = True
                            else:
                                line -= num
            combined = []
            if keep_going:
                a = 5
                b = 7
                c = 5
                while a:
                    haiku[0].append(combined[0][1])
                    a -= combined[0][0]
                    combined.pop(0)
                while b:
                    haiku[1].append(combined[0][1])
                    b -= combined[0][0]
                    combined.pop(0)
                while c:
                    haiku[2].append(combined[0][1])
                    c -= combined[0][0]
                    combined.pop(0)
        embed = discord.Embed(title=f"Haiku Debug from {ctx.message.author}", color=discord.Color.from_rgb(153, 50, 204))
        embed.add_field(name='**Message:**', value=f'```{" ".join(msg_list)}```')
        embed.add_field(name='Syllables:', value=sum)
        embed.add_field(name='\u200b', value='\u200b')
        embed.add_field(name='\u200b', value='\u200b')
        breakdown = ""
        try:
            for pair in combined_save:
                breakdown += f'{pair[1]}: {pair[0]}\n'
        except IndexError as exception:
            embed = discord.Embed(title=f"Haiku Debug - Error: TypeError", color=discord.Color.from_rgb(255, 0, 0))
            embed.add_field(name='**Message:**', value=f'```{" ".join(msg_list)}```')
            embed.add_field(name='**Error whilst parsing message**', value=f'```{exception}```')
            try:
                await ctx.author.send(embed=embed)
                await ctx.message.add_reaction(check_reaction)
            except discord.Forbidden:
                await ctx.send(embed=embed)
        embed.add_field(name='Word Breakdown:', value=f"```{breakdown}```")
        embed.add_field(name='\u200b', value='\u200b')
        embed.add_field(name='\u200b', value='\u200b')
        if keep_going and sum == 17:
            embed.add_field(name='Haiku:', value="Valid Haiku!")
        else:
            embed.add_field(name='Haiku:', value="Invalid Haiku")
        try:
            await ctx.author.send(embed=embed)
            await ctx.message.add_reaction(check_reaction)
        except discord.Forbidden:
            await ctx.send(embed=embed)
    except TypeError as exception:
        breakdown = ""
        try:
            for pair in combined_save:
                breakdown += f'{pair[1]}: {pair[0]}\n'
            error = f"\n{exception}\n\n" \
                    f"Extra info:\n" \
                    f"Syllables: {sum}\n" \
                    f"Word Breakdown: {breakdown}"
        except:
            error = f"\n{exception}\n\n" \
                    f"Extra info:\n" \
                    f"Syllables: {sum}\n" \
                    f"Syllable parser error at: {syl_error}"
        embed = discord.Embed(title=f"Haiku Debug - Error: TypeError", color=discord.Color.from_rgb(255, 0, 0))
        embed.add_field(name='**Message:**', value=f'```{" ".join(msg_list)}```')
        embed.add_field(name='**Error whilst parsing message**', value=f'```{exception}{error}```')
        try:
            await ctx.author.send(embed=embed)
            await ctx.message.add_reaction(check_reaction)
        except discord.Forbidden:
            await ctx.send(embed=embed)


# Events


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('Listening for poetry skills | prefix: >'), status="dnd")
    print('Bot Initialized')


@bot.listen()
async def on_message(message):
    try:
        if " " in message.content.strip():
            msg_list = message.content.strip().split(" ")
            syl = []
            sum = 0
            i = 0
            combined = [[] for _ in range(len(msg_list))]
            for word in msg_list:
                syl.append(get_syllable_count(word))
                combined[i].append(get_syllable_count(word))
                combined[i].append(word)
                sum += combined[i][0]
                i += 1
            keep_going = True
            haiku = [[], [], []]
            if sum == 17:
                flip = False
                for line in [5, 7, 5]:
                    if keep_going:
                        for num in syl:
                            if line < 0:
                                keep_going = False
                                break
                            if flip:
                                temp = num
                                break
                            if line > 0:
                                if flip:
                                    line -= temp
                                    line -= num
                                    flip = False
                                if line - num == 0:
                                    flip = True
                                else:
                                    line -= num
                if keep_going:
                    a = 5
                    b = 7
                    c = 5
                    while a:
                        haiku[0].append(combined[0][1])
                        a -= combined[0][0]
                        combined.pop(0)
                    while b:
                        haiku[1].append(combined[0][1])
                        b -= combined[0][0]
                        combined.pop(0)
                    while c:
                        haiku[2].append(combined[0][1])
                        c -= combined[0][0]
                        combined.pop(0)
                    embed = discord.Embed(title=f"Haiku by {message.author}", color=discord.Color.from_rgb(34, 139, 34),
                                          timestamp=datetime.datetime.utcnow())
                    embed.add_field(name='\u200b', value=" ".join(haiku[0]))
                    embed.add_field(name='\u200b', value='\u200b')
                    embed.add_field(name='\u200b', value='\u200b')
                    embed.add_field(name='\u200b', value=" ".join(haiku[1]))
                    embed.add_field(name='\u200b', value='\u200b')
                    embed.add_field(name='\u200b', value='\u200b')
                    embed.add_field(name='\u200b', value=" ".join(haiku[2]))
                    await message.channel.send(embed=embed)
    except TypeError:
        return

bot.run(token)
