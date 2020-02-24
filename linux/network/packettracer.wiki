# Doc
https://www.reddit.com/r/Cisco/comments/9cqzwb/cisco_packet_tracer_v72_is_out_and_is_now_free/
According to wikipedia and also www.packettracernetwork.com, packet tracer 7.2 is now free to everyone. You just have to enroll on the netacad site and grab your copy. Enjoy and good studies!

# Install PacketTrace

## Sample: Install pt7.2.0

1. Download from https://www.computernetworkingnotes.com/ccna-study-guide/download-packet-tracer-for-windows-and-linux.html
2. Install from terminal:
    $ tar xf pt7.tar.gz -C pt7
    $ cd pt7
    $ ./install
    $ ./bin/PacketTracer7
     ./PacketTracer7: error while loading shared libraries: libpng12.so.0: cannot open shared object file: No such file or directory

3. [fix libpng12.so for LinuxMint 19.3](https://askubuntu.com/questions/895897/error-while-loading-shared-libraries-libpng12-so-0)
    - Download from https://packages.ubuntu.com/xenial/amd64/libpng12-0/download
    - Install by: sudo dpkg -i libpng12-0_1.2.54-1ubuntu1.1_amd64.deb
4. Try to run again, it works. But before enter, please register a free account from https://www.netacad.com/courses/packet-tracer/introduction-packet-tracer
5. Done.

