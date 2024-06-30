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





if __name__ == "__main__":

    conn = pyodbc.connect(connection_string)
    #print(conn)
    cursor = conn.cursor()

    #import our data into sql
    import_augments(cursor)

    cursor.close()
    conn.close()
    print("Data Inserted")

