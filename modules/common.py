import requests
from math import ceil
import random


#------------------------------------Begin Fonctions principales--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def PickOverFirstHalf(data, picks, all_profit, totalOK, totalKO, total, lostMax, lostMaximum, isProd):
    # ODD1
    retourFT1 = {
        "all_profit": all_profit,
        "totalKO": totalKO,
        "totalOK": totalOK,
        "total": total,
        "lostMax": lostMax,
        "lostMaximum": lostMaximum
    }
    odd, max_minute, type = find_valueFirstHalf(data, isProd)
    if odd != None:
        return getProfitOverFirstHalf(data, odd, max_minute, type, picks, all_profit, totalOK, totalKO, total, lostMax, lostMaximum)
    else:
        return retourFT1

def PickOverSecondHalfTest(data, picks, all_profit, totalOK, totalKO, total, lostMax, lostMaximum, isProd):
    # ODD1
    retourFT1 = {
        "all_profit": all_profit,
        "totalKO": totalKO,
        "totalOK": totalOK,
        "total": total,
        "lostMax": lostMax,
        "lostMaximum": lostMaximum
    }
    odd, max_minute, type = find_valueSecondHalfTest(data, isProd)
    if odd != None:
        return getProfitOverSecondHalf(data, odd, max_minute, type, picks, all_profit, totalOK, totalKO, total, lostMax, lostMaximum)
    else:
        return retourFT1

def PickOverSecondHalf(data, picks, all_profit, totalOK, totalKO, total, lostMax, lostMaximum, isProd):
    # ODD1
    retourFT1 = {
        "all_profit": all_profit,
        "totalKO": totalKO,
        "totalOK": totalOK,
        "total": total,
        "lostMax": lostMax,
        "lostMaximum": lostMaximum
    }
    odd, max_minute, type = find_valueSecondHalf(data, isProd)
    if odd != None:
        return getProfitOverSecondHalf(data, odd, max_minute, type, picks, all_profit, totalOK, totalKO, total, lostMax, lostMaximum)
    else:
        return retourFT1

#------------------------------------End Fonctions principales--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------






#------------------------------------Begin Fonctions de test------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def find_valueSecondHalf(data, isProd):
        progressive_data = data['progressive_data']
        #firstHalfData = extract_progressive_data_at_timer(progressive_data, 46)
        firstHalfData = {}
        for entry in progressive_data:
            #init
            key = list(entry.keys())[0]
            value = entry[key]
            time = float(key)

            #traitement
            if time == 46:
                firstHalfData = value
            if 55 <= time <= 70:
                lastProgressiveData = value
                # Vérifier les tirs au but (on) et les expected goals (xG)
                try:
                    teamA_xG_1st = float(firstHalfData["teamA"]["xG"])
                    teamA_xG_2nd = float(lastProgressiveData["teamA"]["xG"])
                except:
                    teamA_xG_2nd = 0
                try:
                    teamB_xG_1st = float(firstHalfData["teamB"]["xG"])
                    teamB_xG_2nd = float(lastProgressiveData["teamB"]["xG"])
                except:
                    teamB_xG_2nd = 0

                #goals
                try:
                    teamA_goals_1st = int(firstHalfData["teamA"]["goal"])
                    teamB_goals_1st = int(firstHalfData["teamB"]["goal"])
                    teamA_goals_total = int(lastProgressiveData["teamA"]["goal"])
                    teamB_goals_total = int(lastProgressiveData["teamB"]["goal"])
                    teamA_goals_2nd = teamA_goals_total - teamA_goals_1st
                    teamB_goals_2nd = teamB_goals_total - teamB_goals_1st
                except:
                    continue

                #shots on targets
                try:
                    teamA_shots_on_target_1st = int(firstHalfData["teamA"]["shoots"]["on"])
                    teamA_shots_on_target_2nd = int(lastProgressiveData["teamA"]["shoots"]["on"]) - teamA_shots_on_target_1st
                except:
                    teamA_shots_on_target_2nd = 0
                try:
                    teamB_shots_on_target_1st = int(firstHalfData["teamB"]["shoots"]["on"])
                    teamB_shots_on_target_2nd = int(lastProgressiveData["teamB"]["shoots"]["on"]) - teamB_shots_on_target_1st
                except:
                    teamB_shots_on_target_2nd = 0


                #77%%%%% OK Shots on target OK
                if (teamA_shots_on_target_2nd + teamB_shots_on_target_2nd >= 3):
                    if teamA_goals_2nd >= 1 or teamB_goals_2nd >= 1: #and teamA_xG_2nd >= 1.2:
                        return 1.5, time, 'expGoals'
        return None, None, None


def find_valueSecondHalfTest(data, isProd):
    progressive_data = data['progressive_data']
    #firstHalfData = extract_progressive_data_at_timer(progressive_data, 46)
    firstHalfData = {}
    filtered_data_teamA = []
    filtered_data_teamB = []
    for entry in progressive_data:
        #init
        key = list(entry.keys())[0]
        value = entry[key]
        time = float(key)

        lastData = progressive_data[len(progressive_data) - 1]
        lastDataKey = list(lastData.keys())[0]
        lastDataValue = lastData[lastDataKey]
        #traitement
        if time == 46:
            firstHalfData = value

        if 46 <= time <= 69:
            filtered_data_teamA.append(value['teamA'])
            filtered_data_teamB.append(value['teamB'])
        if 70 <= time <= 70:
            lastProgressiveData = value
            # Vérifier les tirs au but (on) et les expected goals (xG)
            try:
                teamA_xG_1st = float(firstHalfData["teamA"]["xG"])
                teamB_xG_1st = float(firstHalfData["teamB"]["xG"])
                teamA_xG_2nd = float("{:.2f}".format(float(lastDataValue["teamA"]["xG"]) - teamA_xG_1st))
                teamB_xG_2nd = float("{:.2f}".format(float(lastDataValue["teamB"]["xG"]) - teamB_xG_1st))
                teamA_xG_total = float("{:.2f}".format(float(lastDataValue["teamA"]["xG"])))
                teamB_xG_total = float("{:.2f}".format(float(lastDataValue["teamB"]["xG"])))

                teamA_xG_2ndAt70 = float("{:.2f}".format(float(lastProgressiveData["teamA"]["xG"]) - teamA_xG_1st))
                teamB_xG_2ndAt70 = float("{:.2f}".format(float(lastProgressiveData["teamB"]["xG"]) - teamB_xG_1st))

                teamA_shots_on_target_1st = int(firstHalfData["teamA"]["shoots"]["on"])
                teamA_shots_on_target_2nd = int(lastDataValue["teamA"]["shoots"]["on"]) - teamA_shots_on_target_1st
                teamB_shots_on_target_1st = int(firstHalfData["teamB"]["shoots"]["on"])
                teamB_shots_on_target_2nd = int(lastDataValue["teamB"]["shoots"]["on"]) - teamB_shots_on_target_1st

                teamA_shots_on_target_at70 = int(lastProgressiveData["teamA"]["shoots"]["on"]) - teamA_shots_on_target_1st
                teamB_shots_on_target_at70 = int(lastProgressiveData["teamB"]["shoots"]["on"]) - teamB_shots_on_target_1st

            except:
                teamA_xG_2nd = 0
                teamB_xG_2nd = 0
                teamA_shots_on_target_2nd = 0
                teamB_shots_on_target_2nd = 0
                teamA_xG_2ndAt70 = 0
                teamB_xG_2ndAt70 = 0
                teamB_shots_on_target_at70 = 0
                teamB_shots_on_target_at70 = 0
            #goals
            try:
                teamA_goals_1st = int(firstHalfData["teamA"]["goal"])
                teamB_goals_1st = int(firstHalfData["teamB"]["goal"])
                teamA_goals_total = int(lastProgressiveData["teamA"]["goal"])
                teamB_goals_total = int(lastProgressiveData["teamB"]["goal"])
                teamA_goals_2nd = teamA_goals_total - teamA_goals_1st
                teamB_goals_2nd = teamB_goals_total - teamB_goals_1st
            except:
                continue


            if (teamA_xG_2nd > 0 and teamA_xG_2ndAt70 > 0):


                projecttionxGTeamA, projected_shots_on_teamA = project_to_94_from_46_to_70(filtered_data_teamA, lastProgressiveData['teamA'], teamA_xG_1st, data['id'])
                projecttionxGTeamB, projected_shots_on_teamB = project_to_94_from_46_to_70(filtered_data_teamB, lastProgressiveData['teamB'], teamB_xG_1st, data['id'])

                projecttionxGTeamA = float("{:.2f}".format((projecttionxGTeamA + 0.1)))
                projecttionxGTeamB = float("{:.2f}".format((projecttionxGTeamB + 0.1)))

                projected_shots_on_teamA = int(projected_shots_on_teamA - teamA_shots_on_target_1st)
                projected_shots_on_teamB = int(projected_shots_on_teamB - teamB_shots_on_target_1st)



                if teamA_shots_on_target_2nd + teamB_shots_on_target_2nd >= 6:
                    if teamA_xG_2nd >= 0.9 and teamA_goals_2nd == 0:
                        return 1.5, time, 'expGoals' + ';projectionA;' + str(projecttionxGTeamA) + ';realA;' + str(teamA_xG_2nd) + ';projectionShotsA;' + str(projected_shots_on_teamA) + ';realShotsA;' + str(teamA_shots_on_target_2nd) + ';projectionShotsB;' + str(projected_shots_on_teamB) + ';realShotsB;' + str(teamB_shots_on_target_2nd) + ';realB;' + str(teamB_xG_2nd) + ';' + ';teamA0;' + str(teamA_xG_2ndAt70) + ';' + str(teamB_xG_2ndAt70) + ';' + str(teamA_shots_on_target_at70 + teamB_shots_on_target_at70)
                    # if teamA_xG_2nd >= 1.5 and teamA_goals_2nd == 1:
                    #     return 1.5, time, 'expGoals' + ';projectionA;' + str(projecttionxGTeamA) + ';realA;' + str(teamA_xG_2nd) + ';projectionB;' + str(projecttionxGTeamB) + ';realB;' + str(teamB_xG_2nd) + ';' + ';teamA1;' + str(teamA_xG_2ndAt70) + ';' + str(teamB_xG_2ndAt70) + ';' + str(teamA_shots_on_target_at70 + teamB_shots_on_target_at70)
                    # if teamB_xG_2nd >= 0.9 and teamB_goals_2nd == 0:
                    #     return 1.5, time, 'expGoals' + ';projectionA;' + str(projecttionxGTeamA) + ';realA;' + str(teamA_xG_2nd) + ';projectionB;' + str(projecttionxGTeamB) + ';realB;' + str(teamB_xG_2nd) + ';' + ';teamB0;' + str(teamA_xG_2ndAt70) + ';' + str(teamB_xG_2ndAt70) + ';' + str(teamA_shots_on_target_at70 + teamB_shots_on_target_at70)
                    # if teamB_xG_2nd >= 1.5 and teamB_goals_2nd == 1:
                    #     return 1.5, time, 'expGoals' + ';projectionA;' + str(projecttionxGTeamA) + ';realA;' + str(teamA_xG_2nd) + ';projectionB;' + str(projecttionxGTeamB) + ';realB;' + str(teamB_xG_2nd) + ';' + ';teamB1;' + str(teamA_xG_2ndAt70) + ';' + str(teamB_xG_2ndAt70) + ';' + str(teamA_shots_on_target_at70 + teamB_shots_on_target_at70)
                    #
                    else:
                        return None, None, None

                #87%
                # if teamA_shots_on_target_2nd + teamB_shots_on_target_2nd >= 6:
                #     if teamA_xG_2nd >= 0.9 and teamA_goals_2nd == 0:
                #         return 1.5, time, 'expGoals' + ';projectionA;' + str(projecttionxGTeamA) + ';realA;' + str(teamA_xG_2nd) + ';projectionB;' + str(projecttionxGTeamB) + ';realB;' + str(teamB_xG_2nd) + ';' + ';teamA0;' + str(teamA_xG_2ndAt70) + ';' + str(teamB_xG_2ndAt70) + ';' + str(teamA_shots_on_target_at70 + teamB_shots_on_target_at70)
                #     if teamA_xG_2nd >= 1.5 and teamA_goals_2nd == 1:
                #         return 1.5, time, 'expGoals' + ';projectionA;' + str(projecttionxGTeamA) + ';realA;' + str(teamA_xG_2nd) + ';projectionB;' + str(projecttionxGTeamB) + ';realB;' + str(teamB_xG_2nd) + ';' + ';teamA1;' + str(teamA_xG_2ndAt70) + ';' + str(teamB_xG_2ndAt70) + ';' + str(teamA_shots_on_target_at70 + teamB_shots_on_target_at70)
                #     if teamB_xG_2nd >= 0.9 and teamB_goals_2nd == 0:
                #         return 1.5, time, 'expGoals' + ';projectionA;' + str(projecttionxGTeamA) + ';realA;' + str(teamA_xG_2nd) + ';projectionB;' + str(projecttionxGTeamB) + ';realB;' + str(teamB_xG_2nd) + ';' + ';teamB0;' + str(teamA_xG_2ndAt70) + ';' + str(teamB_xG_2ndAt70) + ';' + str(teamA_shots_on_target_at70 + teamB_shots_on_target_at70)
                #     if teamB_xG_2nd >= 1.5 and teamB_goals_2nd == 1:
                #         return 1.5, time, 'expGoals' + ';projectionA;' + str(projecttionxGTeamA) + ';realA;' + str(teamA_xG_2nd) + ';projectionB;' + str(projecttionxGTeamB) + ';realB;' + str(teamB_xG_2nd) + ';' + ';teamB1;' + str(teamA_xG_2ndAt70) + ';' + str(teamB_xG_2ndAt70) + ';' + str(teamA_shots_on_target_at70 + teamB_shots_on_target_at70)
                #     else:
                #         return None, None, None

    return None, None, None








def project_to_94_from_46_to_70(all_data, data70, team_xG_1st, fix_id):
    """
    Projette les valeurs du match à la minute 94
    en utilisant les données des minutes 46 et 70.

    Args:
        data_46 (dict): Données du match à la minute 46.
        data_70 (dict): Données du match à la minute 70.

    Returns:
        dict: Projections pour la minute 94.
    """
    projections = {}
    start_minute = 46
    mid_minute = 70
    end_minute = 94

    def project_value(current_value, rate, current_minute, target_minute):
        if current_value is None:
            return None
        current_value = float(current_value)
        return current_value + (rate * (target_minute - current_minute))

    projections = {}
    start_minute = 46
    mid_minute = 70
    end_minute = 94

    def calculate_average_rate(values):
        if len(values) < 2:
            return 0
        differences = []
        for i in range(len(values) - 1):
            diff = float(values[i+1]) - float(values[i])
            # if (diff > 0.10):
            #     #diviser par 2
            #     diff = diff - 0.01

            differences.append(diff)

        average_rate = sum(differences) / len(differences)
        return average_rate

    # Projection de xG
    listxG = [(float(d['xG']) - team_xG_1st) for d in all_data if d['xG'] is not None]
    xG_rate = calculate_average_rate(listxG)

    # Utilisation de la tendance pour ajuster la projection de xG
    projected_xG = project_value(float(data70['xG']) - team_xG_1st, xG_rate, mid_minute, end_minute)
    # if fix_id == "9cfe7a29c924c1b4":
    #     print(listxG)
    #     print(xG_rate)
    #     print(projected_xG)

    # Projection des tirs
    listShootsOn = [d['shoots']['on'] for d in all_data if d['shoots']['on'] is not None]
    shoots_rate = calculate_average_rate(listShootsOn)
    projected_shoots = int(project_value(data70['shoots']['on'], shoots_rate, mid_minute, end_minute))

    return round(projected_xG, 2), projected_shoots

#------------------------------------Begin Fonctions de profit--------------------------------------------------------------------------------------------------------------------------------------------------------------------

def getProfitOverFirstHalf(data, odd, above_minutes, type, picks, all_profit, totalOK, totalKO, total, lostMax, lostMaximum):
    stake = 1000
    goals = data['goals']
    isOk = False
    isSameMinute = False
    numberTotalGoalsBefore = 0
    if 10 <= above_minutes <= 20:
        odd = 1.50
    elif 20 <= above_minutes <= 45:
        odd = 1.9
    for goal in goals:
        time_float = getTime(str(goal['timer']))
        if time_float < above_minutes:
            numberTotalGoalsBefore = numberTotalGoalsBefore + 1
        if time_float == above_minutes:
            isSameMinute = True
        if above_minutes < time_float < 46:
            isOk = True
    if numberTotalGoalsBefore <= 4 and not isSameMinute:
        if isOk:
            lostMax = 0
            result = 'OK'
            profit = int(stake * odd) - stake
            totalOK = totalOK + 1
        else:
            lostMax = lostMax + 1
            lostMaximum = lostMax if lostMax > lostMaximum else lostMaximum
            result = 'KO'
            profit = -stake
            totalKO = totalKO + 1
        total = total + 1
        pick = ''
        if numberTotalGoalsBefore == 0:
            pick = 'Over 0.5 FIRST_HALF'
        elif numberTotalGoalsBefore == 1:
            pick = 'Over 1.5 FIRST_HALF'
        elif numberTotalGoalsBefore == 2:
            pick = 'Over 2.5 FIRST_HALF'
        elif numberTotalGoalsBefore == 3:
            pick = 'Over 3.5 FIRST_HALF'
        elif numberTotalGoalsBefore == 4:
            pick = 'Over 4.5 FIRST_HALF'
        elif numberTotalGoalsBefore == 5:
            pick = 'Over 5.5 FIRST_HALF'
            #odd

        print(str(data["dateTime"]) + ';' + ';' + data["league_name"] + ';' + str(data["id"]) + ';' + data["home_team"] + ';' + data["away_team"] + ';' + (
                  str(odd)).replace('.', ',') + ';' + pick + ';' + str(above_minutes) + ';' + type + ';' + result + ';' + str(stake) + ';' + str(
            profit))
        all_profit = all_profit + profit
        picks.append(data["id"])
    retourFT1Vote = {
        "all_profit": all_profit,
        "totalOK": totalOK,
        "totalKO": totalKO,
        "total": total,
        "lostMax": lostMax,
        "lostMaximum": lostMaximum,
        "picks": picks
    }
    return retourFT1Vote



def getProfitOverSecondHalf(data, odd, above_minutes, type, picks, all_profit, totalOK, totalKO, total, lostMax, lostMaximum):
    stake = 1000
    goals = data['goals']
    isOk = False
    isSameMinute = False
    numberTotalGoalsBefore = 0
    if 49 <= above_minutes <= 59:
        odd = 1.35
    elif 60 <= above_minutes <= 65:
        odd = 1.45
    elif 66 <= above_minutes <= 71:
        odd = 1.55
    else:
        odd = 1.7
    for goal in goals:
        time_float = getTime(str(goal['timer']))
        if time_float < above_minutes:
            numberTotalGoalsBefore = numberTotalGoalsBefore + 1
        if time_float == above_minutes:
            isSameMinute = True
        if time_float > above_minutes:
            isOk = True
    if numberTotalGoalsBefore <= 7 and not isSameMinute:
        if isOk:
            lostMax = 0
            result = 'OK'
            profit = int(stake * odd) - stake
            totalOK = totalOK + 1
        else:
            lostMax = lostMax + 1
            lostMaximum = lostMax if lostMax > lostMaximum else lostMaximum
            result = 'KO'
            profit = -stake
            totalKO = totalKO + 1
        total = total + 1
        pick = ''
        if numberTotalGoalsBefore == 0:
            pick = 'Over 0.5'
        elif numberTotalGoalsBefore == 1:
            pick = 'Over 1.5'
        elif numberTotalGoalsBefore == 2:
            pick = 'Over 2.5'
        elif numberTotalGoalsBefore == 3:
            pick = 'Over 3.5'
        elif numberTotalGoalsBefore == 4:
            pick = 'Over 4.5'
        elif numberTotalGoalsBefore == 5:
            pick = 'Over 5.5'
            #odd

        print(str(data["dateTime"]) + ';' + ';' + data["league_name"] + ';' + ';' + str(data["id"]) + ';' + data["home_team"] + ';' + data["away_team"] + ';' + (
                  str(odd)).replace('.', ',') + ';' + pick + ';' + str(above_minutes) + ';' + type + ';' + result + ';' + str(stake) + ';' + str(
            profit))
        all_profit = all_profit + profit
        picks.append(data["id"])
    retourFT1Vote = {
        "all_profit": all_profit,
        "totalOK": totalOK,
        "totalKO": totalKO,
        "total": total,
        "lostMax": lostMax,
        "lostMaximum": lostMaximum,
        "picks": picks
    }
    return retourFT1Vote

#------------------------------------End Fonctions de profit--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def extract_progressive_data_at_timer(progressive_data, target_timer):
    # Chercher les données où le timer correspond à `target_timer`
    for data in progressive_data:
        time_float = getTime(data['timer'])
        if time_float == target_timer:
            return data
    return None

def extract_timer(data):
    # Chercher les données où le timer correspond à `target_timer`
    time_float = getTime(data['timer'])
    return time_float

def getTime(duration):
    # Si le format est "X:Y+Z:W" (deux durées séparées par un '+')
    if '+' in duration:
        # Séparer les deux parties par '+'
        part1, part2 = duration.split('+')

        # Convertir la première partie (minutes:secondes ou minutes)
        if ':' in part1:
            minutes1, seconds1 = part1.split(':')
            total_minutes1 = int(minutes1) + int(seconds1) / 60
        else:
            total_minutes1 = float(part1)

        # Convertir la deuxième partie (minutes:secondes ou minutes)
        if ':' in part2:
            minutes2, seconds2 = part2.split(':')
            total_minutes2 = int(minutes2) + int(seconds2) / 60
        else:
            total_minutes2 = float(part2)

        # Additionner les deux durées
        total_minutes = total_minutes1 + 0.1* total_minutes2

    # Si le format est "X:Y" ou simplement "X"
    elif ':' in duration:
        minutes, seconds = duration.split(':')
        total_minutes = int(minutes) + int(seconds) / 60
    else:
        # Si la durée est simplement en minutes
        total_minutes = float(duration)

    return total_minutes


def extract_event(events, eventType):
    # Filter the events where the type is "goal"
    goals = [event for event in events if event["type"] == eventType]
    return goals

def extract_goals(events):
    # Filter the events where the type is "goal"
    goals = [event for event in events if event["type"] == 'goal' or event["type"] == 'penalty_score']
    return goals




def getJsonResponse(url, headersParam, queryString):
    response = requests.get(url, headers=headersParam, params=queryString)
    response_json = response.json()
    return response_json


#------------------------------------------------------------End fonctions Get--------------------------------------------------------------------------------------------------------------------------------------------