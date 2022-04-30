# build
build:
	gcc -o main ./main.c
# test
test:
	./main
# push
push:
	git push origin master
# fetch
fetch:
	git pull origin master