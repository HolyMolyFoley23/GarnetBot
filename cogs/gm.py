import discord
from discord.ext import commands
import garnet_helper

class GM(commands.Cog):

    def _init_(self, bot):
        self.bot = bot
    
    async def is_gm(ctx):
        return any("GM" in role.name for role in ctx.author.roles)
    
    @commands.command(name='init', brief='Start a new game', help="Example: !init")
    @commands.check(is_gm)
    async def init(self, ctx): 
        garnet_helper.init_game(ctx.guild)
    
    
    @commands.command(name='set', brief='Set players garnets', help="Example: !set Jack 2")
    @commands.check(is_gm)
    async def set_garnets(self, ctx, name, num_garnets: int): 
        if garnet_helper.set_player_garnets(name,num_garnets):
            await ctx.send(f'{name} has {num_garnets} garnet(s)')
        else:
            await ctx.send(f'{name} does not exist')
    
    @commands.command(name='get', brief = r"Get a player's garnets", help="Example: !get David Jack")
    @commands.check(is_gm)
    async def get_garnets(self, ctx, *args):
        for player in args:
            curr_garnets = garnet_helper.get_garnets(player)
            if curr_garnets:
                await ctx.send(f'{player} has {curr_garnets} garnets')
            else:
                await ctx.send(f'{player} is not a player')
    
    @commands.command(name='get_all', brief = 'Get all players garnets', help = "Example: !get_all")
    @commands.check(is_gm)
    async def get_all(self, ctx, *flags):
        list_players= list(garnet_helper.get_all_garnets())
        list_players.sort(key=lambda x:x[1],reverse=True)
        people=["Players Garnets"]
        for player,amount in list_players:
            people.append(f'{player} : {amount}')
        await ctx.send('\n'.join(people))

    @commands.command(name='add_player', brief = 'Add another player', help = "Example: !add_player David")
    @commands.check(is_gm)
    async def add_player(self, ctx, name):
        garnet_helper.add_player(name)
        await ctx.send(f'{name} has been added')
        
    @commands.command(name='kill', brief = 'Kill the loser of a deathmatch and transfer their garnets', help = "Example: !kill David Jack")
    @commands.check(is_gm)
    async def kill(self, ctx, winner, loser):
        if not garnet_helper.valid_player(winner):
            await ctx.send(f'{winner} is not a player')
            return
        if not garnet_helper.valid_player(loser):
            await ctx.send(f'{loser} is not a player')
            return
        loser_garnets = garnet_helper.get_garnets(loser)
        garnet_helper.change_player_garnets(winner, loser_garnets)
        garnet_helper.delete_player(loser)
        await ctx.send(f'{winner} has killed {loser} and taken their garnets')
    
    @commands.command(name='add_garnets', brief = 'Give a player additional garnets', help = "Example: !add_garnets David 5")
    @commands.check(is_gm)
    async def add_garnets(self, ctx, name, num_garnets : int):
        if not garnet_helper.valid_player(name):
            await ctx.send(f'{name} is not a player')
            return
        garnet_helper.change_player_garnets(name, num_garnets)
        await ctx.send(f'{name} has been given {num_garnets} garnet(s)')


def setup(bot):
    bot.add_cog(GM(bot))