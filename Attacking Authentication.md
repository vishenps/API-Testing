**Authentication**
#basic authentication has been depricated. 

#bearer token: application doesn't have way to check if i have stolen it.  -- JWT. 

logic issues, forgeting rate limiting implimentation -- try to identify root cause. 



![Sucessful Brute force(status 200 OK) against admin account using ffuf, incredibly fast](image-8.png)




ATTACKING Tokens: 
one of elements of REST API is there has to be token in every request to identify the sender identity but it can be stolen. 


JWT each part is encoded by Base64 and seperated by full stop comproise of header.payload.signature 

how to sign JWT (PKI). 


one key thing in attacking via brute force is understanding the responses of websites : for example : INVALID USERNAME, invalid username!, password, wrong pwd! because it can help attacker where to brute force, bcz it creates a difference in response length and attacker uses that to filter it. 


***KNOWING WHAT TOOLS TO USE, PASS/DUMP the values correctly is super iMP***

