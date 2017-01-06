from stats import Stats
from race import Race
from horse import Horse
import logging

logger = logging.getLogger()

##############################################################
# One two overall (Cameron) Bet
##############################################################
def one_two_overall(races,stat,DIFF=1):
    stat.name = "One/Two Overall"
    for race in races:
        logger.info('Date: {} Track: {} Race: {}'.format(race.date, race.track, race.race_number))
        exacta_payout = float(race.exacta['payout'])
        exacta_bet= int(race.exacta['bet_amount'])
        horses = race.sortedHorseOdds()
        if not horses:
            logger.warning('No odds for any horses- Date: {} Track: {} Race: {}'.format(race.date, race.track, race.race_number))
            continue

        if one_two_overall_conditions(horses,DIFF):
            cost_of_bet = (len(horses)-1)*2*exacta_bet
            WON=False
            if (horses[0].finish_position['position'] == '1' or horses[1].finish_position['position'] == '1'):
                WON=True
                stat.races_bet.append((race,WON))
                logger.debug('WON- Date: {} Track: {} Race: {} Net: {}'.format(race.date, race.track, race.race_number,exacta_payout-cost_of_bet))
            else:
                stat.races_bet.append((race,WON))
                logger.warning('LOST- Date: {} Track: {} Race: {}'.format(race.date, race.track, race.race_number))
            stat.appendBet([cost_of_bet, exacta_payout, WON])
    return()

def one_two_overall_conditions(horses, DIFF):
    flag = False
    if float(horses[1].odds)*DIFF <= float(horses[2].odds):
        flag = True
    return(flag)
#######################################################################

##############################################################
# Two three overall (Camerons Dad) Bet
##############################################################
def two_three_overall(races,stat,DIFF=1):
    stat.name = "Two/Three Overall"
    for race in races:
        exacta_payout = float(race.exacta['payout'])
        exacta_bet= int(race.exacta['bet_amount'])
        horses = race.sortedHorseOdds()
        if not horses:
            logger.warning('No odds for any horses- Date: {} Track: {} Race: {}'.format(race.date, race.track, race.race_number))
            continue
        elif len(horses)<4:
            logger.warning('Not enough hourse for this bet- Date: {} Track: {} Race: {}'.format(race.date, race.track, race.race_number))
            continue

        if float(horses[2].odds)*DIFF <= float(horses[3].odds):
            cost_of_bet = (len(horses)-1)*2*exacta_bet
            WON=False
            if (horses[1].finish_position['position'] == '1' or horses[2].finish_position['position'] == '1'):
                WON=True
                stat.races_bet.append((race,WON))
                logger.debug('WON- Date: {} Track: {} Race: {} Net: {}'.format(race.date, race.track, race.race_number,exacta_payout-cost_of_bet))
            else:
                logger.warning('LOST- Date: {} Track: {} Race: {}'.format(race.date, race.track, race.race_number))
            stat.appendBet([cost_of_bet, exacta_payout, WON])
    return()        
########################################################
