import discord


async def defer_with_message(ctx, message, ephemeral: bool = False) -> discord.Message:
    return await ctx.respond(content=message, ephemeral=ephemeral)