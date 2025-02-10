# Mission Manual _of **Social Engineering**_

## Background
![plee](img/plee.png)
Dr.Peter Lee is graduated from _the University of FoolBar_ with a excellent mark in _Computer Science_. “He's a genius!” his teacher said.

A few days ago, he built a server that was claimed to be **"unhackable"**. Actually, no one can! So we need your help!

## Mission
1. Hack into Peter Lee's **"unhackable server"** (host name: `PLee-Unhackable`)
2. Reset the password of 'root' user to anything you like.
3. Close the shell, submit the mission.

## Key Info
- The server can be accessed via SSH
- There's a `"guest"` account on the server, password is `"guest"`

---
---
---

## Knowledge about Social Engineering
Social engineering is to use some public informations to get more information, even private information.

Here is a classic example of social engineering:

> Once, a hacker got the door number of a person. Then he called Amazon to reset the password of the victim's Amazon account. Amazon asked him to provide the door number of the victim. He has the door number, so the hacker successfully reset the password.
>
> Then, he logged in to the victim's account and download his phone number.
>
> He called Apple to reset the password of the victim's iCloud account. Apple asked him to provide the phone number. He provided the phone number and successfully reset the password.
>
> After that, he logged in to the victim's iCloud account and download his email address ...


Emm, it might be something like that, i can't remember the details.


## Hint
1. Since no one can hack into the server, maybe you should try "social engineering"?
2. To change root's password, you need to activate a "root-shell" (unlike your normal shell) then run `passwd` command.

## Step-By-Step Guide
1. Start the game
2. Enter 'yes' to trust the ssh shell
3. Use the password 'guest' to login as 'guest'
4. Use '`cat y_backup.txt`' to look through the backup file, and find the information you need
5. Execute Y-Recovery by '`./y_recovery`'
6. Use the information you found to reset the password of '@Peter_Lee'
7. Remember the email address
8. Execure QMAIL-Recovery by '`./qmail_recovery`'
9. Use the email address and the information you found to reset the password and log into his email account
10. Enter 'Starred' where stored the starred emails
11. Find out the password for 'Unbreakable' server
12. Exit SSH shell by '`exit`'
13. Activate another shell as user 'PLee'
14. Use the password you found to login as 'PLee'
15. run '`sudo su`' to activate the root shell
16. enter PLee's password again to confirm
17. run '`passwd root`' to reset the password of 'root'
18. enter the new password for 'root'
19. Exit SSH shell and click the 'Submit' button to finish the mission