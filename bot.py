import os
import discord
import main
import utils

from discord import Option

bot = discord.Bot()


@bot.command(name="update_sheet", description="updates all information on the spreadsheet")
async def update_sheet(ctx, event_key: str):
    await ctx.defer()
    await main.update_sheet(event_key)
    await ctx.respond("Sheet updated")

@bot.command(name="get_name", description="returns the name of the specified team")
async def get_name(ctx, team):
    await ctx.defer()
    await ctx.respond(f"team {team}'s name is {utils.get_name(int(team))}")

@bot.command(name="get_state_prov", description="returns the state/province of the specified team")
async def get_state_prov(ctx, team):
    await ctx.defer()
    await ctx.respond(f"{team}'s home state/province is {utils.get_state_province(int(team))}")

@bot.command(name="get_rookie_year", description="returns the rookie year of the specified team")
async def get_rookie_year(ctx, team):
    await ctx.defer()
    await ctx.respond(f"team {team}'s rookie year is {utils.get_rookie_year(int(team))}")

@bot.command(name="get_district_points", description="returns the district points of the specified team")
async def get_district_points(ctx, team):
    await ctx.defer()
    if utils.get_district_points(team) == "N/A":
        await ctx.respond(f"team {team} is not part of any district")
    else:
        await ctx.respond(f"team {team} has eared {utils.get_district_points(int(team))} district points")

@bot.command(name="get_events_played", description="returns the number events played for the specified team")
async def get_events_played(ctx, team):
    await ctx.defer()
    await ctx.respond(f"team {team} has played at {utils.events_played(int(team))} events")

@bot.command(name="get_wtl", description="returns the WTL of the specified team")
async def get_wtl(ctx, team):
    await ctx.defer()
    await ctx.respond(f"team {team}'s wtl is {utils.get_wtl(int(team))}")

@bot.command(name="get_winrate", description="returns the winrate of the specified team")
async def get_winrate(ctx, team):
    await ctx.defer()
    await ctx.respond(f"team {team}'s winrate is {utils.get_winrate(int(team))}%")

@bot.command(name="get_epa", description="returns the epa of the specified type for the specified team")
async def get_epa(ctx, team, epa_type:  str = Option(str, "epa type", choices=["total", "auto", "teleop", "endgame"])):
    await ctx.defer()
    await ctx.respond(f"team {team}'s {epa_type} epa is {utils.get_epa(int(team), epa_type)}")

@bot.command(name="get_auto_moverate", description="returns the auto moverate of the specified team")
async def get_auto_moverate(ctx, team):
    await ctx.defer()
    await ctx.respond(f"team {team} moves in auto {utils.auto_move_percentage(int(team))}% of the time")

@bot.command(name="summary", description="provides all stats on the specified team")
async def summary(ctx, team: int):
    await ctx.defer()

    name = utils.get_name(team)
    state = utils.get_state_province(team)
    rookie_year = utils.get_rookie_year(team)
    district_points = utils.get_district_points(team)
    events_played = utils.events_played(team)
    wtl = utils.get_wtl(team)
    winrate = utils.get_winrate(team)
    epa_total = utils.get_epa(team, "total")
    epa_auto = utils.get_epa(team, "auto")
    epa_teleop = utils.get_epa(team, "teleop")
    epa_endgame = utils.get_epa(team, "endgame")
    auto_move = utils.auto_move_percentage(team)

    # Handle district points gracefully
    district_info = (
        f"{district_points}"
        if district_points != "N/A"
        else "not part of any district"
    )

    summary_text = (
        f"**Team {team} Summary**\n"
        f"- Name: {name}\n"
        f"- State/Province: {state}\n"
        f"- Rookie Year: {rookie_year}\n"
        f"- District Points: {district_info}\n"
        f"- Events Played: {events_played}\n"
        f"- WTL: {wtl}\n"
        f"- Winrate: {winrate}%\n"
        f"- EPA (Total): {epa_total}\n"
        f"- EPA (Auto): {epa_auto}\n"
        f"- EPA (Teleop): {epa_teleop}\n"
        f"- EPA (Endgame): {epa_endgame}\n"
        f"- Auto Move Rate: {auto_move}%"
    )

    await ctx.respond(summary_text)

@bot.command(name="clear_cache", description="deletes all stored event data to refresh team stats with the latest season info")
async def clear_cache(ctx):
    await ctx.defer()
    utils.clear_cache()
    await ctx.respond(f"cached cleared")

bot.run(os.getenv("BOT_KEY"))