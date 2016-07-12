#!python3
import os
import subprocess
import zipfile

SRC_DIR = "src"
DIST_DIR = "dist"
DIST_FNAME = "xaks-argent-orange"

def compileacs ():
    print ("Compiling ACS files...")

def makepkg ():
    destination = os.path.join (DIST_DIR, DIST_FNAME + ".pk3")
    if not os.path.exists (DIST_DIR):
        os.mkdir (DIST_DIR)
    if os.path.exists (DIST_FNAME):
        os.remove (DIST_FNAME)
    
    print ("Writing {filename}...".format (filename=destination))
    print ("-" * 70)
    filelist = []
    for path, dirs, files in os.walk (SRC_DIR):
        for file in files:
            # Remove "src/"
            splitpath = path.split(os.sep)[1:]
            splitpath.append (file)
            name = os.path.join (*splitpath)

            filelist.append ((os.path.join (path, file), name,))

    distzip = zipfile.ZipFile (destination, "w", zipfile.ZIP_DEFLATED)
    current = 1
    for file in filelist:
        print ("[{percent:>3d}%] Adding {filename}...".format (percent = int(current * 100 / len (filelist)), filename=file[1]))
        distzip.write (*file)
        current += 1

def maketxt ():
    sourcename = os.path.join (SRC_DIR, "wadinfo.txt")
    destname = os.path.join (DIST_DIR, DIST_FNAME + ".txt")
    print ("Copying {source} to {dest}...".format (source=sourcename, dest=destname))
    textfile = open (destname, "wb")
    sourcefile = open (sourcename, "rb")
    
    textfile.write (sourcefile.read ())
    
    textfile.close ()
    sourcefile.close ()

if __name__ == "__main__":
    compileacs ()
    makepkg ()
    maketxt ()
    
    print("Finished.")
