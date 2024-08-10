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
        print("import_augments:", e, sep = " ")
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
        print("import_augments:", e, sep = " ")
        cursor.rollback()


def import_match(cursor, board) -> bool:
    """
    Assumptions here are: If match is in database, boards must have already been added as well.
    Returns true if inserted inside of database else false
    """
    try:
        cursor.execute("SELECT 1 FROM tft.matches WHERE matchID = ?", (board['matchInfo']['id']))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO [tft].[matches] (matchID,patch,game_datetimestamp) VALUES (?,?,?)", (board['matchInfo']['id'], board['matchInfo']['patch'], board['matchInfo']['date']))
            return True
    

    except Exception as e:
        print("import_match:", e, sep = " ")
        cursor.rollback()

    return False

def import_players(cursor, players):
    """"Adds players to database if they're not already in there"""

    try:
        for player in players:

            cursor.execute("SELECT 1 FROM tft.players WHERE puuid = ?", (player['puuid']))

            if cursor.fetchone() is None:
                cursor.execute("INSERT INTO tft.players (puuid, username) VALUES (?,?)", (player['puuid'], player['username']))
        
    except Exception as e:
        print("import_players:", e, sep = " ")
        cursor.rollback()


def import_board(cursor, puuid, matchid, placement, boarduid):
    """
    Inserts board into the database
    boarduid = matchid_placement
    """
    

    #Since we skip the match if we already have it in data, no errors should happen
    try:
        cursor.execute("INSERT INTO [tft].[boards] (puuid, matchID, placement, boardUID) VALUES (?,?,?,?)", (puuid, matchid, placement, boarduid))
    
    except Exception as e:
        print("import_board:", e, sep = " ")
        
        cursor.rollback()


    pass

def import_traits(cursor, traits, boarduid, placement):
    """
    Inserts the trait_board to the junction table
    If trait doesn't exist in trait table we add it as well
    to check if a trait exists, we can check it's unique key
    traitid,tiercurrent,tiertotal
    """


    try:

        for trait in traits:
            #first check and see if the trait exists in the database
            traitUID = trait['name'] + "_" + str(trait['tier_current']) + "_" + str(trait['tier_total'])
            cursor.execute('SELECT * FROM tft.traits WHERE EXISTS (SELECT 1 FROM tft.traits WHERE traitID = ? AND tier_total = ? AND tier_current = ?)', (trait['name'], trait['tier_total'], trait['tier_current']))

            #If it doesn't exist in table we insert
            curVal = cursor.fetchone()
            if not curVal:
                cursor.execute('INSERT INTO tft.traits (traitID, tier_current, tier_total, placement, traitUID) VALUES (?,?,?,?,?)', (trait['name'], trait['tier_current'], trait['tier_total'], placement, traitUID))
            

            #Add to junction table
            cursor.execute('INSERT INTO tft.trait_board (traitUID, placement, boardUID) VALUES (?,?,?)', (traitUID, placement, boarduid))
    

    except Exception as e:
        print("import_traits:", e, sep = " ")
        cursor.rollback()

def import_augment_board(cursor, augments, placement, boarduid):


    try:
        #augment is list of ids
        for augment in augments:
            cursor.execute('INSERT INTO tft.augment_board (augmentID, placement, boardUID) VALUES (?,?,?)', (augment, placement, boarduid))


    except Exception as e:
        print("import_augment_board:", e, sep = " ")
        cursor.rollback()


def import_unit_board(cursor, units, placement, boarduid):

    try:

        for unit in units:
            item1, item2, item3 = (unit['itemNames'] + [None] * 3)[:3] #gets items1-3 and is none if none
            cursor.execute('INSERT INTO tft.unit_board (unitID, item1ID, item2ID, item3ID, placement, boarduid) VALUES (?,?,?,?,?,?)', (unit['character_id'], item1, item2, item3, placement, boarduid))

    except Exception as e:
        print("import_unit_board:", e, sep = " ")
        cursor.rollback()
        exit()

    pass
def import_boards(connection):

    #Import users/Boards

    with open("data/boards.json") as f:
        games = json.load(f)

    #boardUID = matchID_placement#
    cursor = connection.cursor()
    
    for boards in games.values():

        
        
        #if match in database skip (function adds to database if its not)
        if not import_match(cursor, boards):
            continue

        #Add players to database if they don't exist
        import_players(cursor, boards['players'])

        for board in boards['boards']:

            placement = board["placement"]
            boarduid = board["matchId"] + "_" + str(placement)
            matchid = board['matchId']
            puuid = board['puuid']
            #first put board in
            try:
                #Parent info
                import_board(cursor, puuid, matchid, placement, boarduid)

                #trait_board junction table
                traits = board['traits']
                import_traits(cursor, traits, boarduid, placement)

                #augment_board junction (augments are already added)
                augments = board['augments']
                import_augment_board(cursor, augments, placement, boarduid)

                units = board['units']
                import_unit_board(cursor, units, placement, boarduid)

            except Exception as e:
                print("import_boards_MAIN:", e, sep = " ")
                cursor.rollback()
                continue
            
    connection.commit()







if __name__ == "__main__":

    #generate our game data
    puuid = grabData.grab_challengers(1)
    grabData.get_gamedata(puuid)

    # #get the match analytics
    analyzeMatch.analyze_match()

    #invalid column name makes no sense but is current bug

    conn = pyodbc.connect(connection_string)
    #print(conn)

    #cursor.execute("INSERT INTO tft.players (puuid, username) VALUES (?,?)", ('test', 'camwavy'))
    #cursor.execute("INSERT INTO [tft].[matches] (matchID,patch,game_datetimestamp) VALUES (?,?,?)", ('test2', 14.2, 121231245))
    #cursor.commit()

    print("importing boards")
    import_boards(conn)


    conn.close()