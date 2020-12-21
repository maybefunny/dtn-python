# dtn-python

# run example:
### Host app-1

``` shell
vagrant@app-1:~$ python3 dtn-client.py 
your id: 1123da20830c4b4e8354cedad3aae30d
1) print received messages
2) send a message
(1/2): 2
2
send message to: 093b1d219ccc493a9986b3c7336593fe
your message is: pesan penting
added to broadcast queue
1) print received messages
2) send a message
(1/2): 
```
### Host app-2

``` shell
vagrant@app-2:~$ python3 dtn-client.py 
your id: 093b1d219ccc493a9986b3c7336593fe
1) print received messages
2) send a message
(1/2): 1
1
received messages:
{'destination_id': '093b1d219ccc493a9986b3c7336593fe', 'hop': 1, 'id': '4a9d38becdf34073aca7318d7138bef3', 'source_id': '8bd74304e4e44643a3b0a67c53f737ea', 'message': 'pesan penting', 'lifetime': 86317}
1) print received messages
2) send a message
(1/2):
````
