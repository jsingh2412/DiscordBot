# bot.py
# Jagroop Singh
# WIP
import os
from re import I
from dotenv import load_dotenv, find_dotenv
import hikari
import lightbulb

load_dotenv(find_dotenv())
#bot = hikari.GatewayBot(token = os.getenv('TOKEN'), default_enabled_guilds=(os.getenv('DEFAULT_GUILD_ID')))
bot = lightbulb.BotApp(token = os.getenv('TOKEN'), default_enabled_guilds=os.getenv('DEFAULT_GUILD_ID'))

inputed_roles = {}
#test_roles = {'NA': ':red_circle:', 'EU' : ':orange_circle:', 'SA' : ':yellow_circle:', 'AS' : ':green_circle:', 'AF' : ':blue_circle:', 'OCE' : ':purple_circle:'}
#bot.rest.add_reaction

#bot launch
@bot.listen(hikari.StartedEvent)
async def on_started(event):
    print('Bot has started!')

#message that is outputted once all inputs have been given
async def rolesmessage():
    rolemessage = ''
    for i in inputed_roles:
        rolemessage += inputed_roles[i] + ' ' +  i + '\n'
    #hard coded until channel set command is finished
    await bot.rest.create_message(
        channel=(991944891695386654), 
        content = rolemessage
    )
        

#rr = reaction role
#will create message that will be used for reactions
@bot.listen(hikari.GuildMessageCreateEvent)
async def createrrmessage(event):
    if event.is_bot or not event.content or event.channel_id!=(991944891695386654):
        return

    if event.content.startswith('!send'):
        await rolesmessage()
        for i in inputed_roles:
            print(i + inputed_roles[i])
            

#roles initiation 
@bot.listen(hikari.GuildMessageCreateEvent)
async def roles(event):
    if event.is_bot or not event.content or event.channel_id!=(991944891695386654):
        return

    if event.content.startswith('!roles'):
        await event.message.respond('Send all roles you would like to be added. Add in the format of !addingroles emoji, @role per message, after you are done type !send #channel. To restart the addition of roles type !resetroles and begin again.')



@bot.listen(hikari.GuildMessageCreateEvent)
async def roles(event):
    if event.is_bot or not event.content or event.channel_id!=(991944891695386654):
        return

    if event.content.startswith('!addingroles'):
        temproleid = event.message.role_mention_ids
        tempcontent = event.content.replace('!addingroles ', '')
        inputed_roles.setdefault(tempcontent, temproleid)
        print(tempcontent + str(temproleid))
  

#@bot.listen(hikari.GuildReactionAddEvent)
#async def reactionroles(event):
#    print(event.emoji_name)
    

# ALL CODE ABOVE THIS IS NOT BEING ACTIVELY USED


listofroles = []
#holds id of message that is created by bot
message_id = ''
#holds channel ID for bot to communicate in
setChannel = ''
roleMessageHolder = ''
@bot.command
@lightbulb.command('reactionroles','test groups')
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def reactionroles(ctx: lightbulb.Context):
    await ctx.respond('Pong!')

@reactionroles.child
@bot.command
#@lightbulb.option('message_id', 'The message ID of the message to add reaction role to!', 
    #type=str, required= True)
@lightbulb.option('emoji', 'The emoji you would like to assign to this role', 
    type=str, required= True)
@lightbulb.option('role', 'The role you would like to assign', 
    type=hikari.Role, required= True)
@lightbulb.command('add','test groups')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def add(ctx: lightbulb.Context):
    listofroles.append({
        #1 : ctx.options.message_id, 
    2 : ctx.options.emoji, 3 : ctx.options.role})
    
    await ctx.respond('The role has been added!')

@reactionroles.child
@bot.command
@lightbulb.command('clear',"Removes all roles already queue'd")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def clear(ctx: lightbulb.Context):
    listofroles.clear()
    await ctx.respond('List of roles has been cleared')


    #@bot.listen(hikari.ReactionAddEvent)
    #async def addarole(event):
    #    if event.channel_id!=(993726578997600396):
    #        return
    #    if event.message_id==(993727929840316447):
    #        print('working!')

# Uses the queued up roles to create a new message that lists 
# the roles along with the emoji assoicated with them. 
# The id for the message created is then captured by getMessageID
@reactionroles.child
@bot.command
@lightbulb.command('createmessage',"Creates and sends a message using the queued roles.")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def createmessage(ctx: lightbulb.Context):
    try:
        rolemessage = ''
        #role = 3
        #emoji = 2
        #message_id = 1
        
        for i, value in enumerate(listofroles):
            tempdict=listofroles[i]
            print (tempdict)
            rolemessage += str(tempdict[3]) + ' ' +  tempdict[2] + '\n'
        
        await bot.rest.create_message(
            channel=(993726578997600396), 
            content = rolemessage
        )

        await ctx.respond('The message has been sent!')
    except:
        await ctx.respond(
            'Some error occured. Make sure you have added at least one role before using this command!'
        )
        
@bot.listen(hikari.ReactionAddEvent)
async def checkRoleSelection(message_id, event, ctx: lightbulb.Context):
    try:
        if(message_id == event.message_id):
            ctx.respond('caught reaction')
    except:
        await ctx.respond(
            'No reaction was found, try again.'
        )
        
@bot.listen(hikari.GuildMessageCreateEvent)
async def getMessageID(event):
    if event.is_bot & event.message==rolesmessage:
        message_id = event.message_id
    else:
        return
        
bot.run()

