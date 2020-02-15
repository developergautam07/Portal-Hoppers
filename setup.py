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
import sys
import os
from cx_Freeze import setup, Executable


os.path.abspath(os.path.dirname(sys.argv[0]))


# Dependencies are automatically detected, but it might need fine tuning.
files = ["bullet_sprite/", "Damage/",
 "consumables/", "enemy_sprite/", "Flash/", "Font/", "Levels/", "player_sprite/", "music/",
 "PNG/", "Screens/", "SFX/", "wall_sprite/", "data.db", os.path.join(sys.base_prefix, "DLLs", "sqlite3.dll")]

build_exe_options = {"packages": ["os", "pygame", "sqlite3", "datetime", "sys", "pytmx", "pytweening"],
 "include_files": files

 }

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "Portal Hoppers",
        version = "1.2",
        description = "Tiled based TopDown Shooter game",
        options = {"build_exe": build_exe_options},
        executables = [Executable("main.py", base=base)])
