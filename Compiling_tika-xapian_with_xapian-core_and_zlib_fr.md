---
title: Compiling tika-xapian with xapian-core and zlib from scratch
description: ""
lead: ""
date: "2021-07-08T10:06:53-04:00"
lastmod: "2021-07-08T10:06:53-04:00"
tags:
  - work
draft: true
weight: 50
images: []
contributors:
  - Steve Sosik
---

```bash
cd ~/workspace/tika-xapian/

wget https://zlib.net/zlib-1.2.11.tar.gz
tar -xvzf zlib-1.2.11.tar.gz

wget https://oligarchy.co.uk/xapian/1.4.18/xapian-core-1.4.18.tar.xz
tar -xvf xapian-core-1.4.18.tar.xz

#wget https://oligarchy.co.uk/xapian/1.4.18/xapian-bindings-1.4.18.tar.xz
#tar -xvf xapian-bindings-1.4.18.tar.xz

cd zlib-1.2.11
./configure
make

cd ../xapian-core-1.4.18
./configure CPPFLAGS=-I/home/ssosik/workspace/tika-xapian/zlib-1.2.11 LDFLAGS=-L/home/ssosik/workspace/tika-xapian/zlib-1.2.11
make

#cd ../xapian-bindings-1.4.18/
#./configure XAPIAN_CONFIG=/home/ssosik/workspace/tika-xapian/xapian-core-1.4.18/xapian-config
#make
```

~Dead end, couldn't figure out how to build libxapian.so so I did a `sudo apt-get install libxapian-dev`~

Oh, it looks like I did produce `libxapian.so` by building xapian-core above,
under the `.libs` directory.

I did figure out how to pass custom linker args through cargo, add a
`.cargo/config` file:
```
╰─ cat --style=plain .cargo/config
[build]
rustflags = ["-C", "link-args=-L/home/ssosik/workspace/tika-xapian/xapian-core-1.4.18/.libs/"]
```
