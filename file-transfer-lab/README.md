Within this package, fileServer.py needs to be running first (seperate
subshell, etc) and then run fileClient.py. The program then asks for the file
the user wishes to transfer to server. Enter name of file then press enter.

An error is produced due to line 35 of framedSock.py returning a length of 0
when it shouldn't be initially, resulting a return of None object on line 38 to the
server, which then attempt to write a None object to a file (Not the desire).
