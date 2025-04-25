import hashlib
import os
from flask import Flask,redirect
staticPath="/home/OmegaGodzilla66/mysite/static/"
msgsPath="/home/OmegaGodzilla66/mysite/msgs/"

navbar='''
<link rel="stylesheet" href="/static/home.css">
<style>/* The navigation menu */
.navbar {
  overflow: hidden;
  background-color: #4a4a4a;
}

/* Navigation links */
.navbar a {
  float: left;
  font-size: 16px;
  color: white;
  text-align: center;
  padding: 14px 16px;
  text-decoration: none;
}

/* The subnavigation menu */
.subnav {
  float: left;
  overflow: hidden;
}

/* Subnav button */
.subnav .subnavbtn {
  font-size: 16px;
  border: none;
  outline: none;
  color: white;
  padding: 14px 16px;
  background-color: inherit;
  font-family: inherit;
  margin: 0;
}

/* Add a red background color to navigation links on hover */
 .subnav:hover .subnavbtn {
background-color:#ff656c;
}
.navbar a:hover {
  animation-name:fadeIntoColor;
  animation-duration: 0.5s;
  animation-fill-mode:forwards;
}

/* Style the subnav content - positioned absolute */
.subnav-content {
  display: none;
  position: absolute;
  left: 0;
  background-color: #ff656c;
  width: 100%;
  z-index: 1;
}

/* Style the subnav links */
.subnav-content a {
  float: left;
  color: white;
  text-decoration: none;
}

/* Add a grey background color on hover */
.subnav-content a:hover {
  background-color: #4a4a4a;
}


@keyframes fadeIntoColor {
  0%{background-color:grey}
  100%{background-color:#ff656c}
}

/* When you move the mouse over the subnav container, open the subnav content */
.subnav:hover .subnav-content {
  display: block;
}
</style><!-- The navigation menu -->
<div class="navbar">
  <a href='/poetrynet'>Home</a>
  <div class="subnav">
    <button class="subnavbtn">Chat <i class="fa fa-caret-down"></i></button>
    <div class="subnav-content">
      <a href='/poetrynet/multichat'>Chat</a>
      <a href='/poetrynet/multichat/addboard'>Create a board</a>
    </div>
  </div><a href='/poetrynet/bugreport'>Report a Bug</a>
  <a id='account'></a>
</div>
<script>
var mod = document.getElementById("account");
if (localStorage.getItem("pn:login")=="yes"){
  var dd=localStorage.getItem("pn:login_details");
  mod.innerHTML='My Account';
  mod.href='/poetrynet/login/'+dd;
}else{
  mod.href='/poetrynet/login';
  mod.innerHTML='Login';
}
</script>
'''

footer='''
<style>
/* Footer */
.footer {
  padding: 20px;
  text-align: center;
  background: #ddd;
  margin-top: 20px;
}</style>
<div class="footer"> <!--Do footer seperately-->
  <h4>POETRYNET</h4>
  <a href='/poetrynet/termsofservice'>Terms of Service</a>
</div>'''
check_login='''<script>
if (localStorage.getItem("pn:login_details")==null){
    window.location = "https://omegagodzilla66.pythonanywhere.com/poetrynet/login";
  }</script>'''

def return_file(filename):
  '''Returns the static/+filename'''
  return open('/home/OmegaGodzilla66/mysite/static/'+filename,'r').read()

def good_hash(variable):
  return hashlib.sha256(bytes(variable, "utf-8")).hexdigest()

def pf(data):
  data=normalize(data)
  return data.replace("(*q)","?").replace("(*s)","/")

import unicodedata

def normalize(text):
    normalized = unicodedata.normalize('NFD', text)
    stripped = ''.join(c for c in normalized if not unicodedata.combining(c))
    return unicodedata.normalize('NFC', stripped)




# Misc (at begining bc why not)
@app.route('/poetrynet')
def home():
  return navbar+check_login+open('/home/OmegaGodzilla66/mysite/static/index.html','r').read()+footer

@app.route("/poetrynet/done")
def done():
    """the most important url in the entire server"""
    return navbar+"Done!"+footer

@app.route('/poetrynet/termsofservice')
def tos():
  return navbar+'''<h1>Terms of Service:</h1>
  <ol>
  <li>Don't be a jerk. No racist, sexist, homophobic, ableist, etc.</li>
  <li>Don't spam. Anything. ANYTHING.(this means repeated messaging, creating boards, accounts, etc).</li>
  <li>Don't impersonate anyone (creating fake admin accounts, etc).</li>
  <li>Report all bugs, exploits, etc in the Report a Bug feature.</li>
  <li>You understand that your account can be banned at any time, for any reason without warning for not following an Admin's interpretation of the Terms Of Servuce.</li>
  <li>No code injection. Don't add any type of script to any page.</li>
  <li>Any violation of these is at the admin's discresion. By continuing to use the site, you agree for all of our usage of your data/messages. </li>
  </ol>
'''+footer

# MultiChat

@app.route('/poetrynet/multichat') # Main front end
def multichat():
  '''FRONT END - Chat'''
  return navbar+check_login+'''  <link rel="stylesheet" href="/static/home.css">
'''+open(staticPath+'MultiChat/multi.html','r').read()+footer

@app.route('/poetrynet/chatroom/<roomname>') # Chat room front end
def multichat2(roomname):
  '''FRONT END - Chat chat room'''
  return navbar+check_login+'''<link rel="stylesheet" href="/static/home.css">
'''+'<h1 id=title>'+roomname+'</h1>'+"<div class='card'>"+open(staticPath+'MultiChat/chat.html','r').read()+open(msgsPath+roomname.lower()+'.txt','r').read()+'''
</div>
      <script>
      var link = document.getElementById("add");
      if (localStorage.getItem("pn:login")=="yes"){
        link.href='/poetrynet/addboard/'+localStorage.getItem("pn:login_details")+'(*)'+document.getElementById("title").innerHTML;
        link.innerHTML="Add this board to your personal collection"
      }else{
        link.href='/poetrynet/login'
        link.innerHTML="Login to add this board to your personal collection"
      }</script>'''+check_login+footer

@app.route('/poetrynet/multimsg/<data>') # Send message back end
def multimsg(data):
  '''BACK END - Send message (Chat)
  formatting: room(*)message(*)account_details'''
  data=data.split('(*)')
  if '</script>' in data[1].lower():
    return 'Failed.'

  data[0]=pf(data[0])
  data[1]=pf(data[1])
  data[2]=pf(data[2])
  data[3]=pf(data[3])

  if not os.path.isfile('/home/OmegaGodzilla66/mysite/accounts/'+data[2]+".txt"):
    return 'Login or create an account first. [HERE]'
  t = open(msgsPath+data[0]+'.txt','r').read()


  if not open('/home/OmegaGodzilla66/mysite/accounts/'+data[2]+'.txt').readlines()[1]==good_hash(str(data[3]))+'\n':
    return 'Failed.'
  open('/home/OmegaGodzilla66/mysite/msgs/'+data[0]+'.txt','w').write("<br><a href='/poetrynet/viewaccount/"+data[2]+"'><b>"+data[2]+': </b></a>'+data[1]+"\n"+str(t))
  return redirect("https://omegagodzilla66.pythonanywhere.com/poetrynet/done", code=302)



@app.route('/poetrynet/multichat/addboard') # Add board front end
def addboard():
  '''FRONT END for adding board'''
  return navbar+check_login+'''<link rel="stylesheet" href="/static/home.css">
'''+'<h1 id=title>'+open('/home/OmegaGodzilla66/mysite/static/MultiChat/addboard.html','r').read()+footer

@app.route('/poetrynet/multichat/createboard/<data>') # Add board back end
def createboard(data):
  '''BACK END for adding board
  formatting: boardname(*)username(*)password'''
  data=data.split('(*)')
  data[0]=pf(data[0])
  data[1]=pf(data[1])
  data[2]=pf(data[2])
  data[2]=data[2].lower()
  if data[1]=='null':
    return '<br>Login first.'
  if not os.path.isfile('/home/OmegaGodzilla66/mysite/accounts/'+data[1]+'.txt'):
    return navbar+'<br>Failed'+footer
  if not open('/home/OmegaGodzilla66/mysite/accounts/'+data[1]+'.txt','r').readlines()[1]==good_hash(str(data[2]))+'\n':
    return navbar+'<br>Failed'+footer

  open('/home/OmegaGodzilla66/mysite/msgs/'+data[0]+'.txt','w').write('<br>--START BOARD--')
  return redirect('https://omegagodzilla66.pythonanywhere.com/poetrynet/done')

@app.route('/poetrynet/bugreport') # To report a bug
def bugreport():
  return navbar+check_login+'''  <link rel="stylesheet" href="/static/home.css">
'''+open('/home/OmegaGodzilla66/mysite/static/bugreport.html','r').read()
# Account stuff

@app.route('/poetrynet/login/<ddata>') # Check account existence AND front end for account page
def login(ddata):
  '''BACK END FOR LOGIN FEATURE, FRONT END FOR ACCOUNT PAGE'''
  data=ddata.split('(*)')
  data[0]=pf(data[0])
  data[1]=pf(data[1])
  dataKEY=open('/home/OmegaGodzilla66/mysite/accounts/'+data[0]+'.txt','r').readlines()
  if good_hash(str(data[1]))+'\n'==dataKEY[1] or data[1]=="red6c": # ADMIN can access any password - CHANGE LATER
    msgboards=''
    friends=''
    dk2=dataKEY[2].split('(*)')
    dk3=dataKEY[3].split('(*)')
    for i in range(len(dk2)):
      msgboards+='<a href="/chatroom/'+dk2[i]+'">'+dk2[i]+'</a>  '
    for i in range(len(dk3)):
      if dk3[i]!='':
        friends+='<a href="/poetrynet/viewaccount/'+dk3[i]+'">'+dk3[i]+'</a>  '
    return navbar+'<h1 id="usrname"> '+data[0]+'</h1><a href="/poetrynet/logout">Logout</a><p style="font-size:0px;" id=dd>'+ddata+'</p><h2>Your current joined message boards: </h2>' + msgboards +'<h2>Your current friends: </h2>'+friends+ '''
      <link rel="stylesheet" href="/static/home.css">
    <script>
      function post(){
        var data= document.getElementById("txt").value;
        var title= document.getElementById("title").value;
        var ld= localStorage.getItem("pn:login_details");
        window.open("https://omegagodzilla66.pythonanywhere.com/poetrynet/post/"+ld+"(*)"+title+"(*)"+data);
        <!--username(*)password(*)posttile(*)postmessage-->
      }
    </script>
    <h2>Post a message!</h2>
    <p>You can view your posts <a href="/poetrynet/viewaccount/'''+data[0]+'''">here</a>
    <form>
    <input type="text" id="title" placeholder="Enter the name of your post here!"/>
<input type="text" id="txt" placeholder="Type what you want to say here!"/>
<input type="submit" value="Post" onclick="post()"/><br>
</form>
    <script>
    var usr=document.getElementById("usrname").innerHTML;
    var dd =document.getElementById("dd").innerHTML;
    localStorage.setItem("pn:login","yes");
    localStorage.setItem("pn:login_details",dd);
    localStorage.setItem("pn:username",usr);
    </script>'''+footer
  else:
    return navbar+'<br>Login failed.'+footer

@app.route('/poetrynet/login') # Front end for login meathod
def login_static():
  '''FRONT END for login page'''
  return open(staticPath+'login_page.html','r').read()+footer

@app.route('/poetrynet/logout') # Logout feature
def clear_storage():
  '''Logout page'''
  return '''<script>localStorage.clear();
                    window.location.replace("/poetrynet/done");</script>'''



@app.route('/poetrynet/viewaccount/<accountname>')
def viewaccount(accountname):
  if os.path.isfile('/home/OmegaGodzilla66/mysite/accounts/'+accountname+'.txt'):
    dataKEY=open('/home/OmegaGodzilla66/mysite/accounts/'+accountname+'.txt','r').readlines()
    msgboards=''
    friends=''
    posts=''
    dk2=dataKEY[2].split('(*)')
    dk3=dataKEY[3].split('(*)')
    if os.path.exists('/home/OmegaGodzilla66/mysite/posts/'+accountname):
      dk4=os.listdir('/home/OmegaGodzilla66/mysite/posts/'+accountname)
    else:
      dk4=[]
    for i in range(len(dk2)):
      msgboards+='<a href="/poetrynet/chatroom/'+dk2[i]+'">'+dk2[i]+'</a>  '
    for i in range(len(dk3)):
      if dk3[i]!='':
        friends+='<a href="/poetrynet/viewaccount/'+dk3[i]+'">'+dk3[i]+'</a>  '

    for i in range(len(dk4)-1,-1,-1):
      dkf=open('/home/OmegaGodzilla66/mysite/posts/'+accountname+'/'+dk4[i],'r').read().split('\n')
      posts+='''<!--Add stylesheet here-->
      <div class="card">
      <h3>'''+dkf[0]+'''</h3>
      <p>'''+dkf[1]+'''</p>
    </div>'''

    return "<style>"+open("/home/OmegaGodzilla66/mysite/static/home.css","r").read()+"</style>"+navbar+check_login+'<br><h1 id="name">'+accountname+"</h1><p>Joined message boards: "+msgboards+'</p><p>Friends: '+friends+'</p><a id="friend"></a>'+""+'''

  <link rel="stylesheet" href="/home/OmegaGodzilla66/mysite/static/home.css">
    <script>
  e=document.getElementById("friend");
  if (localStorage.getItem("login")=='yes'){
    e.innerHTML='Friend this person! ';
    e.href='/poetrynet/friend/'+localStorage.getItem("pn:login_details")+'(*)'+document.getElementById("name").innerHTML;
  }else{
    window.location.replace('/login');
  }
    </script><h2>Posts</h2>'''+posts+footer
  else:
    return navbar+'<br><h1>302: Account not found</h1>'+footer

@app.route('/poetrynet/friend/<data>')
def friend(data):
  '''Back end for friending
     Formatting: myaccount(*)mypassword(*)friend's account'''
  data=data.split('(*)')
  data[0]=pf(data[0])
  data[2]=pf(data[2])
  data[1]=pf(data[1])
  if not os.path.isfile('/home/OmegaGodzilla66/mysite/accounts/'+data[2]+'.txt') or not os.path.isfile('/home/OmegaGodzilla66/mysite/accounts/'+data[0]+'.txt'):
    return navbar+'<h1>302 Error: Account not found</h1>'+footer

  if data[0] == data[2]:
    return navbar+'<h1>304 Error: Cannot friend self</h1><p>Cmon bro. Thats narcisism! You have friends! Heck Ill be your friend! Friend the admin! AAAA!!!</p>'+footer


  dataF=open('/home/OmegaGodzilla66/mysite/accounts/'+data[0]+'.txt','r').read()
  dataKEY=dataF.split('\n')

  if data[2] in dataKEY[3].split("(*)"):
    return navbar+'<h1>304 Error: Multiples not allowed</h1><p>what does that meannnnnn</p>'+footer

  if data[0]==dataKEY[0] and str(good_hash(data[1]))==dataKEY[1]:
    toreturn=dataKEY[0]+'\n'+dataKEY[1]+'\n'+dataKEY[2]+'\n'+dataKEY[3]+'(*)'+data[2]
    open('/home/OmegaGodzilla66/mysite/accounts/'+data[0]+'.txt','w').write(toreturn)
    return redirect('/poetrynet/done',code=302)

@app.route('/poetrynet/post/<data>')
def post(data):
  '''Formatting: username(*)password(*)posttile(*)postmessage'''
  data=data.split('(*)')
  if "</script>" in data[2] or "</script>" in data[3]:
    return 'Failed'
  data[0]=pf(data[0])
  data[1]=pf(data[1])
  data[2]=pf(data[2])
  data[3]=pf(data[3])

  if not os.path.isfile('/home/OmegaGodzilla66/mysite/accounts/'+data[0]+'.txt'):
    return 'Login or create an account first.'

  if not os.path.isdir('/home/OmegaGodzilla66/mysite/posts/'+data[0]+"/"):
    os.mkdir("/home/OmegaGodzilla66/mysite/posts/"+data[0]+"/")

  # Find next number
  ldrd=os.listdir('/home/OmegaGodzilla66/mysite/posts/'+data[0]+"/")
  nextNum=str(len(ldrd))
  open('/home/OmegaGodzilla66/mysite/posts/'+data[0]+'/'+nextNum+'.txt','w').write(data[2]+'\n'+data[3])

  return redirect('/poetrynet/done',code=313)

@app.route('/poetrynet/addaccount1')
def newaddaccount1():
  return open('/home/OmegaGodzilla66/mysite/static/add.html','r').read()+footer

@app.route('/poetrynet/createaccount/<data>')
def newcreateaccount(data):
  '''Formatting - username(*)password'''
  data=data.split('(*)')

  if "​" in data:
      return "Failed"

  if os.path.isfile('/home/OmegaGodzilla66/mysite/accounts/'+data[0]+'.txt'):
      return 'Account already exists. '
  else:
    open('/home/OmegaGodzilla66/mysite/accounts/'+data[0]+'.txt','w').write(data[0]+'\n'+str(good_hash(data[1]))+'\n'+'board'+'\n(*)')
    return redirect("/poetrynet/done",code=310)

def PoetryAuth(data):
  '''Formatting: username(*)password'''
  data=data.split("(*)")

  if not os.path.isfile("/home/OmegaGodzilla66/mysite/accounts/"+data[0]+".txt"):
    return False

  dataKEY=open("/home/OmegaGodzilla66/mysite/accounts/"+data[0]+".txt",'r').read().split("\n")

  if good_hash(data[1])==dataKEY[1]:
    return True

  else:
    return False

# POETRYNET 2.0 Message System
@app.route("/poetrynet/community") # community searchbar (homepage)
def community_join():
    return navbar+check_login+return_file("Communities/base.html")+footer

@app.route("/poetrynet/community/<ddata>") # viewpage for community
def community_view(ddata):
    """backend for try to join community, frontend for view community
    format: username(*)password(*)comname"""
    data=ddata.split("(*)")
    pa=PoetryAuth(ddata) # idk why this warning exists, pa is totally used. :shrug:
    if not pa: return navbar+"Please <s>branch</s> log in first"+good_hash("red6c")+footer
    #data=ddata.split("\n") <-- idk why this was here but if it's important then here it is

    ddddata = open("/home/OmegaGodzilla66/mysite/communities/"+data[2]+"/[CONFIG]"+data[2]+".txt","r").read().split("\n")

    TEMP_found = False
    if ddddata[2]=="yes": # if it's private check to see if username is allowed
        for i in ddddata[3].split("(*)"):
            if data[0] == i:
                TEMP_found=True

        if not TEMP_found:
            return navbar+check_login+"Community is private"+footer


    pposts = os.listdir("/home/OmegaGodzilla66/mysite/communities/"+data[2]+"/")
    posts="""<div class="row">
  <div class="leftcolumn">"""
    for ii in pposts:
        i=ii.split("]")
        if i[0]=="[POST":
            dddddata = open("/home/OmegaGodzilla66/mysite/communities/"+data[2]+"/[POST]"+i[1].split(".")[0]+".txt","r").read().split("\n")
            if len(dddddata[1])>100:
                dddddata[1] = dddddata[1][:97]+"..." # if it's too long, then now it's not :)
            posts+= f"""
            <!--BREAK-->
      <div class="card">
      <h2><a href='https://omegagodzilla66.pythonanywhere.com/poetrynet/community/post/{ddata}(*){i[1].split(".")[0]}'>{i[1].split(".")[0]}</a><br></h2>
      <h5>{dddddata[2]}</h5>
      <p>{dddddata[1]}</p>
           </div>"""

    posts+="</div></div>"
    css= "<style>"+open("/home/OmegaGodzilla66/mysite/static/home.css","r").read()+"</style>"
    return f"<html><head><title>View Community</title>{css}</head><body>"+navbar+check_login+"<p>This is a part of the new Communities feature. This feature is still in development.</p>"+"<h1>"+data[2]+"</h1>"+posts+footer+"</body></html>"

@app.route("/poetrynet/community/post/<ddata>")
def view_post(ddata):
    """View a post
    format: username(*)password(*)community(*)postname"""

    data=ddata.split("(*)")

    dddata = data[0]+"(*)"+data[1]


    pa=PoetryAuth(ddata) # Check to make sure user is using a valid account
    if not pa: return navbar+"Please <s>branch</s> log in first"+footer


    # Check to make sure that the user is allowed to view the community
    ddddata = open("/home/OmegaGodzilla66/mysite/communities/"+data[2]+"/[CONFIG]"+data[2]+".txt","r").read().split("\n")
    TEMP_found = False
    if ddddata[2]=="yes": # if it's private check to see if username is allowed
        for i in ddddata[3].split("(*)"):
            if data[0] == i:
                TEMP_found=True

        if not TEMP_found:
            return navbar+check_login+"Community is private"+footer

    dddddata = open("/home/OmegaGodzilla66/mysite/communities/"+data[2]+"/[POST]"+data[3]+".txt","r").read().split("\n")
    post="""<div class="row">
  <div class="leftcolumn">"""

    post+=f"""<div class="card">
      <h2 id='ttl'>{dddddata[0]}</h2><br>
      <h5 id = 'usr'>{dddddata[2]}</h5>
      <p>{dddddata[1]}</p></div>"""


    post+="</div></div>"
    comments=open("/home/OmegaGodzilla66/mysite/static/Communities/comment.html","r").read()+"<h3>Comments:</h3>\n"

    ccomments=dddddata[4:]

    for ii in ccomments:
        i=ii.split("(*)")
        comments+=f"""<div style="margin:0px; padding: 5px;"><p><b>{i[0]}</b><br style="height:1vh;">{i[1]}</p></div>"""




    css= "<style>"+open("/home/OmegaGodzilla66/mysite/static/home.css","r").read()+"</style>"
    return f"<html><head><title>View Community</title>{css}</head><body>"+navbar+check_login+"<p>This is a part of the new Communities feature. This feature is still in development.</p>"+f"<a href = 'https://omegagodzilla66.pythonanywhere.com/poetrynet/community/{dddata}(*){data[2]}'><h1 id='com'>"+data[2]+"</h1></a>"+post+comments+footer+"</body></html>"

@app.route("/poetrynet/community/createpost/<data>")
def createpost(data):
    """Creates a post - BACKEND
    formatting: username(*)password(*)community(*)title(*)contents"""
    ## Misc setup stuff ##
    ddata = data
    data = data.split("(*)")
    pa = PoetryAuth(ddata)
    pa=PoetryAuth(ddata) # Check to make sure user is using a valid account
    if not pa: return navbar+"Please <s>branch</s> log in first"+footer

    # Check to make sure that the user is allowed to view the community
    ddddata = open("/home/OmegaGodzilla66/mysite/communities/"+data[2]+"/[CONFIG]"+data[2]+".txt","r").read().split("\n")
    TEMP_found = False
    if ddddata[2]=="yes": # if it's private check to see if username is allowed
        for i in ddddata[3].split("(*)"):
            if data[0] == i:
                TEMP_found=True

        if not TEMP_found:
            return navbar+check_login+"Community is private"+footer


    ## Generate the file ##

    file = f"""{data[3]}
    {data[4]}
    {data[0]}
    0"""

    open(f"/home/OmegaGodzilla66/mysite/communities/{data[2]}/[POST]{data[3]}.txt","w").write(file)

    ## Redirect to done ##

    return redirect("https://omegagodzilla66.pythonanywhere.com/poetrynet/done", code=302)

@app.route("/poetrynet/community/createcomment/<data>")
def createcomment(data):
    """Creates a comment - BACKEND
    formatting: username(*)password(*)community(*)postTitle(*)contents"""
    ## Misc setup stuff ##
    ddata = data
    data = data.split("(*)")
    pa = PoetryAuth(ddata)
    pa=PoetryAuth(ddata) # Check to make sure user is using a valid account
    if not pa: return navbar+"Please <s>branch</s> log in first"+footer

# Check to make sure that the user is allowed to view the community
    ddddata = open("/home/OmegaGodzilla66/mysite/communities/"+data[2]+"/[CONFIG]"+data[2]+".txt","r").read().split("\n")
    TEMP_found = False
    if ddddata[2]=="yes": # if it's private check to see if username is allowed
        for i in ddddata[3].split("(*)"):
            if data[0] == i:
                TEMP_found=True

        if not TEMP_found:
            return navbar+check_login+"Community is private"+footer


    open(f"/home/OmegaGodzilla66/mysite/communities/{data[2]}/[POST]{data[3]}.txt","a").write(f"\n{data[0]}(*){data[4]}(*)0")


    return redirect("https://omegagodzilla66.pythonanywhere.com/poetrynet/done", code=302)


@app.route("/poetrynet/community/createpost/<data>")
def createpost(data):
    """Creates a post - BACKEND
    formatting: username(*)password(*)community(*)title(*)contents"""
    ## Misc setup stuff ##
    ddata = data
    data = data.split("(*)")
    pa = PoetryAuth(ddata)
    pa=PoetryAuth(ddata) # Check to make sure user is using a valid account
    if not pa: return navbar+"Please <s>branch</s> log in first"+footer

# Check to make sure that the user is allowed to view the community
    ddddata = open("/home/OmegaGodzilla66/mysite/communities/"+data[2]+"/[CONFIG]"+data[2]+".txt","r").read().split("\n")
    TEMP_found = False
    if ddddata[2]=="yes": # if it's private check to see if username is allowed
        for i in ddddata[3].split("(*)"):
            if data[0] == i:
                TEMP_found=True

        if not TEMP_found:
            return navbar+check_login+"Community is private"+footer

    postText = f"""{data[3]}
    {data[4]}
    {data[0]}
    0"""
    os.path.isfile()
    open(f"/home/OmegaGodzilla66/mysite/communities/{data[2]}/[POST]{data[3]}.txt","w").write(postText)



# Direct Messages
@app.route("/poetrynet/mydms/<data>")
def mydms(data):
  '''Formatting: username(*)password'''
  pa=PoetryAuth(data)
  ddata=data
  data=data.split("(*)")
  if pa:
    if not os.path.isfile("/home/OmegaGodzilla66/mysite/dms/"+data[0]+"/config.pyson"):
      return "Your account is not set up for this feature yet. "
    order=pyson.getData("/home/OmegaGodzilla66/mysite/dms/"+data[0]+"/config.pyson","dmlst")
    otr=""
    for i in order:
        otr+=f"<a href=/poetrynet/mydms/dm/{ddata}(*){i}>{i}</a><br>"
    return navbar+otr+footer
  else:
    return "Please <s>stick</s> log in first"

@app.route("/poetrynet/mydms/dm/<data>")
def thisdm(data):
  '''Formatting: username(*)password(*)thedm'''
  pa=PoetryAuth(data)
  data=data.split("(*)")
  if pa:
    if not os.path.isfile("/home/OmegaGodzilla66/mysite/dms/"+data[0]+"/config.pyson"):
      return "Your account is not set up for this feature yet. "
    else:
      plaintxt=open("/home/OmegaGodzilla66/mysite/dms/"+data[0]+"/"+data[2]+".txt",'r').read()
      ##splittxt=plaintxt.split("\n")

    return navbar+f"<h1 id='title'>{data[2]}</h1>"+open("/home/OmegaGodzilla66/mysite/static/dms/adm.html","r").read()+plaintxt+footer


  else:
    return "You don't have access to this"

@app.route("/poetrynet/mydms/dm/senddm/<data>")
def senddm(data):
    '''Formatting: username(*)password(*)therecipiant(*)contents'''
    # Login checks
    pa=PoetryAuth(data) # idk why this warning exists, pa is totally used. :shrug:
    data=data.split("(*)")
    if not pa: return "Please <s>branch</s> log in first"
    if not os.path.isfile("/home/OmegaGodzilla66/mysite/dms/"+data[0]+"/config.pyson"): return "Your account is not set up for this feature yet. "


    # importante i swear
    with open("/home/OmegaGodzilla66/mysite/dms/"+data[0]+"/"+data[2]+".txt","r") as dmr: t=dmr.read()

    # self file
    with open("/home/OmegaGodzilla66/mysite/dms/"+data[0]+"/"+data[2]+".txt", "w") as dmw:
        dmw.write(data[0]+": "+data[3]+"\n <br>"+t)
        dmw.close()

    # tr file
    with open("/home/OmegaGodzilla66/mysite/dms/"+data[2]+"/"+data[0]+".txt", "w") as dmw:
        dmw.write(data[0]+": "+data[3]+"\n <br>"+t)
        dmw.close()

    return redirect("https://omegagodzilla66.pythonanywhere.com/poetrynet/done", code=302)
