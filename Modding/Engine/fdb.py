"""Database Manager class

This class acts as an interface to a content pack SQLite3 databases. Using this 
class will ensure the correct addition of template fdb files to a content pack.

Note: Requires database (in sqlite3, or script format) and a Lua template.

Example:
    To use this class individually, you wil create a custom manager instance, 
    perform a few sqlite queries and the export the data.

            fdbm = DatabaseManager()
            tArgs = {
                "BlueprintID": 1,
                "Tag"        : 'test',
            }
            fdbm.insert_into('Blueprints', 'PrebuiltTags', tArgs)
            fdbm.export_contentpack('Mods', 'TestMod')

    The previous example will export the Blueprints fdb file and the required
    lua file to load them into the Mods/TestMod/Main folder, with the tag
    test added to the game for the blueprint id 1.

The default implementation suports custom fdb only, game fdbs need to be provided as
per game context.

Todo:
    * Allow moving the templates to the setup process to add custom fdb.
    * Allow using the content pack current fdbs instead of making new ones
    * Separate game fdbs using context
    * Allow creating new fdb files from sql scripts.
    * Remove the ACSE check for non-acse mods.
    * Allow separating Init and Main fdbs (usually ownership fdbs go into Init)

"""
import os
import sys
import sqlite3
import string


# Allow for future overriding, since we have to make a distinction of fdbs by game
# we also need to add more info to template data, like destination folder, source fdb/script, etc.
default_templates = {
    #create a copy of Test database with only the content from TestTable01, others empty.
    'Test'          : ['TestTable01']
}

class DatabaseManager():

    def __init__(self):
        self.refs = {}
        self.templates = default_templates
        self.templates_path = os.path.join(os.path.dirname(__file__), 'Data')

    def get_templates(self):
        """Return the known fdb templates as a dict of name : tables to copy"""
        return self.templates

    def add_connection(self, name):
        """ Creates a memory fdb from an existing template fdb, copying the fdb structure
            and the content from the template table list.
        """
        print(f"Adding connection to {name}")
        if name not in self.get_templates().keys():
            raise Exception(f"database template not found for {name}")

        self.refs[name] = self._open_connection(':memory:')

        fdb_source = os.path.join(self.templates_path, 'fdb', name + ".fdb")
        print(fdb_source)

        try:
            tables = self._get_database_tables(fdb_source)
            self._copy_database_tables(fdb_source, self.refs[name], tables)
            self._copy_database_content(fdb_source, self.refs[name], self.get_templates()[name])
        except:
            raise Exception(f"database file not found for {name}")


    def insert_into(self, name, dbtable, tArgs):
        """ Execute an insert into a database. If the database is still not present
            in the ref list it will create one.
        """
        print(f"Inserting into {name}:{dbtable}")
        if name not in self.refs:
            self.add_connection(name)

        return self._insert_into(
            self.refs[name],
            dbtable,
            tArgs
        )

    def get_database_refs(self):
        """ Return the dict of memory fdb references """
        return self.refs

    def get_database_ref(self, name):
        """ Return the dict of memory fdb references """
        return self.refs[name] or None

    def build_databases_lua(self, mod_name, mod_acse=0.713):
        """ Returns the lua file content for the fdb files. """
        init         = open(os.path.join(self.templates_path, "fdb",  "Databases.Template.lua")).read()
        tload        = ""
        tmerge       = ""
        for fdbname in self.refs.keys():
            tload   += f"            {mod_name}{fdbname} = {{sSymbol = \"{mod_name}{fdbname}\" }},\n"
            tmerge  += f"            {fdbname} = {{ tChildrenToMerge = {{\"{mod_name}{fdbname}\"}} }},\n"
        init_data    = string.Template(init)
        init_content = init_data.substitute(Name=mod_name, tLoad=tload, tMerge=tmerge, ACSE=mod_acse)
        return init_content

    def export_contentpack(self, path, contentpack_name):
        """ Exports to {path}/Main/{contentpack_name}{fdbname}.fdb
            Creates path/Main/Databases.{contentpack_name}.lua to load the fdbs
        """
        contentpack_path = os.path.join(path, "Main", ".")
        os.makedirs(contentpack_path, exist_ok=True)

        for name in self.refs:
            fdbname = name if contentpack_name == None else contentpack_name + name
            fdbpath = os.path.join(contentpack_path, fdbname)
            print(f"exporting: {fdbname}")
            try:
                os.remove(f"{fdbpath}.fdb")
            except:
                pass
            self.refs[name].execute(f"VACUUM MAIN INTO '{fdbpath}.fdb'")

        if len(self.refs) > 0:
            databases_file = os.path.join(contentpack_path, f"Databases.{contentpack_name}.lua")
            open(databases_file, 'w').write(self.build_databases_lua(contentpack_name))


    """ SQLITE3 interface """

    def _open_connection(self, source):
        conn  = sqlite3.connect(source)
        return conn

    def _close_connection(self, conn):
        conn.commit()
        conn.close()

    # copy table structure, no data
    def _get_database_tables(self, source):
        out  = sqlite3.connect(source)
        cursor = out.execute("SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%'")
        tablenames = cursor.fetchall()
        cursor.close()
        out.close()
        tables = [t[0] for t in tablenames]
        return tables

    def _copy_database_tables(self, source, dest, tables):
        dest.execute("ATTACH '" + source +  "' as dba")
        dest.execute("BEGIN")

        for table in tables:
            cursor = dest.execute("SELECT * FROM dba.sqlite_master WHERE type='table' and name =?", (table,) )
            row = cursor.fetchall()[0]
            dest.execute(row[4])

        dest.commit()
        dest.execute("detach database dba")
        return dest

    def _copy_database_content(self, source, dest, tables, where=None):
        dest.execute("ATTACH '" + source +  "' as dba")
        dest.execute("BEGIN")
        for table in tables:
            for row in dest.execute("SELECT * FROM dba.sqlite_master WHERE type='table' and name =?", (table,) ):
                combine = "INSERT OR IGNORE INTO "+ row[1] + " SELECT * FROM dba." + row[1]
                if where:
                    combine += ' WHERE ' + where
                dest.execute(combine)
        dest.commit()
        dest.execute("detach database dba")

    def _insert_into(self, conn, dbtable, tArgs):
        """
        Query all rows in the table
        :param conn: the Connection object
        :param dbtable: the database table
        :param tArgs: dict with key values

        :return: last row id
        """
        try:
            cur    = conn.cursor()
            keys   = ','.join(tArgs.keys())
            marks  = ','.join(list('?'*len(tArgs)))
            values = tuple(tArgs.values())      
            cur.execute(f"INSERT INTO {dbtable} ({keys}) VALUES ({marks}) ", values)
            conn.commit()

        except sqlite3.Error as e:
            print(e)

        return cur.lastrowid

    def _query_fetch_all(self, conn, query):
        ret    = conn.execute(query)
        return ret.fetchall()

    def _query_params_fetch_all(conn, query, params):
        ret    = conn.execute(query, params)
        return ret.fetchall()

    def _query_params_fetch(conn, query, params):
        ret    = conn.execute(query, params)
        return ret.fetchone()



if __name__ == "__main__":

    # Create a manager
    fdbm = DatabaseManager()

    # Insert a row into Test, by default the Test database will be copied, but 
    # only the content of TestTable01 will be copied. TestTable02 will be empty.
    tArgs = {
        "TestColumnID"    : 2,
        "TestColumnValue" : 'test2',
    }
    fdbm.insert_into('Test', 'TestTable02', tArgs)

    # Export to ./Mods/TestMod1/Main/ (folder must exist)
    # it will create one fdb and a lua file
    fdbm.export_contentpack('Mods/TestMod1', 'TestMod1')


    # Create a manager for an specific game
    fdbm = DatabaseManager()

    # Work on PZ 
    fdbm.templates_path = os.path.join('Modding', 'Games', 'PlanetZoo', 'Data')
    fdbm.templates      = {
        'ModularScenery': ['ContentPacks', 'LocalGridAlignmentStyle', 'MoveObjectType', 'PlacementPartType', 'TagGroupsDefinition'],
    }

    # Insert a row into ModularScenery, this is normaly handled by the ModularScenery python class
    # instead of doing raw sql here, but this is included for testing
    tArgs = {
        'SceneryPartName'    : 'Test_Scenery',
        'PrefabName'         : None,              # will use the scenery part name
        'PlacementPartType'  : 'SimpleScenery',
        'MoveObjectType'     : 'AttachmentProp',
        'ContentPack'        : 'BaseGame'
    }
    fdbm.insert_into('ModularScenery', 'ModularSceneryParts', tArgs)

    # Export to ./Mods/TestModPZ/Main/ (folder must exist)
    # it will create one fdb and a lua file
    fdbm.export_contentpack('Mods/TestModPZ', 'TestModPZ')

