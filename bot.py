from re import I
import hikari
import lightbulb

#bot = hikari.GatewayBot(token = 'OTkxNTU0OTgxNDk0ODAwMzg2.GgYmXV.O6kxgD83El-Ek__yCiGaUeVd7ccoD9HXUPLaEI')
bot = lightbulb.BotApp(token = 'OTkxNTU0OTgxNDk0ODAwMzg2.GgYmXV.O6kxgD83El-Ek__yCiGaUeVd7ccoD9HXUPLaEI', default_enabled_guilds=(991435839680827416,991820924590510162))

inputed_roles = {}
#test_roles = {'NA': ':red_circle:', 'EU' : ':orange_circle:', 'SA' : ':yellow_circle:', 'AS' : ':green_circle:', 'AF' : ':blue_circle:', 'OCE' : ':purple_circle:'}
#bot.rest.add_reaction

@bot.listen(hikari.StartedEvent)
async def on_started(event):
    print('Bot has started!')


async def rolesmessage():
    
    rolemessage = ''
    for i in inputed_roles:
        rolemessage += inputed_roles[i] + ' ' +  i + '\n'
    
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
    


listofroles = []

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

@bot.listen(hikari.ReactionAddEvent)
async def addarole(event):
    if event.channel_id!=(993726578997600396):
        return
    if event.message_id==(993727929840316447):
        print('yo it worked nice!')

@reactionroles.child
@bot.command
@lightbulb.command('createmessage',"Removes all roles already queue'd")
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
bot.run()

