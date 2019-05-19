#!python3
import os
import subprocess
import zipfile
import datetime

from glob import iglob
from shutil import copyfile
from argparse import ArgumentParser
from configparser import ConfigParser

today = datetime.datetime.now().strftime('%m/%d/%Y')

#
# Build main package (as .pk3, a good ol' zip, really)
#
def makepkg(sourcePath, destPath):
	destination = destPath + ".pk3"
	wadinfoPath = destPath + ".txt" # just assume this, 'cause we can.

	print ("\n-- Compressing {filename} --".format (filename=destination))
	filelist = []
	for path, dirs, files in os.walk (sourcePath):
		for file in files:
			if file != "wadinfo.txt": # special exception
				# Remove sourcepath from filenames in zip
				splitpath = path.split(os.sep)[1:]
				splitpath.append(file)
				name = os.path.join(*splitpath)

				filelist.append((os.path.join (path, file), name,))

	distzip = zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED)
	current = 1
	for file in filelist:
		print ("[{percent:>3d}%] Adding {filename}".format(percent = int(current * 100 / len (filelist)), filename=file[1]))
		distzip.write(*file)
		current += 1

	# for wadinfo.txt, use the transformed file in the output dir
	# rather than the template one with x.x.x's still in it
	distzip.write(wadinfoPath, 'wadinfo.txt')

#
# Copy wadinfo TXT file to output directory.
#
def maketxt(sourcePath, destPath, version):
	textname = os.path.join (sourcePath, "wadinfo.txt")
	destname = destPath + ".txt"

	print("\n-- Copying {source} to {dest} --".format (source=textname, dest=destname))

	sourcefile = open (textname, "rt")
	textfile = open (destname, "wt")

	for line in sourcefile:
		line = line.replace('x.x.x', version)
		line = line.replace('xx/xx/xxxx', today)
		textfile.write(line)

	textfile.close()
	sourcefile.close()

#
# Make versioned distribution of the new build.
#
def makever(version, destPath):

	print("\n-- Making distribution version --")

	copyfile(destPath + ".pk3", destPath + "_" + version + ".pk3")
	copyfile(destPath + ".txt", destPath + "_" + version + ".txt")

#
# Main method. Loads project.ini and fires up the
# build routines for each project. 'Nuff said.
#
if __name__ == "__main__":
	cmd = ArgumentParser()
	cmd.add_argument("-d", "--dist", action="store_true", dest="dist", default=False, help="make version for distribution")
	args = cmd.parse_args()

	config = ConfigParser()
	config.read("project.ini")

	if(len(config.sections()) == 0):
		print("No projects to build. Be sure project.ini is present and set up correctly.");

	for project in config.sections():
		version   = config[project].get('Version'  , '0.0.1');
		sourceDir = config[project].get('SourceDir', 'src'  );
		distDir   = config[project].get('DistDir'  , 'dist' );
		fileName  = config[project].get('FileName' , project);

		print("\n-- Building {name} --".format(name=project));

		if not os.path.exists(distDir):
			os.mkdir(distDir)

		destPath = os.path.join(distDir, fileName)

		maketxt(sourceDir, destPath, version)
		makepkg(sourceDir, destPath)

		if(args.dist):
			makever(version, destPath)

	print("\n-- Finished! --")
