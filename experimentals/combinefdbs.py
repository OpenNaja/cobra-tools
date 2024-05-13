### Script to combine all PZ fdbs
### Make the ./fdb folder and save all game fdb files into it.
### Have to through look up tables because some fdbs could not be filtered by name
### or they would not be merged in order.

import sqlite3
import os, sys

# content packs to test
contentPacks = [
    'Content1',
    'Content2',
    'Content3',
    'Content4',
    'Content5',
    'Content6',
    'Content7',
    'Content8',
    'Content9',
    'Content10',
    'Content11',
    'Content12',
    'Content13',
    'Content14',
    'Content15',
    'Content16',
    'Content17',
    'ContentAnniversary',
    'ContentAnniversary2',
    'ContentAnniversary3'
]

# Content 0
fdblist = {
    'Animals': 'Animals.fdb',
    'Audio': 'C0Audio.fdb',
    'Blueprints': 'C0Blueprints.fdb',
    'Education': 'C0Education.fdb',
    'Exhibits': 'C0Exhibits.fdb',
    'Franchise': 'C0Franchise.fdb',
    'Habitatboundary': 'C0Habitatboundary.fdb',
    'Inventory': 'C0Inventory.fdb',
    'Modularscenery': 'C0Modularscenery.fdb',
    'Multipart': 'C0Multipart.fdb',
    'Notifications': 'C0Notifications.fdb',
    'Paths': 'C0Paths.fdb',
    'Research': 'C0Research.fdb',
    'Rides': 'C0Rides.fdb',
    'Terraintypes': 'C0Terraintypes.fdb',
    'Trackedridecars': 'C0Trackedridecars.fdb',
    'Trackedrides': 'C0Trackedrides.fdb',
    'Weathereffects': 'C0Weathereffects.fdb',
    'Zoochallenges': 'C0Zoochallenges.fdb',
    'Zoopedia': 'C0Zoopedia.fdb',
    'Park': 'Park.fdb',
    'Plants': 'Plants.fdb',
    'Tweakables': 'Tweakables.fdb'
}

# Given a folder and a fdb, will return a memory fdb 
# combining all the fdb files into the main db.
def get_combined_database_from_packs(main_db_name, folder, output, contentPacks):

    rtdb = None

    try:
        os.remove(output + '.fdb')
    except:
        pass

    # create a memory db
    try:
        rtdb = sqlite3.connect( output + '.fdb' )
        # load main fdb into memory
        print("Loading: " + main_db_name)
        main = sqlite3.connect( os.path.join(folder, main_db_name))
        main.backup(rtdb)
    except:
        raise("Cant create runtime fdb")

    # merge the rest of fdbs
    try:
        for contentname in contentPacks:
            fname = os.path.join(folder, contentname + output + ".fdb") 
            # only if the sqlite3 file exists and it has any table, size of files without tables = 4096
            # this size checks prevents locking issues with empty fdbs, e.g. Content11Tweakables.fdb
            if os.path.isfile(fname) and os.path.getsize(fname) > 4096:
                print("Merging: " + fname)
                test = rtdb.execute("ATTACH '" + fname +  "' as dba")
                rtdb.execute("BEGIN")

                # assumming not column differences
                #for row in rtdb.execute("SELECT * FROM dba.sqlite_master WHERE type='table'"):
                #    combine = "INSERT OR IGNORE INTO "+ row[1] + " SELECT * FROM dba." + row[1]
                #    #print(combine)
                #    rtdb.execute(combine)

                # allowing column differences
                for row in rtdb.execute("SELECT * FROM dba.sqlite_master WHERE type='table'"):
                    cursor = rtdb.execute("SELECT * FROM dba." + row[1])
                    colnames = [name[0] for name in cursor.description]
                    cursor.close()
                    combine = "INSERT OR IGNORE INTO "+ row[1] + " (" + ",".join(colnames) + ") SELECT * FROM dba." + row[1]
                    rtdb.execute(combine)
                    rtdb.commit()

                rtdb.execute("PRAGMA integrity_check;")
                rtdb.execute("DETACH database dba")

            # Clean up for pending transations
            rtdb.execute("VACUUM")

    except:
        raise("Error merging databases")

    return rtdb

if __name__ == '__main__':

    for fdbname in fdblist:
        print(f"Processing {fdbname}")
        main_db_name = fdblist[fdbname] 

        get_combined_database_from_packs(main_db_name, './fdb', fdbname, contentPacks)
