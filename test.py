# import smtplib

# # Email configuration
# sender_email = "twofactfactor@gmail.com"
# receiver_email = "rdhammpls@gmail.com"
# password = "gvhr hoxe ugcn gxcj"

# server = smtplib.SMTP("smtp.gmail.com", 587)
# server.starttls()

# subject = "Your Subject Here"
# body = "Mail send from Python"
# message = f"Subject: {subject}\n\n{body}"

# server.login(sender_email, password)

# server.sendmail(sender_email, receiver_email, message)

# print("Email Sent")


#s2f8$89fs42*lj

import random

def generate_twofactor():
    lst = []
    for i in range(17):
        lst.append(random.randint(0,9))
        if i % 4 == 0:
            lst.append(' ')
    return ''.join(map(str,lst))[2:]

print(generate_twofactor())