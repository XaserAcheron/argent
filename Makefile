all: clean compress

clean:
	rm -f dist/xa-argen.pk3

compress:
	zip dist/xa-argen.pk3 src/*
