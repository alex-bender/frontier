# Roamer collisions
Tool for calculating collisions for the [roamer](https://github.com/abaldwin88/roamer).

It calculates hash for each file in directory and all subdirectories.  
Hash method is `sha224(file_name+file_mtime)[0:12]`  
### Usage:
```
./findit.py .
Visited items: 62
Hash, count
a92432e 2
1cd71ba 2
2f42d3f 2
3c685aa 1
11fea59 1
d06086a 1
0eb9db2 1
e1fcdd7 1
00d4245 1
27853ed 1
```

For now, it's known that this hash method will fail for each `.git` folder with at least one commit:
```
~/roamer_collisions [master] % cd /tmp
/tmp % mkdir testgitcoll
/tmp % cd testgitcoll 
testgitcoll % git init .
Initialized empty Git repository in /tmp/testgitcoll/.git/
testgitcoll [master] % touch file
testgitcoll [master●] % git add .
testgitcoll [master●] % git commit -am 'So what?'
[master (root-commit) cc1f23b] So what?
 1 file changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 file
cd ~/roamer_collisions
roamer_collisions [master] % ./findit.py /tmp/testgitcoll 
Visited items: 39
Hash, count
ff9804b 2
11e0af6 2
...
```
The reason is `git`. Git is *blazingly fast*, so:
```
ls -la .git/logs/refs/heads/master .git/refs/heads/master 
-rw-r--r-- 1 me me 542 Oct  9 22:22 .git/logs/refs/heads/master
-rw-r--r-- 1 me me  41 Oct  9 22:22 .git/refs/heads/master 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^~~~~~~~~~~~~~~~~~^^^^^^
```
As a result:
**Both files are sharing the same name and modification time, so it isn't surprising to have duplicated hashes, yeah?**

## As this is **not** actually collisions, let's look here...
```
time ./findit.py ~/
Visited items: 86511
Hash, count
43555d4 992
9be3d08 992
f109908 346
94b8e22 342
b69087b 178
b2c20be 176
f53566c 87
9e4c00e 87
07e520e 71
3743ed1 71
./findit.py ~/  15.60s user 2.36s system 99% cpu 17.998 total
```
and
```
time ./findit.py /etc 
Visited items: 2760
Hash, count
0023ea8 6
4aef647 5
78d9bff 5
f047e74 5
f7630b8 5
3ec0fb6 4
f8af333 4
dd9af97 4
29cc510 4
9b32d92 4
./findit.py /etc  0.28s user 0.12s system 16% cpu 2.396 total
```
My home dir of course contains git repos, but `/etc` -- doesn't.

## Update -- 12 symbols

```
time ./findit.py /etc
Visited items: 3185
Hash, count
3d54e5108f65 7
5dc766f5f1f4 7
55bfb14a7f71 7
0922098c17d1 7
0023ea87322b 6
4aef6476544c 5
f047e748551a 5
c31253835d7f 5
f7630b8c96b2 5
d65f16584d20 4
```

## Seems that we need to review roamer hashing method

    Please look at this script and open an issue if you think that there is an error in it.
    Thanks!
