#pylint:disable=C0103
#pylint:disable=C0111
#pylint:disable=W0312
"""Essential Functions Module"""

from __future__ import print_function
import base64
import ftplib
import os
import socket
import sys

ftp_buffer = 4096
ftp_address = "files.000webhost.com"
ftp_pass = "f6e7350954aa87f140d656d0a908b010"

# Function to write errors to a log and notify the user
def error_log(e, full=True,fatal=False):
	f = open("error_log.txt","a")
	f.write(str(e)+"\n")
	f.close()
	if fatal:
		raise e
	elif full:
		clear()
		exc_type, exc_value, exc_traceback = sys.exc_info()[:]
		file = exc_traceback.tb_frame.f_code.co_filename.split("\\")
		print("{} on line {} in {}".format(e,exc_traceback.tb_lineno,file[len(file)-1]))
	else:
		print(str(e))

# Function to push data to a file with support for
#grouped arguments
def write_file(data,filename="filename.txt", line=1):
	if data == tuple(data):
		if len(data) > 2:
			line = data[2]
		data, filename = data[:2]
	f = open(filename,"w")
	f.write("\n"*(line-1)+str(data))
	f.close()
	error_log("wrote data: \"{}\" to file: \"{}\" on line: \"{}\""\
	.format(data,filename,line), False)

# Function to grab data from a file with support for
#grouped arguments
def read_file(filename, line=0):
	if filename == tuple(filename):
		if len(filename) > 1:
			line = filename[1]
		filename = filename[0]
	f = open(filename,"r")
	if line < 1:
		data = f.read()
	else:
		data = f.readlines()[line-1]
	f.close()
	return data

# Function to add on to a file with support for grouped
#arguments
def append_file(data,filename="filename.txt", newline=True):
	if data == tuple(data):
		if len(data) > 2:
			newline = data[2]
		data, filename = data[:2]
	f = open(filename,"a")
	if not newline:
		f.write(str(data))
	else:
		f.write("\n"+str(data))
	f.close()
	error_log("appended data: \"{}\" to file: \"{}\""\
	.format(data,filename))

# Function to delete a file
def remove_file(filename):
	try:
		os.remove(filename)
	except OSError:
			pass

# Function for decoding data
def b64decode(s):
	data = base64.b64decode(s + '=' * (-len(s) % 4))
	return data.decode("utf8")

# Function for encoding data
def b64encode(s):
	data = base64.b64encode(s.encode("utf8"))
	return data.decode("utf8")

# Function to set up file transfer protocal credentials
def ftp_setup():
	global ftp
	connecting = True
	while connecting:
		try:
			ftp = ftplib.FTP(ftp_address)
			__hidden = b64decode(ftp_pass).split()
			ftp.login(__hidden[0],__hidden[1])
			del(__hidden)
			connecting = False
		except socket.gaierror as e:
			error_log(e)

# Function to push a local file to a server
def send_file(localfile, serverfile=False):
	if localfile == tuple(localfile):
		if len(localfile) > 1:
			localfile, serverfile = localfile
	if not serverfile:
		serverfile = localfile
	try:
		f = open(localfile,"rb")
		ftp.storbinary('STOR '+serverfile, f)
		f.close()
	except socket.error as e:
		error_log(e)
		recv_file(serverfile)
		send_file(localfile, serverfile)

# Function to grab a file from a server
def recv_file(filename):
	global count
	localfile = open(filename,"wb")
	try:
		ftp.retrbinary("RETR "+filename, localfile.write, ftp_buffer)
		count = 0
	except Exception as e:
		if count > 0:
			ftp.close()
			ftp_setup()
		count += 1
		error_log(e)
		localfile.close()
		if count >= 5:
			count = 0
			try:
				main_menu()
			except Exception as e:
				error_log(e)
		else:
			recv_file(filename)
	localfile.close()
	message = read_file(filename)
	return message

# Small function to format cash values
def cash_format(cash):
	cash = int(cash*100)/100.0
	return cash

def bank_setup():
    while True:
        try:
            listdata = b64decode(read_file("log.txt")).split("|")
        except IOError as e:
            error_log(e)
            try:
                new_blank()
            except Exception as e:
                error_log(e)
            continue
        name, last_cash, last_cash_time = listdata
        last_cash_time, last_cash = float(last_cash_time), float(last_cash)
        print(name, last_cash, last_cash_time)
        ftp_setup()
        break
    return name, last_cash, last_cash_time

def clear():
	try:
		os.system("cls")
	except Exception:
		os.system("clear")







# Is only run if file is in the __main__ namespace, for
#debugging use
if __name__ == "__main__":
	print(cash_format(2.736364736262636))
	pass
