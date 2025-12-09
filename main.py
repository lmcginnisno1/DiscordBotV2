import os
from dotenv import load_dotenv
import gspread
import utils

load_dotenv("./constants.env")
load_dotenv("./keys.env")

TBA_Auth_Key = os.getenv("TBA_AUTH_KEY")
gc = gspread.service_account("credentials.json")
sheet = gc.open(os.getenv("SPREADSHEET_NAME")).sheet1
sheet.resize(76, 29)

async def update_sheet(event_key):
    numbers = []
    names = []
    states_provinces = []
    rookie_years = []
    district_points = []
    events_played = []
    wtl = []
    winrates = []
    total_epa = []
    auto_epa = []
    tele_epa = []
    endgame_epa = []
    auto_moverate = []
    matches_played = []
    climbs = []
    climb_percents = []
    parks = []

    for team in utils.call_tba_api(f"event/{event_key}/teams", f"{event_key}"):
        numbers.append([team["team_number"]])

        names.append([team["nickname"]])

        states_provinces.append([team["state_prov"]])

        rookie_years.append([team["rookie_year"]])

        team_district_points = utils.call_statbotics_api(team["team_number"], team["team_number"])["district_points"]
        if team_district_points is None:
            district_points.append(["N/A"])
        else:
            district_points.append([team_district_points])

        events_played.append([utils.events_played(team["team_number"])])

        team_stats = utils.call_statbotics_api(team["team_number"], team["team_number"])

        wtl.append([f"{team_stats["record"]["wins"]}-{team_stats["record"]["ties"]}-{team_stats["record"]["losses"]}"])

        winrates.append([str(round(team_stats["record"]["winrate"]*100, 1))+"%"])

        total_epa.append([team_stats["epa"]["breakdown"]["total_points"]])

        auto_epa.append([team_stats["epa"]["breakdown"]["auto_points"]])

        tele_epa.append([team_stats["epa"]["breakdown"]["teleop_points"]])

        endgame_epa.append([team_stats["epa"]["breakdown"]["endgame_points"]])

        auto_moverate.append([utils.auto_move_percentage(team["team_number"])])

        matches_played.append([utils.matches_played(team["team_number"])])

        climbs.append([utils.climbs(team["team_number"])])

        climb_percents.append([utils.climb_percentage(team["team_number"])])

        parks.append([utils.parks(team["team_number"])])

        sheet.batch_update([
        {
            "range": f"{os.getenv("NUM")}2:{os.getenv("NUM")}{len(numbers) + 1}",
            "values": numbers
        },
        {
            "range": f"{os.getenv("NAME")}2:{os.getenv("NAME")}{len(names) + 1}",
            "values": names
        },
        {
            "range": f"{os.getenv("STATE_PROV")}2:{os.getenv("STATE_PROV")}{len(states_provinces) + 1}",
            "values": states_provinces
        },
        {
            "range": f"{os.getenv("ROOKIE_YEAR")}2:{os.getenv("ROOKIE_YEAR")}{len(rookie_years) + 1}",
            "values": rookie_years
        },
        {
            "range": f"{os.getenv("DISTRICT_POINTS")}2:{os.getenv("DISTRICT_POINTS")}{len(district_points) + 1}",
            "values": district_points
        },
        {
            "range": f"{os.getenv("EVENTS_PLAYED")}2:{os.getenv("EVENTS_PLAYED")}{len(events_played) + 1}",
            "values": events_played
        },
        {
            "range": f"{os.getenv("WTL")}2:{os.getenv("WTL")}{len(wtl) + 1}",
            "values": wtl
        },
        {
            "range": f"{os.getenv("WINRATE")}2:{os.getenv("WINRATE")}{len(winrates) + 1}",
            "values": winrates
        },
        {
            "range": f"{os.getenv("TOTAL_EPA")}2:{os.getenv("TOTAL_EPA")}{len(total_epa) + 1}",
            "values": total_epa
        },
        {
            "range": f"{os.getenv("AUTO_EPA")}2:{os.getenv("AUTO_EPA")}{len(auto_epa) + 1}",
            "values": auto_epa
        },
        {
            "range": f"{os.getenv("TELE_EPA")}2:{os.getenv("TELE_EPA")}{len(tele_epa) + 1}",
            "values": tele_epa
        },
        {
            "range": f"{os.getenv("ENDGAME_EPA")}2:{os.getenv("ENDGAME_EPA")}{len(endgame_epa) + 1}",
            "values": endgame_epa
        },
        {
            "range": f"{os.getenv("AUTO_MOVE_PERCENT")}2:{os.getenv("AUTO_MOVE_PERCENT")}{len(auto_moverate) + 1}",
            "values": auto_moverate
        },
        {
            "range": f"{os.getenv("MATCHES_PLAYED")}2:{os.getenv("MATCHES_PLAYED")}{len(matches_played) + 1}",
            "values": matches_played
        },
        {
            "range": f"{os.getenv("CLIMBS")}2:{os.getenv("CLIMBS")}{len(climbs) + 1}",
            "values": climbs
        },
        {
            "range": f"{os.getenv("CLIMB_PERCENT")}2:{os.getenv("CLIMB_PERCENT")}{len(climb_percents) + 1}",
            "values": climb_percents
        },
        {
            "range": f"{os.getenv("PARKS")}2:{os.getenv("PARKS")}{len(parks) + 1}",
            "values": parks
        },
    ])