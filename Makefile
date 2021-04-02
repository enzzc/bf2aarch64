Hello: Hello.o
	ld -o hello Hello.o

Hello.o: Hello.s
	as -g -o Hello.o Hello.s

Hello.s:
	python3 bfas.py > Hello.s

run: Hello
	./hello

clean:
	rm Hello.o Hello.s
