all: clean compile compress

clean:
	rm -f dist/xa-argen.pk3

compile:
	gdcc-acc src/scripts/argent.acs -o src/acs/argent.o

compress:
	zip dist/xa-argen.pk3 src/*

