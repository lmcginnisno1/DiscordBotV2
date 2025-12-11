import json
import os
import shutil

import statbotics
from datetime import datetime
import requests

stats = statbotics.Statbotics()


def call_tba_api(url, filename):
    if os.path.exists(f"./json-files/tba/{filename}.json"):
        return json.load(open(f"./json-files/tba/{filename}.json"))
    else:
        r = requests.get(f"https://www.thebluealliance.com/api/v3/{url}", headers={"X-TBA-Auth-Key": os.getenv("TBA_AUTH_KEY")})
        os.makedirs(f"./json-files/tba", exist_ok=True)
        with open(f"./json-files/tba/{filename}.json", "w") as json_file:
            json.dump(r.json(), json_file)
        return r.json()

def call_statbotics_api(team, filename):
    if os.path.exists(f"./json-files/statbotics/{filename}.json"):
        return json.load(open(f"./json-files/statbotics/{filename}.json"))
    else:
        r = stats.get_team_year(team, datetime.now().year)
        os.makedirs(f"./json-files/statbotics", exist_ok=True)
        with open(f"./json-files/statbotics/{filename}.json", "w") as json_file:
            json.dump(r, json_file)
        return r

def get_name(team):
    try:
        name = call_tba_api(f"team/frc{team}" ,team).get("nickname")
    except Exception:
        return "N/A"
    return name

def events_played(team_num):
    try:
        events = call_tba_api(f"team/frc{team_num}/events/{datetime.now().year}", f"{team_num}_events")
    except Exception:
        return "N/A"
    if "Error" in events:
        return "N/A"

    num_events = len(events)

    if num_events == 0:
        return "N/A"

    return num_events

def get_state_province(team):
    try:
        state_prov = call_tba_api(f"team/frc{team}", team).get("state_prov")
    except Exception:
        return "N/A"
    return state_prov

def get_rookie_year(team):
    try:
        rookie_year = call_tba_api(f"team/frc{team}", team).get("rookie_year")
    except Exception:
        return "N/A"
    return rookie_year

def get_district_points(team):
    try:
        district_points = call_statbotics_api(team, team).get("district_points")
    except Exception:
        return "N/A"
    if district_points is None:
        return "N/A"
    return district_points

def get_wtl(team):
    try:
        w = call_statbotics_api(team, team).get("record").get("wins")
        t = call_statbotics_api(team, team).get("record").get("ties")
        l = call_statbotics_api(team, team).get("record").get("losses")
        wtl = f"{w}-{t}-{l}"
    except Exception:
        return "N/A"
    return wtl

def get_winrate(team):
    try:
        winrate = call_statbotics_api(team, team).get("record").get("winrate")
    except Exception:
        return "N/A"
    return round(winrate * 100, 2)

def get_epa(team, epa_type):
    try:
        epa = call_statbotics_api(team, team).get("epa").get("breakdown").get(epa_type + "_points")
    except Exception:
        return "N/A"
    return epa

def auto_move_percentage(team_num):
    moves = 0
    total_matches = 0

    try:
        events = call_tba_api(f"team/frc{team_num}/events/{datetime.now().year}", f"{team_num}_events")
    except Exception:
        return "N/A"
    if "Error" in events:
        return "N/A"

    for event in events:
        event_key = event["key"]

        try:
            matches = call_tba_api(f"event/{event_key}/matches", f"{team_num}_matches")
        except Exception:
            return "N/A"
        for match in matches:
            alliances = match["alliances"]
            score_breakdown = match.get("score_breakdown", {})

            if score_breakdown is None: continue

            for color in ["blue", "red"]:
                if f"frc{team_num}" in alliances[color]["team_keys"]:
                    team_slot = alliances[color]["team_keys"].index(f"frc{team_num}") + 1
                    move_status = score_breakdown.get(color, {}).get(f"autoLineRobot{team_slot}", "")

                    if move_status == "Yes":
                        moves += 1
                    total_matches += 1
                    break

    if total_matches == 0:
        return "N/A"

    percentage = round((moves / total_matches) * 100, 1)
    return percentage

def matches_played(team):
    try:
        matches = call_statbotics_api(team, team).get("record").get("count")
    except Exception:
        return "N/A"

    return matches

def climbs(team_num):
    num_climbs = 0

    try:
        events = call_tba_api(f"team/frc{team_num}/events/{datetime.now().year}", f"{team_num}_events")
    except Exception:
        return "N/A"

    if "Error" in events:
        return "N/A"

    for event in events:
        event_key = event["key"]

        try:
            matches = call_tba_api(f"event/{event_key}/matches", f"{team_num}_matches")
        except Exception:
            return "N/A"
        for match in matches:
            alliances = match["alliances"]
            score_breakdown = match.get("score_breakdown", {})

            if score_breakdown is None: continue


            for color in ["blue", "red"]:
                if f"frc{team_num}" in alliances[color]["team_keys"]:
                    team_slot = alliances[color]["team_keys"].index(f"frc{team_num}") + 1
                    climb_status = score_breakdown.get(color, {}).get(f"endGameRobot{team_slot}", "")

                    if climb_status in {"DeepCage", "ShallowCage"}:
                        num_climbs += 1
                    break

    return num_climbs

def climb_percentage(team_num):
    climbs = 0
    total_matches = 0

    events = call_tba_api(f"team/frc{team_num}/events/{datetime.now().year}", f"{team_num}_events")
    if "Error" in events:
        return "N/A"

    for event in events:
        event_key = event["key"]

        try:
            matches = call_tba_api(f"event/{event_key}/matches", f"{team_num}_matches")
        except Exception:
            return "N/A"
        for match in matches:
            alliances = match["alliances"]
            score_breakdown = match.get("score_breakdown", {})

            if score_breakdown is None: continue

            for color in ["blue", "red"]:
                if f"frc{team_num}" in alliances[color]["team_keys"]:
                    team_slot = alliances[color]["team_keys"].index(f"frc{team_num}") + 1
                    climb_status = score_breakdown.get(color, {}).get(f"endGameRobot{team_slot}", "")

                    if climb_status in {"DeepCage", "ShallowCage"}:
                        climbs += 1
                    total_matches += 1
                    break

    if total_matches == 0:
        return "N/A"

    percentage = round((climbs / total_matches) * 100, 1)
    return percentage

def parks(team_num):
    parks = 0

    try:
        events = call_tba_api(f"team/frc{team_num}/events/{datetime.now().year}", f"{team_num}_events")
    except Exception:
        return "N/A"
    if "Error" in events:
        return "0 matches"

    for event in events:
        event_key = event["key"]

        try:
            matches = call_tba_api(f"event/{event_key}/matches", f"{team_num}_matches")
        except Exception:
            return "N/A"
        for match in matches:
            alliances = match["alliances"]
            score_breakdown = match.get("score_breakdown", {})

            if score_breakdown is None: continue


            for color in ["blue", "red"]:
                if f"frc{team_num}" in alliances[color]["team_keys"]:
                    team_slot = alliances[color]["team_keys"].index(f"frc{team_num}") + 1
                    climb_status = score_breakdown.get(color, {}).get(f"endGameRobot{team_slot}", "")

                    if climb_status == "Parked":
                        parks += 1
                    break

    return parks

def clear_cache():
    if os.path.exists("./json-files/tba"):
        shutil.rmtree("./json-files/tba")

    if os.path.exists("./json-files/statbotics"):
        shutil.rmtree("./json-files/statbotics")