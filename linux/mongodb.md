# Install

[Install mongodb Server](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/)
[MongoDB Shell Enhancements](https://github.com/TylerBrock/mongo-hacker)
  Also inprove mongo-shell's color, so if cooperate with vim, maybe it's better not install the hacker.
  $ ls -l  ~/.mongorc.js
    lrwxrwxrwx 1 root root 56 Mar  1 10:14 /home/hyu/.mongorc.js -> /usr/local/lib/node_modules/mongo-hacker/mongo_hacker.js
  $ sudo vi mongo_hacker.js
    //__colorize = (_isWindows() && !mongo_hacker_config['force_color']) ? false : true;
    __colorize = false;

[A dedicated repository that collects collections to practice/use](https://github.com/ozlerhakan/mongodb-json-files)


