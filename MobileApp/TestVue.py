import sys
import os
import time

def main():
    print(os.name)

if __name__ == '__main__':
    try:
            import paramiko

            # Connect to remote host
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect('10.10.189.240', username='mohad', password='Moh123123!')


            # Run the transmitted script remotely without args and show its output.
            # SSHClient.exec_command() returns the tuple (stdin,stdout,stderr)
            stdout = client.exec_command('python C:/Users/mohad/SDP/pipeline.py')[1]
            for line in stdout:
            # Process each line in the remote output
                print (line)

            client.close()
            sys.exit(0)
    except IndexError:
        pass
