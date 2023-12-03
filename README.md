# Highway to Hell

Python ELF infector using Hellf lib

Project inspired by https://tmpout.sh/3/03.html

## Features

* [x] Inject user-defined code 

## Use 

```py 
python3 src/h2.py infect -c tests/exit.s -t /bin/ls -o /tmp
# infecting /bin/ls with tests/exit.s, output will be put in /tmp/
chmod +x /tmp/ls && /tmp/ls
echo $?
# 69
```
