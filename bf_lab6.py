print("######the following are the usernames######")
for i in range(150):
    if i % 3:
        print("carlos")
    else:
        print("wiener")


print("######the following are the passwords######")
with open("/Users/paurushsmacmini/Documents/authentication_ip_block_bf.txt") as f:
    lines = f.readlines()

i=0
for pwd in lines:
    if i % 3:
        print(pwd.strip("\n"))
    else:
        print("peter")
        print(pwd.strip("\n"))
        i = i+1
    i=i+1    

    
