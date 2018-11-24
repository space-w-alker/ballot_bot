import mechanize
import getpass
import threading
import time
import sys
import re
import copy
import cli_text
from httplib import BadStatusLine

text = cli_text.Textify()
print(text.print_string("__unilag"))
print(text.print_string("_ballot"))
print(text.print_string("___bot"))


def go_to(br,exec_string):
    while(True):
        try:
            eval(exec_string)
            if(br.response().getcode() != 200):
                print(br.response().getcode())
                print("Retrying...")
                time.sleep(0.1)
                continue
            break
        except BadStatusLine:
            print("Bad Status Line \n Retrying...")
            time.sleep(0.2)
            continue
        except mechanize.URLError:
            print("Url Error...\n retrying...")
            time.sleep(0.2)
            continue
        except mechanize.BrowserStateError:
            print("Browser State Error...Opening Home Page")
            exec_string = "br.open('http://studentportal.unilag.edu.ng/(S(qiiicv5wmgvxjsrm3q0d4g2i))/StudentLoginPage.aspx')"
        except mechanize.LinkNotFoundError:
            print("Link Not Found Error Error...Opening Home Page")
            exec_string = "br.open('http://studentportal.unilag.edu.ng/(S(qiiicv5wmgvxjsrm3q0d4g2i))/StudentLoginPage.aspx')"

class User(object):

    def __init__(self):
        

        self.accom_string = "http://studentportal.unilag.edu.ng/(S(3b32hzf5m2rxptnxrb5ifonb))/AccommodationReservation.aspx?"
        self.hostel_list = ["hallid=ENI-NJOKU+HALL","hallid=PROFESSOR+SABURI+BIOBAKU+HALL","hallid=MARIERE+HALL","hallid=JAJA"]
        self.readable_hostel_list = ["ENI-NJOKU HALL", " BIOBAKU HALL", "MARIERE HALL", "JAJA HALL"]
        self.selected_hostel = []
        self.div = 1
        self.fetch_user_input()

    def fetch_user_input(self):
        while(True):
            self.matric = raw_input("Enter Your Matric No::")#[:-1]
            self.password = str(getpass.getpass("Enter your Portal Password::"))#[:-1]
            
            #print(len(self.matric))
            #print(len(self.password))

            if (len(self.matric)==0 or len(self.password)==0):
                print("\n\n\n\n!!!!!!!!!!!!!!!!  Invalid Input !!!!!!!!!!!!!!!!")
                continue
            break

        while(True):
            hostel = input("Press 0 to select Eni-Njoku Hall\nPress 1 to select Biobaku Hall\nPress 2 to select Mariere Hall\nPress 3 to select Jaja Hall\nPress 4 to attempt all hostels\n>>>")
            if(hostel < 0 or hostel > 4 or (type(hostel) != int)):
                print("\n\n\n\n!!!!!!!!!!!!!!!!!!!! *  Invalid Input  * !!!!!!!!!!!!!!!!!!!!")
                continue
            if(hostel != 4):
                self.selected_hostel.append(self.hostel_list[hostel])
                self.select_index = hostel
                break
            self.selected_hostel = self.hostel_list
            self.div = 4
            break

    def newLogin(self):
        br = mechanize.Browser()
        print(len(self.password))
        print(len(self.matric))
        br.set_handle_robots(False)
        br.set_header("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36")


        print("Connecting to http://studentportal.unilag.edu.ng/...")
        exec_string = "br.open('http://studentportal.unilag.edu.ng/(S(qiiicv5wmgvxjsrm3q0d4g2i))/StudentLoginPage.aspx')"
        go_to(br,exec_string)


        while(True):
            print("Attempting login...")
            br.select_form(nr=0) 
            br["UsernameTextBox"] = self.matric
            br["PasswordTextBox"] = self.password


            exec_string = "br.submit()"
            go_to(br,exec_string)

            if (re.search('<div class="error error-ico">Username/Password mismatch</div>',br.response().read())):
                print("\n\n\n\n!!!!!!!!!!!!!!!!!!!!  Invalid Username or Password !!!!!!!!!!!!!!!!!!!!!!!")
                self.fetch_user_input()
                continue
            break

        m = re.search('''<div class="float-right std-name">\s*Welcome,\s*(?P<name>.*?)\s*</div>''', br.response().read())
        
        print(("#"*50) + "\nlogged in as {0}\n" + ("#"*50)).format(m.group('name'))
        
        return br

def run(br,hostel_string,usr,hostel_index):

    def check_status(br):
        if (re.search(".*?StudentLoginPage.aspx$",br.response().geturl())):
            print("Oops We were Logged out \n Let's try that again")
            print(br.response().geturl())
            br = usr.newLogin()
            return True
        return False


    while(True):
        print("Clicking on Accommodation...Thread-{}".format(threading.current_thread().ident))
        exec_string = "br.follow_link(url='Accommodation.aspx')"
        go_to(br,exec_string)
        if(check_status(br)):continue

        print("Clicking On {}...").format(usr.readable_hostel_list[hostel_index])
        exec_string = "br.follow_link(url='AccommodationRooms.aspx?{}')".format(hostel_string)
        go_to(br,exec_string)
        if(check_status(br)):continue
        
        refresh_string = br.response().geturl()

        br.select_form(nr=0)
        print("Attempting to reseerve at {0}".format(usr.readable_hostel_list[hostel_index]))
        exec_string = "br.submit()"
        go_to(br,exec_string)
        if(check_status(br)):continue
        

        print("Sent Reserve Request To {}...Restarting...".format(usr.readable_hostel_list[hostel_index]))

#user = User()
#user.newLogin()

if (__name__ == "__main__"):
    user = User()
    index = 0
    for i in range(4):
        htl = user.selected_hostel[i % user.div]
        t = threading.Thread(target=run, args=(user.newLogin(),htl,user, user.select_index))
        #t.daemon = True
        try:
            t.start()
        except KeyboardInterrupt():
            sys.exit()
        
        index += 1
