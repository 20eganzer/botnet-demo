# Todo

 - [x] Create a protocol for client-server comunication
 - [x] Make it work
 - [x] Attack library
 - [x] Add README.md
 - [ ] UUID for clients?
 - [ ] Add authentification?


# Comunication protocol

## Allowed methods for sending commands to clients are:

 - Execute a command
   - `POST /EXECUTE/sys_command`

 - DDoS an ip, optionally at location
   - `POST /ATTACK/target/port`
   - `POST /ATTACK/target/port/location`

 - Stop a DDoS attack
   - `POST /STOP/target/port`

 - Download a file to the downloads folder, optionally specifying filename
   - `POST /DOWNLOAD/url`
   - `POST /DOWNLOAD/url/filename`

  - Run a file from the downloads folder
   - `POST /RUN/filename`

## Allowed methods for sending requests to server are:

 - Notify server
   - `POST /NOTIFY/ONLINE`

 - Get file from server
   - `GET /filename`
