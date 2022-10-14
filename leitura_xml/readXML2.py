import xml.etree.ElementTree as et

arquivo = et.parse('29220908736011000901550010000259701892467294-nfe.xml')
#print(arquivo)
raiz = arquivo.getroot()
print(raiz) # <Element 'catalog' at 0x7fb4984ab530>
#print(raiz.tag) # 'catalog'

for filhas in raiz.findall('det'):
    prod = filhas.find('prod').text 
    print(f'Produto: {prod}')