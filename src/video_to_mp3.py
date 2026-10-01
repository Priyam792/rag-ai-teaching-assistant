import os 
import subprocess

current_dir = os.getcwd()
files = os.listdir("videos")

for file in files:
    tutorial_number = file.split(".")[0].split(" #")[1]
    file_name = file.split(" ｜")[0]
    print(tutorial_number,file_name)
        
    subprocess.run(["ffmpeg","-i", f"{current_dir}/videos/{file}",f"{current_dir}/audios/{tutorial_number}_{file_name}.mp3"], check=True)