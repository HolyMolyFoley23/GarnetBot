import discord
from discord.ext import commands
import garnet_helper

class Player(commands.Cog):

    def _init_(self, bot):
        self.bot = bot
    
    def get_name(self,ctx):
        return ctx.message.author.display_name.split()[0]
    
    @commands.command(name='give', brief = 'Give another player garnets', help = "Example: !give David 2")
    async def give(self, ctx, recipient: str, num_garnets: int):
        parsed_author = self.get_name(ctx)
        if num_garnets < 0:# or parsed_author == recipient:
            await ctx.send("Please don't try to break the bot")
            return
        if not garnet_helper.valid_player(parsed_author):
            await ctx.send(f'{parsed_author} is not a player')
            return
        if not garnet_helper.valid_player(recipient):
            await ctx.send(f'{recipient} is not a player')
            return
        if num_garnets > garnet_helper.get_garnets(parsed_author):
            await ctx.send(f'Not enough garnets')
            return
        garnet_helper.add_payment_info(parsed_author,recipient,str(ctx.message.channel.id),num_garnets)
        await ctx.send(f'{parsed_author} has offered {num_garnets} garnets to {recipient}')
        
        
    @commands.command(name='revoke', brief = 'Revoke an offer you made to a player', help = "Example: !revoke David")
    async def revoke(self, ctx, recipient: str):
        parsed_author = self.get_name(ctx)
        parsed_id = str(ctx.message.channel.id)
        if not garnet_helper.valid_player(parsed_author):
            await ctx.send(f'{parsed_author} is not a player')
            return
        if not garnet_helper.valid_player(recipient):
            await ctx.send(f'{recipient} is not a player')
            return
        if garnet_helper.remove_payment_info(parsed_author,recipient,parsed_id):
            await ctx.send(f'Offer to {recipient} has been revoked')
        else:
            await ctx.send(f'No offer found between {parsed_author} and {recipient} in {ctx.message.channel.name}')

    @commands.command(name='accept', brief = 'Accept another player garnets', help = "Example: !accept David")
    async def accept(self, ctx, giver: str):
        recipient = self.get_name(ctx)
        parsed_id=str(ctx.message.channel.id)
        if not garnet_helper.valid_player(recipient):
            await ctx.send(f'{recipient} is not a player')
            return
        if not garnet_helper.valid_player(giver):
            await ctx.send(f'{giver} is not a player')
            return
        offered_garnets = garnet_helper.remove_payment_info(giver, recipient, parsed_id)
        if (offered_garnets >= 0):
            num_garnets = garnet_helper.get_garnets(giver)
            if num_garnets < offered_garnets:
                await ctx.send(f'Not enough garnets')
                return
            garnet_helper.change_player_garnets(recipient, offered_garnets)
            garnet_helper.change_player_garnets(giver, -offered_garnets)
            await ctx.send(f'{giver} has given {recipient} {offered_garnets} garnets')
        else:
            await ctx.send(f'No offer found between {giver} and {recipient} in {ctx.message.channel.name}')

    @commands.command(name='decline', brief = 'Decline an offer made to you', help = "Example: !decline David")
    async def decline(self, ctx, giver: str):
        recipient = self.get_name(ctx)
        parsed_id = str(ctx.message.channel.id)
        offer = garnet_helper.remove_payment_info(giver, recipient, parsed_id)
        if offer >= -1:
            await ctx.send(f'Offer to {recipient} has been declined')
        else:
            await ctx.send(f'No offer found between {giver} and {recipient} in {ctx.message.channel.name}')

    @commands.command(name='show', brief = 'Shows you your garnet count', help ="Example: !show")
    async def show(self, ctx):
        parsed_author = self.get_name(ctx)
        if garnet_helper.valid_player(parsed_author):
            await ctx.send(f'You have {garnet_helper.get_garnets(parsed_author)} garnet(s)')
        else:
            await ctx.send('You are not a player')
    
    @commands.command(name='buy', brief = 'Buy help during a game with garnets', help = "Example: !buy 3")
    async def buy(self, ctx, num_garnets: int):
        parsed_author = self.get_name(ctx)
        if not garnet_helper.valid_player(parsed_author):
            await ctx.send('You are not a player')
            return
        if num_garnets < 0:
            await ctx.send("Please don't try to break the bot")
        if num_garnets > garnet_helper.get_garnets(player):
            await ctx.send(f'Not enough garnets')
            return
        garnet_helper.change_player_garnets(parsed_author, -num_garnets)
        await ctx.send(f'You have spent {num_garnets} garnets on bonuses.')
    

def setup(bot):
    bot.add_cog(Player(bot))
