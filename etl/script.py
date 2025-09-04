import csv

compromised_users = []
password_row = []
with open('passwords.csv') as passwords_file:
  password_csv = csv.DictReader(passwords_file)

  for row in password_csv:
    # row {'Username': 'jean49', 'Password': 'Da*E%OuGuc9$V1m'}
    password_row.append(row)
    compromised_users.append(row["Username"])

with open('compromised_users.txt', 'w') as compromised_user_file:
  for user in compromised_users:
    compromised_user_file.write(f"{user}\n")

import json
with open("boss_message.json", "w") as boss_message:
    boss_message_dict = {
        "recipient": "The Boss",
        "message": "Mission Success"
    }
    json.dump(boss_message_dict, boss_message)

slash_null_sig = """\
 _  _     ___   __  ____             
/ )( \\   / __) /  \\(_  _)            
) \\/ (  ( (_ \\(  O ) )(              
\\____/   \\___/ \\__/ (__)             
 _  _   __    ___  __ _  ____  ____  
/ )( \\ / _\\  / __)(  / )(  __)(    \\ 
) __ (/    \\( (__  )  (  ) _)  ) D ( 
\\_)(_/\_/\_/ \\___)(__\\_)(____)(____/ 
        ____  __     __   ____  _  _ 
 ___   / ___)(  )   / _\\ / ___)/ )( \\
(___)  \\___ \\/ (_/\\/    \\\\___ \\) __ (
       (____/\\____/\\_/\\_/(____/\\_)(_/
 __ _  _  _  __    __                
(  ( \\/ )( \\(  )  (  )               
/    /) \\/ (/ (_/\\/ (_/\\             
\\_)__)\\____/\\____/\\____/
"""

# Create and write the new password file with the Slash Null signature
with open("new_passwords.csv", "w") as new_passwords_obj:
    new_passwords_obj.write(slash_null_sig)
