#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
from simple_term_menu import TerminalMenu

# create a database connection to the SQLite database
databaseFile = "db/band.db"
conn = sqlite3.connect(databaseFile)
conn.row_factory = lambda cursor, row: row[0]
cursor = conn.cursor()

# fetch info from db tables and assign variables
fetch_rand_adj = cursor.execute("SELECT adjective FROM banddata ORDER BY RANDOM() LIMIT 1;").fetchone()
fetch_rand_noun = cursor.execute("SELECT noun FROM banddata ORDER BY RANDOM() LIMIT 1;").fetchone()
fetch_rand_name = cursor.execute("SELECT random_name FROM banddata ORDER BY RANDOM() LIMIT 1;").fetchone()
fetch_adj = cursor.execute("SELECT adjective FROM banddata;").fetchall()
fetch_noun = cursor.execute("SELECT noun FROM banddata;").fetchall()
fetch_adj_count = cursor.execute("SELECT COUNT(adjective) FROM banddata").fetchone()
fetch_noun_count = cursor.execute("SELECT COUNT(noun) FROM banddata").fetchone()
fetch_band_names = cursor.execute("SELECT band_name FROM bandnames;").fetchall()
fetch_full_bands = cursor.execute("SELECT vocalist, bass_guitarist, drummer, electric_guitarist FROM bandmembers").fetchall()
random_adj = fetch_rand_adj
random_noun = fetch_rand_noun


# generate random band name from random adjective and random noun and add it to database
def random_band_name():
    insert_rbn_to_db_query = f"INSERT INTO bandnames (band_name) VALUES ('{random_adj} {random_noun}')"
    cursor.execute(insert_rbn_to_db_query)
    conn.commit()
    print(f"Your random band name: {random_adj} {random_noun}")


# generate band name from user chosen adjective and noun and add it to database
def user_generated_name():
    insert_ugn_to_db_query = f"INSERT INTO bandnames (band_name) VALUES ('{chosen_adj} {chosen_noun}')"
    cursor.execute(insert_ugn_to_db_query)
    conn.commit()
    print(f"Your chosen band name: {chosen_adj} {chosen_noun}")

# class to generate each band member object
class bandMember:
    def fetch_name(self):
        return cursor.execute("SELECT random_name FROM banddata ORDER BY RANDOM() LIMIT 1;").fetchone()

# defined objects
vocalist = bandMember()
bass_guitarist = bandMember()
drummer = bandMember()
electric_guitarist = bandMember()

# menu logic
def main():
    # define different menus and helper
    main_menu = TerminalMenu(["Generate band name", "Choose adjective and noun from database", "Generate band members", "Count adjectives and nouns in database"],
                             title="Rock Band Generator v1.0\nSelect option:")
    adj_menu = TerminalMenu(fetch_adj, title="Choose adjective:")
    noun_menu = TerminalMenu(fetch_noun, title="Choose noun:")
    band_names_menu = TerminalMenu(fetch_band_names, title="Choose band name you wish to assign new band members")
    main_menu_exit = False
    menu_entry_index = main_menu.show()

    # main logic for each main menu option
    while not main_menu_exit:
        if menu_entry_index == 0:
            random_band_name()
            main_menu_exit = True
        elif menu_entry_index == 1:
            adj_menu_entry_index = adj_menu.show()
            global chosen_adj
            global chosen_noun
            chosen_adj = fetch_adj[adj_menu_entry_index]
            noun_menu_entry_index = noun_menu.show()
            chosen_noun = fetch_noun[noun_menu_entry_index]
            main_menu_exit = True
            user_generated_name()
        elif menu_entry_index == 2:
            band_names_menu_index = band_names_menu.show()
            v = vocalist.fetch_name()
            b = bass_guitarist.fetch_name()
            d = drummer.fetch_name()
            e = electric_guitarist.fetch_name()
            bi = band_names_menu_index + 1
            insert_members = f"INSERT OR REPLACE INTO bandmembers (vocalist,bass_guitarist,drummer,electric_guitarist, band_name_id) VALUES ('{v}','{b}','{d}','{e}',{bi})"
            cursor.execute(insert_members)
            conn.commit()
            main_menu_exit = True
            print(f"You've added:\n Vocalist: {v}\n Bass Guitarist: {b}\n Drummer: {d}\n Electric Guitarist: {e}\n To {fetch_band_names[band_names_menu_index]} band! :)")
        elif menu_entry_index == 3:
            print(f"Currently, there is {fetch_adj_count} adjective(s) and {fetch_noun_count} noun(s) in the database")
            main_menu_exit = True
        else:
            print("Nothing selected!")

if __name__ == "__main__":
    main()
