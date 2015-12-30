# Fiddler Form
This is a script I put together to quickly transform form data captured from fiddler and turn it into a properly formatted python dictionary to be used in parameters for posting forms to do stuff.

### Eg
#### Input (coppied and pasted straight from fiddler and put into fiddlerform.txt)
action	search  
item	orc  
username  
max	463443  
maxQi	2650  

#### Output (In result_finished.txt)
payload = {  
 'action': 'search',  
 'item': 'orc',  
 'max': '463443',  
 'maxQi': '2650',  
 'username': ''  
}
