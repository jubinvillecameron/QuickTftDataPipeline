import pyodbc

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
        print("Data inserted")
    
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
        print("Data inserted")
    
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
        print("Data inserted")
    
    except Exception as e:
        print("Error",e)
        cursor.rollback()

def import_users(cursor):

    with open("data/players.json") as f:
        players = json.load(f)

    inserted = []

    try:

        insert_query = "INSERT INTO tft.players (puuid, username) VALUES (?,?)"
        for p in players:

            username = p["username"]
            puuid = p["puuid"]

            if puuid not in inserted:
                cursor.execute(insert_query, puuid, username)

                inserted.append(puuid)

        cursor.commit()
    
    except Exception as e:
        print("Error",e)
        cursor.rollback()


def import_matches(cursor):

    with open("data/matches.json") as f:
        matches = json.load(f)

    try:

        insert_query = "INSERT INTO tft.matches (match_id, patch, game_datetimestamp) VALUES (?,?,?)"

        for m in matches:
            match_id = m["id"]
            patch = m["patch"]
            game_datetimestamp = m["date"]

            cursor.execute(insert_query,match_id,patch,game_datetimestamp)
        
        cursor.commit()


    except Exception as e:
        print(e)
        cursor.rollback()


    pass

def import_boards(cursor):

    #idea is to insert the boards themselves in first, and then store every trait_board, unit_board, augment_board in there
    #need to create triggers which update the placements when things are added into the junction tables

    #split up boards into the junction tables then do accordingly

    with open("data/boards.json") as f:
        boards = json.load(f)

    #grab boards id
    board_insert_query ="""
    INSERT INTO tft.boards (puuid, match_id, placement) 
    VALUES (?,?,?);
    SELECT SCOPE_IDENTITY() AS boardID;"""

    trait_exits_query = "SELECT traitID FROM tft.traits WHERE traitID = ?" #Check if the trait exists
    trait_insert_query = "INSERT INTO tft.traits (traitID, tier_current, tier_total, placement, num_units) VALUES (?,?,?,?,?)"
    trait_board_insert_query = "INSERT INTO tft.trait_board (traitID, boardID, placement) VALUES (?,?,?)"

    augment_board_insert_query = "INSERT INTO tft.augment_board (augmentID, boardID ,placement) VALUES (?,?,?)"

    unit_board_insert_query = "INSERT INTO tft.unit_board (boardID, unitID, item1ID, item2ID, item3ID, placement) VALUES (?,?,?,?,?,?)"


    
    for board in boards:

        placement = board["placement"]

        #first put board in
        try:
            
            cursor.execute(board_insert_query, board["puuid"], board["matchID"], placement)
            cursor.nextset()
            board_id = cursor.fetchone()[0]

        
        
            #Traits

            for trait in board['traits']:

                #first check if the trait is inside of our trait table

                cursor.execute(trait_exits_query, trait["name"])

                print(trait["name"], "Inserting..")

                inTable = cursor.fetchone()
                



                #if it's not in the table
                if inTable == None:
                    #add the trait to the trait table
                    cursor.execute(trait_insert_query, trait["name"], trait["tier_current"], trait["tier_total"], placement, trait["num_units"])
                
                #now put in our junction table
                cursor.execute(trait_board_insert_query, trait["name"], board_id, placement)

            #augments
            for augment in board['augments']:
                
                cursor.execute(augment_board_insert_query, augment, board_id ,placement)
            

            #units

            for unit in board["units"]:
                #need to also account for all of the items a unit can potentially have

                items = [None,None,None]

                for i in range(len(unit["itemNames"])):
                    
                    items[i] = unit["itemNames"]

                cursor.execute(unit_board_insert_query, board_id, unit["character_ID"], items[0], items[1], items[2], placement)




        except Exception as e:
            print(e)
            cursor.rollback()
            continue
            



        cursor.commit()







if __name__ == "__main__":

    conn = pyodbc.connect(connection_string)
    #print(conn)
    cursor = conn.cursor()

    #import our data into sql
    import_boards(cursor)
    cursor.close()
    conn.close()
    print("Data Inserted")

