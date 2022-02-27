# FTP Client Server Program
To use the server simply run the following in the terminal/ cmd prompt:

    python3 server.py

The server should run until an error is encountered. Various outputs are printed to show progress
and other relevant information. To end the server program use ^C

--------------------------------------------------------------------------------------------------------

To use the client simply run the following in a separate terminal/ cmd prompt:

    python3 client.py

The client has four total commands that can be performed
1. connect              - this command connects the client to the server
2. upload <filename>    - this command sends the desired file from the client to the server
3. get <filename>       - this command sends the desired file from the server to the client
4. quit                 - this command disconnects the client from the server and ends the client program

There is a menu with a list of the client commands and various outputs are printed to show progress
and other relevant information. Use quit to end the client program
