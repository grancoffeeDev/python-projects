from bs4 import BeautifulSoup



with open("29220908736011000901550010000259701892467294-nfe.xml", 'r') as f: 
    data = f.read() 

Bs_data = BeautifulSoup(data, "xml") 
b_unique = Bs_data.find_all('det') 

#print(b_unique) 

b_name = Bs_data.find('det', {'nItem':1}) 

print(b_name.get('prod'))

def teste():
    b_name = Bs_data.find('child', {'name':'Frank'}) 

    print(b_name) 

    value = b_name.get('test') 
  
    print(value) 