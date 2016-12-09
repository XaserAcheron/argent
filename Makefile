all: compile compress

compile:
	gdcc-acc src/scripts/argent.acs -o src/acs/argent.o

compress:
	zip dist/xa-argen.pk3 src/*

