import os
import shutil

# 切换语言
ini_path = os.path.expandvars(r"%USERPROFILE%\Documents\My Games\Sid Meier's Civilization 5\config.ini")
tmp_path = ini_path + ".tmp"

with open(ini_path, "r", encoding="utf-8", errors="ignore") as fin, \
     open(tmp_path, "w", encoding="utf-8", errors="ignore") as fout:
    for line in fin:
        if line.strip() == "Language = zh_CN":
            fout.write("Language = en_US\n")
            print("Language Change: zh_CN -> en_US")
        elif line.strip() == "Language = en_US":
            fout.write("Language = zh_CN\n")
            print("Language Change: en_US -> zh_CN")
        else:
            fout.write(line)

os.replace(tmp_path, ini_path)

# 删除路径
cache_path = os.path.join(os.environ['USERPROFILE'], r"Documents\My Games\Sid Meier's Civilization 5\cache")
mod_file = os.path.join(os.environ['USERPROFILE'], r"Documents\My Games\Sid Meier's Civilization 5\ModUserData\df3333a4-44be-4fc3-9143-21706ff451d5-1.db")

# 删除文件夹
if os.path.exists(cache_path):
    try:
        shutil.rmtree(cache_path)
    except Exception as e:
        print("Delete cache fail:", e)
    else:
        print("Delete cache success!")
else:
    print("Cache folder not found.")

# 删除文件
if os.path.exists(mod_file):
    try:
        os.remove(mod_file)
    except Exception as e:
        print("Delete temp file fail:", e)
    else:
        print("Delete temp file success!")
else:
    print("Temp file not found.")
