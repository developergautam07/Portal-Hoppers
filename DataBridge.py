'''
Portal Hoppers is free software: you can redistribute
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Portal Hoppers is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Portal Hoppers.  If not, see <https://www.gnu.org/licenses/>.
'''
import sqlite3 as sl
import time

class data_bridge:
	def __init__(self):
		self.game_level = 1
		self.player_weapones = 1

	def database_setup(self):
		try:
			conn = sl.connect("data.db")
			cur = conn.cursor()
			q = "CREATE TABLE IF NOT EXISTS gamedata(datetime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, level INTEGER NOT NULL)"
			cur.execute(q)
			conn.commit()
			q1 = "CREATE TABLE IF NOT EXISTS inventory(weapon_no INTEGER PRIMARY KEY AUTOINCREMENT, weapon_name VARCHAR(15) NOT NULL DEFAULT '1' UNIQUE, active BOOLEAN DEFAULT '1')"
			cur.execute(q1)
			conn.commit()
			q2 = "INSERT INTO inventory(weapon_no, weapon_name, active) VALUES ({}, '{}', '{}')".format(1, "pistol", "Y")
			q3 = "INSERT INTO inventory(weapon_no, weapon_name, active) VALUES ({}, '{}', '{}')".format(2, "shotgun", "N")
			q4 = "INSERT INTO gamedata(datetime, level) VALUES (CURRENT_TIMESTAMP, {})".format(1)
			cur.execute(q4)
			conn.commit()
			cur.execute(q2)
			conn.commit()
			cur.execute(q3)
			conn.commit()
		#except Exception as e:
			#print(e)
		finally:
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
			#print(self.player_weapones)

		except Exception as e:
			print(e)
		finally:
			conn.close()
	
	def auto_save(self, weapon, level, quit = False):
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
			if quit:
				q2 = "UPDATE inventory SET active = '{}' WHERE weapon_no = {}".format('N', 2)
				cur.execute(q2)
				conn.commit()

		except Exception as e:
			print(e)
		finally:
			conn.close()

	def get_levels(self):
		self.load_progress()
		return self.game_level

	def get_weapones(self):
		self.load_progress()
		return self.player_weapones
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
			conn.close()
"""
db = data_bridge()
db.load_progress()
"""