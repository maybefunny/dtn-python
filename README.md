# dtn-python

# run example:
### Host app-1

``` shell
vagrant@app-1:~$ python3 dtn-client.py 
your id: 1123da20830c4b4e8354cedad3aae30d
1) print received messages
2) send a message
(1/2): 2
send message to: 093b1d219ccc493a9986b3c7336593fe
your message is: pesan penting
added: 
{'latitude': 0, 'longitude': 0, 'lifetime': 60, 'id': '1123da20830c4b4e8354cedad3aae30d/0', 'destination_id': '093b1d219ccc493a9986b3c7336593fe', 'source_id': '1123da20830c4b4e8354cedad3aae30d', 'message': 'pesan penting'}
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
received messages:
{'latitude': 0, 'longitude': 0, 'lifetime': 59, 'id': '1123da20830c4b4e8354cedad3aae30d/0', 'destination_id': '093b1d219ccc493a9986b3c7336593fe', 'source_id': '1123da20830c4b4e8354cedad3aae30d', 'message': 'pesan penting'}
1) print received messages
2) send a message
(1/2):
````
