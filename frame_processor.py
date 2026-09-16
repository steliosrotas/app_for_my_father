from gooey import Gooey, GooeyParser
#from argparse import ArgumentParser
import subprocess
import os
import wslPath

@Gooey(language="greek")
def main():

    parser = GooeyParser(description="Εφαρμογή Εξαγωγής Καρέ")

    parser.add_argument("Onoma_Fakelou_Eisagwghs", help="Επίλεξε Φάκελο Εισαγωγής Βίντεο", widget='DirChooser')
    parser.add_argument("Onoma_Fakelou_Eksagwghs", help="Επίλεξε Φάκελο Εξαγωγής Καρέ", widget='DirChooser')

    args = parser.parse_args()

    files_f = []
    for root, dirs, files in os.walk(args.Onoma_Fakelou_Eisagwghs):
        for file in files:
            files_f.append(os.path.join(root, file))

    s = 0
    for x in files_f:
        newpath = os.path.join(args.Onoma_Fakelou_Eksagwghs, f"VIDEO {s}")
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        pathwin = files_f[s]
        cmd_path = wslPath.to_posix(pathwin)
        win_out = os.path.join(newpath, f"output_%03d.jpg")
        output_path = wslPath.to_posix(win_out)
        cmd_path = cmd_path.replace(' ', '\\ ')
        output_path = output_path.replace(' ', '\\ ')
        command = r"wsl ffmpeg -i "+cmd_path+r" -qscale:v 2 "+output_path
        print(command)
        p = subprocess.Popen(command, shell=True)
        p.communicate()
        s += 1


    #cd $(wslpath 'C:\Users\<username>\Desktop')
    #files = [f for f in os.listdir(args.Onoma_Fakelou_Eisagwghs) if os.path.isfile(f)]
    #print(files)
    #command = "wsl python3 /mnt/wslg/distro/home/nikosrotas/imgselect/main.py"
    #subprocess.Popen(command, shell=True)

    #print(args.Onoma_Fakelou_Eisagwghs)

main()
