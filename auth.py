from flask import Flask, request, render_template, session
import sqlite3
import smtplib
import random

passkeys = ["y>?Re4l.#*j;_RUO", "/ZGfH4Pr>pO*-O+s", "'Lk=XQ%Ry?n`Srv<", "lRSG7LDWp3rj&;q>", "&3T?O{VI:;F_g(f>"]

def generate_twofactor():
    lst = []
    for i in range(17):
        lst.append(random.randint(0,9))
        if i % 4 == 0:
            lst.append(' ')
    return ''.join(map(str,lst))[2:]

def return_key():
    return passkeys[random.randint(0,4)]

def send_email(subject, body):
    sender_email = "twofactfactor@gmail.com"
    receiver_email = "deshdeepak@yahoo.com"
    password = "gvhr hoxe ugcn gxcj"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    message = f"Subject: {subject}\n\n{body}"

    server.login(sender_email, password)

    server.sendmail(sender_email, receiver_email, message)
    print("Email Sent")
    
def auth_email(subject,body,reciever):
    sender_email = "twofactfactor@gmail.com"
    password = "gvhr hoxe ugcn gxcj"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    message = f"Subject: {subject}\n\n{body}"

    server.login(sender_email, password)

    server.sendmail(sender_email, reciever, message)
    print("Email Sent")

requestDB = sqlite3.connect("requestDB.db")
authDB = sqlite3.connect("authDB.db")
reqCursor = requestDB.cursor()
authCursor = authDB.cursor()

createReqDB = """CREATE TABLE IF NOT EXISTS Requests(
    email VARCHAR(100)
)
"""
createAuthDB = """CREATE TABLE IF NOT EXISTS Auth(
    email VARCHAR(100)
)
"""

reqCursor.execute(createReqDB)
requestDB.commit()
authCursor.execute(createAuthDB)
authDB.commit()

app = Flask(__name__)
app.secret_key = '2525256662'

@app.route('/')
def main():
    return render_template("auth.html")

@app.route('/ret', methods=["GET", "POST"])
def ret():
    return render_template("auth.html")

@app.route('/req', methods=["GET", "POST"])
def req():
    try:
        email = request.form.get("authreq")
        requestDB = sqlite3.connect("requestDB.db")
        reqCursor = requestDB.cursor()
        reqCursor.execute('INSERT INTO Requests (email) VALUES (?)', (email,))
        requestDB.commit()

        authDB = sqlite3.connect("authDB.db")
        authCursor = authDB.cursor()
        authCursor.execute("SELECT * FROM Auth")
        authorize = authCursor.fetchall()
        for auth in authorize:
            if auth[0] == email:
                return render_template("exists.html")
        auth_email("User Authentication Request", "Your request has been sent", email)
        send_email("User Authentication Request", f'{email} is requesting authorization to view your blog')
        # authCursor.execute('INSERT INTO Auth (email) VALUES (?)', (email,))
        # authDB.commit()
        authCursor.execute("SELECT * FROM Auth")
        authorize = authCursor.fetchall()
        print(len(authorize))
        print(authorize)
        return render_template("req.html")
    except smtplib.SMTPRecipientsRefused:
        return render_template("invalid.html")

@app.route('/auth', methods=["GET", "POST"])
def auth():
    # requestDB = sqlite3.connect("requestDB.db")
    # authDB = sqlite3.connect("authDB.db")
    # reqCursor = requestDB.cursor()
    # authCursor = authDB.cursor()
    # email = request.form.get("userauth")
    # authCursor.execute("SELECT * FROM Auth")
    # authorize = authCursor.fetchall()
    # print(len(authorize))
    # print(authorize)
    # for auth in authorize:
    #     if auth[0] == email:
    #         return render_template("blog.html")
    # return render_template("denied.html")
    
    passkey = request.form.get("userauth")
    if passkey in passkeys:
        return render_template("blog.html")
    else:
        return render_template("denied.html")
    
@app.route('/admin')
def admin():
    two_factor = generate_twofactor()
    session['two_factor'] = two_factor
    send_email("Two factor", f'{two_factor} is your authorization code')
    return render_template("admin.html")

@app.route('/twofactor', methods=["GET", "POST"])
def twofactor():
    requestDB = sqlite3.connect("requestDB.db")
    reqCursor = requestDB.cursor()
    reqCursor.execute("SELECT * FROM Requests")
    requests = reqCursor.fetchall()
    print(len(requests))
    print(requests)
    twofactorbox = request.form.get("twofactor", '').strip()
    
    two_factor = str(session.get('two_factor', '')).strip()
    
    if twofactorbox == two_factor:
        print("Welcome")
        session.pop('two_factor', None)
        return render_template("console.html", requests=requests)
    else:
        print("Error")
        return render_template("invalidadmin.html")
 
@app.route('/allow', methods=["GET", "POST"])
def allow():
    requestDB = sqlite3.connect("requestDB.db")
    reqCursor = requestDB.cursor()
    reqCursor.execute("SELECT * FROM Requests")
    requests = reqCursor.fetchall()
    print(len(requests))
    print(requests)
    
    authDB = sqlite3.connect("authDB.db")
    authCursor = authDB.cursor()
    authCursor.execute("SELECT * FROM Auth")
    authorize = authCursor.fetchall()
    print(len(authorize))
    print(authorize)
    
    req_email = request.form.get('reqEmail')[2:-3]
    print(req_email)
    
    reqCursor.execute("DELETE FROM Requests WHERE email = ?", (req_email,))
    requestDB.commit()
    authCursor.execute('INSERT INTO Auth (email) VALUES (?)', (req_email,))
    authDB.commit()
    auth_email("Blog Authorization", f"Your request has been approved. {return_key()} is your password", req_email)
    
    reqCursor.execute("SELECT * FROM Requests")
    requests = reqCursor.fetchall()
    print(len(requests))
    print(requests)
    
    authCursor.execute("SELECT * FROM Auth")
    authorize = authCursor.fetchall()
    print(len(authorize))
    print(authorize)
    return render_template("console.html", requests=requests)
    
@app.route('/decline', methods=["GET", "POST"])
def decline():
    requestDB = sqlite3.connect("requestDB.db")
    reqCursor = requestDB.cursor()
    reqCursor.execute("SELECT * FROM Requests")
    requests = reqCursor.fetchall()
    print(len(requests))
    print(requests)
    
    authDB = sqlite3.connect("authDB.db")
    authCursor = authDB.cursor()
    authCursor.execute("SELECT * FROM Auth")
    authorize = authCursor.fetchall()
    print(len(authorize))
    print(authorize)
    
    req_email = request.form.get('reqEmail')[2:-3]
    print(req_email)
    
    reqCursor.execute("DELETE FROM Requests WHERE email = ?", (req_email,))
    requestDB.commit()
    auth_email("Blog Authorization", "Your request has been declined", req_email)
    
    reqCursor.execute("SELECT * FROM Requests")
    requests = reqCursor.fetchall()
    print(len(requests))
    print(requests)
    
    authCursor.execute("SELECT * FROM Auth")
    authorize = authCursor.fetchall()
    print(len(authorize))
    print(authorize)
    return render_template("console.html", requests=requests)
       
if __name__ == "__main__":
    app.run(debug=True)
    
    