import discord
from discord.ext import commands
from discord.ext import tasks
from dotenv import load_dotenv

import random
import os
import os.path
import csv
import gen

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = commands.Bot(command_prefix="$")

phraseList = []
authorList = []


@bot.event
async def on_ready():
    print(f"{bot} is online.")


def generateLists():
    with open("phrases.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            phraseList.insert(len(phraseList), row[0])
            authorList.insert(len(authorList), row[1])


@bot.command()
async def wacky(ctx):
    generateLists()
    csvNum = random.randint(0, len(phraseList) - 2)
    await ctx.channel.send(f"{phraseList[csvNum]} -{authorList[csvNum]}")


def writeToCsv(quote, author):
    with open("phrases.csv", "a", newline="") as csvfile:
        write = csv.writer(csvfile)
        csvfile.write("\n")
        write.writerow([quote, f" {author}"])


@commands.has_permissions(administrator=True)
@bot.command()
async def quote(ctx, quote, author):
    charArr = list(quote)
    if charArr[0] != '"':
        quote = f'"{quote}"'
    with open("phrases.csv", "a", newline="") as csvfile:
        write = csv.writer(csvfile)
        read = csv.writer(csvfile)
        csvfile.write("\n")
        csvfile.write(f'""{quote}"", {author}')
    generateLists()
    await ctx.channel.send(f"Quote from {author} has been recorded.")


@commands.has_permissions(administrator=True)
@bot.command(pass_context=True)
async def listAll(ctx):
    generateTxt()
    lines = []
    with open(
        "quotes.txt", "r", encoding="utf-8"
    ) as file:  # Use this to open and close the file
        for line in file.readlines():
            line = line.strip()
            lines.append(line)
            index1 = 1
            index1 += 1
            if index1 == (len(lines) + 1):
                break

    await ctx.send(file=discord.File("quotes.txt"))


def generateTxt():
    generateLists()
    with open("quotes.txt", "w", encoding="utf-8") as f:
        for j in range(0, len(authorList)):
            f.write(f"{phraseList[j]}, {authorList[j]}\n")


@bot.command()
async def listPerson(ctx, person):
    generateLists()
    dictionary = dict(zip(phraseList, authorList))
    embed = discord.Embed()
    for quote, author in dictionary.items():
        if author.lower() == f" {person.lower()}":
            embed.add_field(
                name=f"{author.Capitalize()}", value=f"{quote}", inline=False
            )
    await ctx.channel.send(embed=embed)


@bot.command()
async def last(ctx):
    generateLists()
    await ctx.channel.send(
        f"{phraseList[len(phraseList) - 1]} -{authorList[len(authorList) - 1]}"
    )


@bot.command()
async def random(ctx):
    await ctx.channel.send(gen.generateSentence())


generateLists()
bot.run(TOKEN)
