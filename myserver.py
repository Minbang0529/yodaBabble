"""

My lil server

things to do:
take user name out of list when closing server on client side
take user socket out of list when closing server on client side
on public messaging
  whos sending the message, (hint: socket being sent into userCommands)
private messages
"""

import urllib2
import sys
from ex3utils import Server
#from ex3utils import Client

# Create my server
class MyServer(Server):

  def onStart(self):
    # setting up variables for the server
    self.amountOfUsers = 0
    self.userNames = []
    self.socketList = []
    
    print "The server has started"
    
  def onStop(self):
    print "The server has stopped"
    
  def onConnect(self, socket):
    print "A user has connected"   
    # updates how many users on the server     
    self.amountOfUsers += 1
    print str(self.amountOfUsers) + " user(s) on the server"
    socket.userName = None
    socket.registered = False
    self.userCommands = UserCommands(socket)
    # informs the user about the server
    socket.send("---                  Welcome to my server                  ---")
    socket.send("--- You have to register before you can send/read messages ---")
    socket.send("---          Type REGISTER <UserName> to register          ---")

  def onDisconnect(self, socket):
    print "A user has disconnected"
    # updates how many users on the server
    self.amountOfUsers -= 1
    print str(self.amountOfUsers) + " user(s) on the server"

  def onMessage(self, socket, message):
    print "The server has recieved a message"
    (command, sep, parameter) = message.strip().partition(' ') 
    command = command.upper()
    print "Command: " + command
    print "Parameter: " + parameter
        
    # A user can only do send if they are registered
    if socket.registered == True:
      # check the command is valid and execute if it is
      if (self.userCommands.checkCommand(command)):
        if command == "PUBLIC":
          self.userCommands.sendToPublic(parameter,self.socketList)
        elif command == "HELP":
          self.userCommands.commandList();   
      else:
        socket.send("That command isnt valid, type 'help' for a list of commands")
         
    # Executes if a user isnt registered
    else:
      if command == "REGISTER":   
        # check if user name has been taken
        hasUserNameBeenTaken = False
        for uName in self.userNames:
          if uName == parameter:
            hasUserNameBeenTaken = True
        if not hasUserNameBeenTaken:        
          self.userNames.append(parameter)     
          socket.userName = parameter
          socket.registered = True
          self.socketList.append(socket)
          socket.send("You have registered with the server")
        else:
          socket.send("That user name has been taken")
          
      else:
        socket.send("You have to register before you can do anything")
       
    # Signify all is well
    return True		



class UserCommands():

  def __init__(self, socket):
    self.commands = ["REGISTER", "PUBLIC", "PRIVATE","HELP"]
    self.socket = socket
    
  # returns true if the command is a valid command, false otherwise
  def checkCommand(self,command):
    for uCommand in self.commands:
      if uCommand == command:
        return True
    return False       
  
  
<<<<<<< HEAD
"""
  def translateToLanguage(message, language):
=======
  
  def translateToLanguage(self, message, language):
>>>>>>> yoda works again
    message = message.replace(' ', '%20')
    message = message.strip()
    some_url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?key=https://translate.yandex.net/api/v1.5/tr.json/translate&text='+message+'lang='+language
    content = urllib2.urlopen(some_url).read()
    print content
    return content
"""
  #translates the message to yodaspeak
  def translateToYoda(self, message):
    message = message.replace(' ', '%20')
    message = message.strip()
    some_url = 'http://yoda-api.appspot.com/api/v1/yodish?text='+message
    content = urllib2.urlopen(some_url).read()
    content = content.strip('{}')
    content = content.strip()
    content = content[10:]
    return content

  # sends a message to everyone on the server
  def sendToPublic(self,message,socketList):
    content = self.translateToYoda(message)
    for uSocket in socketList:
      uSocket.send(content)
  
  def commandList(self):
    self.socket.send("---  Command list ---")
    self.socket.send("PUBLIC <Message> sends Message to all users")
    self.socket.send("PRIVATE <User:Message> sends a private Message to User")
    

   

# Parse the IP address and port you wish to listen on.
ip = sys.argv[1]
port = int(sys.argv[2])

try:
  # Create my server.
  server = MyServer()

  # Start server
  server.start(ip, port)
except Exception as e:
  print e
  

