import sqlite3 as sl
#import time
#from settings import *

class data_bridge:
	def __init__(self):
		self.game_level = 1
		self.player_weapones = 1
		self.saveTime = ''
		#self.__playerName = 'Player'

	def database_setup(self):
		try:
			conn = sl.connect("data.db")
			cur = conn.cursor()
			q = "CREATE TABLE IF NOT EXISTS gamedata(datetime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,playername VARCHAR(25) NOT NULL, level INTEGER NOT NULL);"
			cur.execute(q)
			conn.commit()
			q1 = "CREATE TABLE IF NOT EXISTS inventory(weapon_no INTEGER PRIMARY KEY AUTOINCREMENT, weapon_name VARCHAR(15) NOT NULL DEFAULT '1' UNIQUE, active BOOLEAN DEFAULT '1');"
			cur.execute(q1)
			conn.commit()
			q2 = "INSERT INTO inventory(weapon_no, weapon_name, active) VALUES ({}, '{}', '{}')".format(1, "pistol", "Y")
			q3 = "INSERT INTO inventory(weapon_no, weapon_name, active) VALUES ({}, '{}', '{}')".format(2, "shotgun", "N")
			q4 = "INSERT INTO gamedata(datetime, playername, level) VALUES (CURRENT_TIMESTAMP, '{}', {})".format('Player', 1)
			cur.execute(q4)
			conn.commit()
			cur.execute(q2)
			conn.commit()
			cur.execute(q3)
			conn.commit()
		except Exception as e:
			print(e)
		finally:
			cur.close()
			conn.close()
	
	def load_progress(self):
		try:
			conn = sl.connect("data.db")
			conn.row_factory = sl.Row
			cur = conn.cursor()
			q = "SELECT * FROM gamedata, inventory;"
			cur.execute(q)
			tabel_data = cur.fetchone()
			# Get Field Names
			#print(tabel_data.keys()) # or names = list(map(lambda x : x[0], cur.description))
			# Geting values from database
			self.game_level = tabel_data['level']
			q1 = "SELECT COUNT(weapon_name) AS weapones FROM inventory WHERE active = '{}';".format('Y')
			cur.execute(q1)
			weapon_data = cur.fetchone()
			self.player_weapones = weapon_data["weapones"]
			
			q2 = "SELECT * FROM gamedata"
			cur.execute(q2)
			player_n = cur.fetchone()
			self.__playerName = player_n['playername']

			cur.execute(q2)
			saving_time = cur.fetchone()
			self.saveTime = saving_time['datetime']
			#print(self.player_weapones)

		except Exception as e:
			print(e)
		finally:
			cur.close()
			conn.close()
	
	def auto_save(self, weapon, level, pl_name):
		try:
			conn = sl.connect("data.db")
			cur = conn.cursor()
			if len(weapon) > 1: 
				q = "UPDATE inventory SET active = '{}' WHERE weapon_name = '{}'".format('Y', weapon)
				cur.execute(q)
				conn.commit()
			q1 = "UPDATE gamedata SET level = {}".format(level)
			cur.execute(q1)
			conn.commit()
			q2 = "UPDATE gamedata SET datetime = CURRENT_TIMESTAMP;"#.format(time.)
			cur.execute(q2)
			conn.commit()
			q3 = "UPDATE gamedata SET playername = '{}'".format(pl_name)
			cur.execute(q3)
			conn.commit()		

		except Exception as e:
			print(e)
		finally:
			cur.close()
			conn.close()

	def update_name(self, pl_name, start = False):
		try:
			conn = sl.connect("data.db")
			cur = conn.cursor()
			q = "UPDATE gamedata SET playername = '{}'".format(pl_name)
			cur.execute(q)
			conn.commit()

			if start:
				q2 = "UPDATE inventory SET active = '{}' WHERE weapon_no = {}".format('N', 2)
				q3 = "UPDATE gamedata SET level = {}".format(1)
				cur.execute(q2)
				conn.commit()
				cur.execute(q3)
				conn.commit()

		except Exception as e:
			print(e)
		finally:
			cur.close()
			conn.close()

	def get_levels(self):
		self.load_progress()
		return self.game_level

	def get_weapones(self):
		self.load_progress()
		return self.player_weapones
	
	def get_time(self):
		self.load_progress()
		return self.saveTime

	def get_name(self):
		self.load_progress()
		print("From DB", self.__playerName)
		return self.__playerName

	def check_tabels(self):
		try:
			conn = sl.connect("data.db")
			cur = conn.cursor()
			q = "SELECT COUNT(*) FROM sqlite_master WHERE type = '{}' AND name = '{}';".format("table", "gamedata")
			cur.execute(q)
			t_count = cur.fetchone()
			return t_count
		except Exception as e:
			print(e)
		finally:
			cur.close()
			conn.close()

	'''
	def save_name(self):
		p_data = {}
		try:
			with open('playerdata.txt', 'r') as f_obj:
				p_data = eval(f_obj.readline())
				self.playerName = p_data['playername']
			conn = sl.connect("data.db")
			cur = conn.cursor()
			q = "UPDATE gamedata SET playername = '{}'".format(self.playerName)
			cur.execute(q)
			conn.commit()
		except Exception as e:
			print(e)
		finally:
			conn.close()

	def get_playerName(self):
		self.load_progress()
		return self.playerName

	'''
'''
db = data_bridge()
#db.database_setup()
db.load_progress()
print(db.saveTime)
'''