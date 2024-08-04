import pyodbc

import analyzeMatch
import grabData

from sql_connection_string import connection_string
import json


def import_all_items(cursor):

    with open("data/tft-item.json") as f:
        items = json.load(f)

    #table is organized where:
    #itemid + placement is everything, no placement so placement will be 0

    try:
        #this grabs all the items, now we can add them
        items = items["data"]

        for i in items.keys():
            
            itemId = items[i]["id"]
            placement = 0

            #insert into table
            insert_query = "INSERT INTO tft.items (itemID, placement) VALUES (?,?)"

            cursor.execute(insert_query, itemId, placement)

        
        cursor.commit()
        #print("Data inserted")
    
    except Exception as e:
        print("Error",e)
        cursor.rollback()


def import_units(cursor):

    with open("data/tft-champion.json") as f:
        champion = json.load(f)

    #table is organized where:
    #itemid + placement is everything, no placement so placement will be 0

    try:
        #this grabs all the items, now we can add them
        champ = champion["data"]

        for i in champ.keys():
            
            champid = champ[i]["id"]
            tier = champ[i]["tier"]
            placement = 0

            #insert into table
            insert_query = "INSERT INTO tft.units (unitID, tier, placement) VALUES (?,?,?)"

            cursor.execute(insert_query, champid, tier, placement)

        
        cursor.commit()
        #print("Data inserted")
    
    except Exception as e:
        print("Error",e)
        cursor.rollback()



    pass

def import_augments(cursor):

    with open("data/tft-augments.json") as f:
        aug = json.load(f)

    #table is organized where:
    #itemid + placement is everything, no placement so placement will be 0

    try:
        #this grabs all the items, now we can add them
        aug = aug["data"]

        for i in aug.keys():
            
            augID = aug[i]["id"]
            placement = 0

            #insert into table
            insert_query = "INSERT INTO tft.augments (augmentID, placement) VALUES (?,?)"

            cursor.execute(insert_query, augID, placement)

        
        cursor.commit()
        #print("Data inserted")
    
    except Exception as e:
        print("Error",e)
        cursor.rollback()


def import_match(cursor, board) -> bool:
    """
    Assumptions here are: If match is in database, boards must have already been added as well.
    Returns true if exists else false
    """

    try:
        cursor.execute("SELECT 1 FROM tft.matches WHERE match_id = ?" (board['matchInfo']['id'],))
        if cursor.fetchone()[0] is None:
            cursor.execute("INSERT INTO tft.matches (match_id,patch,game_datetimestamp) VALUES (?,?,?)", (board['matchInfo']['id'], board['matchInfo']['patch'], board['matchInfo']['date'],))
            return True
    

    except Exception as e:
        print(e)
        cursor.rollback()

    return False

def import_players(cursor, players):
    """"Adds players to database if they're not already in there"""

    try:
        for player in players:

            cursor.execute("SELECT 1 FROM tft.players WHERE puuid = ?" (player['puuid']))

            if cursor.fetchone()[0] is None:
                cursor.execute("INSERT INTO tft.players (puuid, username) VALUES (?,?)", (player['puuid'], player['username'],))
        
    except Exception as e:

        print(e)
        cursor.rollback()

def import_traits(cursor, traits):
    
    pass    


def import_boards(cursor):

    #Import users/Boards

    with open("data/boards.json") as f:
        boards = json.load(f)

    #boardUID = matchID_placement#
    
    for board in boards:

        placement = board["placement"]
        boarduid = board["matchId"] + "_" + str(placement)
        
        #first put board in
        try:

            #if match in database skip (function adds to database if its not)
            if import_match(cursor, board):
                continue
            
            #Add players to database if they don't exist
            import_players(cursor, board['players'])

            #Inside actual board data

            



            


            pass


        except Exception as e:
            print("ERROR")
            print(e)
            cursor.rollback()
            continue
            



    cursor.commit()







if __name__ == "__main__":

    #generate our game data
    puuid = grabData.grab_challengers(1)
    grabData.get_gamedata(puuid)

    #get the match analytics
    analyzeMatch.analyze_match()

    #TODO: is it's already inserted ignore it and insert the next thing



    # conn = pyodbc.connect(connection_string)
    # #print(conn)
    # cursor = conn.cursor()

    # import_matches(cursor)
    # import_users(cursor)
    # import_boards(cursor)

    # cursor.close()