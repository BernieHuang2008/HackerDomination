def checker(sess, os):
    root_pwd = os["user"]["users"]["root"]["password"]
    if root_pwd != 0:
        return True
    return False
