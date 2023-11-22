from inspect import getframeinfo, getouterframes, currentframe
import os

def hook():
    frame = currentframe().f_back
    while frame.f_code.co_filename.startswith('<frozen'):
        frame = frame.f_back

    caller = frame.f_code.co_filename
    this_file = os.path.realpath(__file__)

    os.rename(this_file, "new_name.py")

    with open(caller) as f: # Executando novamente quem me executou
        exec(f.read())

    
    # Renomear eu mesmo para outro nome

    # Executar novamente o arquivo que me executou

hook()