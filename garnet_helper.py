import os
import sqlite3

garnets={}
payment_info={}

CURR_DIR = os.path.dirname(__file__)
con = sqlite3.connect(os.path.join(CURR_DIR,r'garnets.db'))

def load_data():
  cur = con.cursor()
  cur.execute(f"SELECT name FROM sqlite_master WHERE type='table';")
  if(cur.fetchone()):
    for player,amount in cur.execute(f"SELECT * FROM player_garnets"):
      garnets[player] = amount

def init_game(guild):
  garnets={}
  payment_info={}
  
  cur = con.cursor()
  cur.execute('''DROP TABLE IF EXISTS player_garnets''')
  cur.execute('''CREATE TABLE player_garnets 
              (name text, garnets int)''')
  con.commit()
  build_garnets_to_user(guild)

def build_garnets_to_user(guild):
  for member in guild.members:
    cur = con.cursor()
    if any("Players" in role.name for role in member.roles):
      user=member.display_name.split()[0]
      garnets[user] = 1
      cur.execute(f"INSERT INTO player_garnets VALUES ('{user}' , 1)")
      con.commit()

def add_player(player):
  cur = con.cursor()
  garnets[player] = 1
  cur.execute(f"INSERT INTO player_garnets VALUES ('{player}' , 1)")
  con.commit()

def delete_player(player):
  if player in garnets:
    cur = con.cursor()
    garnets.pop(player)
    cur.execute(f"DELETE FROM player_garnets WHERE name = '{player}'")
    con.commit()

def set_player_garnets(player,num_garnets):
  if player in garnets:
    cur = con.cursor()
    cur.execute(f'''UPDATE player_garnets 
                    SET garnets = {num_garnets} 
                    WHERE name = "{player}"''')
    con.commit()
    garnets[player] = num_garnets
    return True
  return False

def change_player_garnets(player, amount):
  if(player in garnets):
    new_garnets = garnets[player] + amount
    set_player_garnets(player, new_garnets)
    return True
  return False

def add_payment_info(giver,receiver,chat,amount):
    if receiver in garnets:
        payment_info[(giver,receiver,chat)]=amount
        return True
    return False

def remove_payment_info(giver,receiver,chat):
    if (giver,receiver,chat) in payment_info:
        return payment_info.pop((giver,receiver,chat))
    return -1

def get_garnets(player):
  if player in garnets:
    return garnets[player]
  return None

def get_all_garnets():
  return garnets.items()

def valid_player(name):
  return name in garnets


