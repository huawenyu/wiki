# Install
```
    $ sudo apt-get update
    $ sudo apt-get remove docker docker-engine docker.io
    $ sudo apt install docker.io
    $ sudo systemctl start docker
    $ sudo systemctl enable docker
    $ docker --version

    $ docker run hello-world
        Got permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock:
        Get http://%2Fvar%2Frun%2Fdocker.sock/v1.40/containers/json: dial unix /var/run/docker.sock: connect: permission denied

    $ sudo groupadd docker
    $ sudo usermod -aG docker ${USER}
    $ su -s ${USER}
    $ docker run hello-world
        Hello from Docker.
        This message shows that your installation appears to be working correctly.

    $ docker images
    $ docker run busybox echo "hello from busybox"
```
