<!-- Title -->
<h1> Chat Room GUI Python Vers. </h1>

<!-- Description -->
<h2> Description </h2>

<!-- 1. Describe the project -->
<p> Chat Room GUI is fully python based that uses the DearPyGUI framework. It allows users to run the client app in which they will choose a name to be represented and can chat with people connected to the local network. </p>

<!-- 2. Explain why you made it -->
<p> The reason why I made this was to understand sockets better and trying to get used to the DearPyGUI framework. </p>

<!-- 3. Describe how a Chatroom is made -->
<p> The chatroom is made by having a server side and a client script. The server would be continuously listening to connections while the clients can enter at any point in time while the server is still running. It is very important to make sure that the client side connects to the right port or it won't work. Messages are sent in bytes so they need to be encoded and decoded by a format, in my case I used utf-8. </p>

<!-- Technologies and Frameworks -->
<h2> Technologies and Frameworks </h2>
<p> Make sure to install the DearPyGUI and Playsound Modules for it to work. You can follow the installation to DearPyGUI <a href="https://github.com/hoffstadt/DearPyGui"> here </a>, and install Playsound <a href="https://pypi.org/project/playsound/"> here </a>.</p> 

<p> You could always just do <i> pip install dearpygui </i> and <i> pip install playsound. </i> </p>

<ul>
    <li><i>PyCharm IDE</i> - Environment </li>
    <li><i>DearPyGUI</i> - Framework used to create the GUI </li>
    <li><i>Plasound</i> - Module used to allow sound to be played when receiving a message </li>
    <li><i>Python 3.8</i> - Python vers.</li>
</ul>
  

<!-- How to Setup -->
<h2> How to Setup </h2>
<ol>
    <li> Make sure to have DearPyGUI and Playsound installed which can be found in the Technologies and Frameworks section</li>
    <li> Use a command console or git bash to execute the server.py (This needs to be running as it manages the connections and broadcasts the messages to other clients) </li>
    <li> Using and IDE or a command console, execute the main.py and a GUI should pop up (Check out the <a href="https://github.com/gnikkoch96/Python-Chat-Server-GUI/blob/master/README.md#-demonstration-"> demonstration section </a> on how to do the rest) </li>
</ol>

<!-- Demonstration-->
<h2> Demonstration </h2>

<!-- Entering Username -->
<h2> Entering Username </h2>
<img src="https://github.com/gnikkoch96/Python-Chat-Server-GUI/blob/master/resources/read_me/Entering-Example.gif"/>

<!-- Sending a Message -->
<h2> Sending a Message </h2>
<img src="https://github.com/gnikkoch96/Python-Chat-Server-GUI/blob/master/resources/read_me/Chatting-Example.gif"/>

<!-- Exiting Chatroom -->
<h2> Exiting Chatroom </h2>
<img src="https://github.com/gnikkoch96/Python-Chat-Server-GUI/blob/master/resources/read_me/Exit-Example.gif"/>

<!-- What I learned -->
<h2> What I learned </h2>
<ul>
    <li> At least two scripts need to run which is the server side and the client side.</li>
    <li> AF_INET is used to declare that the socket can only interact with IPv4 addresses</li>
    <li> SOCK_STREAM means that the connection is a TCP socket which means that it can only receive TCP packets</li>
    <li>The bind() is used in the server-side to bind the ip address to a port, and the client uses the connect() to connect to said port. The socket that gets binded is converted to a server socket</li> 
</ul>

<!-- Credit -->
<h2> Credit </h2>
<ul>
    <li>Banner was made using <a href="https://www.canva.com/"> Canva </a></li>
    <li>Notification sound was found on <a href="https://www.sounds-resource.com/"> Sounds Resource </a> </li>
    <li>The font that was used can be found at <a href="https://www.dafont.com/"> DaFont</a></li>
</ul>

