from gooey import Gooey, GooeyParser
#from argparse import ArgumentParser
import subprocess
import os
import wslPath

@Gooey(language="greek")
def main():

    parser = GooeyParser(description="Εφαρμογή Εξαγωγής Καρέ")

    parser.add_argument("Onoma_Fakelou_Eisagwghs", help="Επίλεξε Φάκελο Εισαγωγής Φωτογραφιών", widget='DirChooser')
    parser.add_argument("Onoma_Fakelou_Eksagwghs", help="Επίλεξε Φάκελο Μετακίνησης Επιλεγμένων Φωτογραφιών", widget='DirChooser')

    args = parser.parse_args()

    cmd_path = wslPath.to_posix(args.Onoma_Fakelou_Eisagwghs)
    cmd_path = cmd_path.replace(' ', '\\ ')
    out_cmd_path = wslPath.to_posix(args.Onoma_Fakelou_Eksagwghs)
    out_cmd_path = out_cmd_path.replace(' ', '\\ ')
    command = r"wsl python3 ~/imgselect/main.py --input="+cmd_path+r" --output="+out_cmd_path
    p = subprocess.Popen(command, shell=True)


    #cd $(wslpath 'C:\Users\<username>\Desktop')
    #files = [f for f in os.listdir(args.Onoma_Fakelou_Eisagwghs) if os.path.isfile(f)]
    #print(files)
    #command = "wsl python3 /mnt/wslg/distro/home/nikosrotas/imgselect/main.py"
    #subprocess.Popen(command, shell=True)

    #print(args.Onoma_Fakelou_Eisagwghs)

main()
