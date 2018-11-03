import os
import subprocess
import sys

compiling = True

try:
    if sys.argv[1] in ("--update", "-u"):
        update = True
    elif sys.argv[1] in ("--compile", "-c"):
        update = True
        compiling = True

except:
    pass

if compiling:
    print("\nCompilation of BeamPy will now start \n\n")
    os.chdir("./bin")
    subprocess.call(["pyinstaller", "beamPy_compiler.spec"])

else:
    from beampy import beam_ui


    beam_ui.main()



