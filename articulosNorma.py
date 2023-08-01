import xml.etree.ElementTree as ET

import requests
from collections import defaultdict



# Función para recorrer los ancestros de un elemento y recolectar su información
def recolectar_ancestros(elemento, padres):
    ancestros = []
    # Si el elemento tiene un padre
    if elemento in padres:
        padre = padres[elemento]
        info_padre = {'tipoParte': padre.attrib.get('tipoParte'),
                      'texto': padre.find("{http://www.leychile.cl/esquemas}Texto").text if padre.find("{http://www.leychile.cl/esquemas}Texto") is not None else ""}
        ancestros.append(info_padre)
        # Recursivamente, recolectamos la información de los demás ancestros
        ancestros.extend(recolectar_ancestros(padre, padres))

    # Filtramos los ancestros para eliminar los datos no deseados
    ancestros = [ancestro for ancestro in ancestros if not (ancestro['tipoParte'] is None and ancestro['texto'] == '')]

    return ancestros





def parse_XML(contenidoXML):

    articulos = []  

    root = ET.fromstring(contenidoXML)

    padres = {child: parent for parent in root.iter() for child in parent}
    # Recorre todos los elementos del archivo XML
    #ARTICULOS
    for element in root.iter():
        # Busca los elementos que representan artículos
        if element.attrib.get('tipoParte') == 'Artículo':
            # Crea un diccionario para el artículo
            articulo = {"metadata": {}}
            # Busca el número y el texto del artículo
            for subelement in element.iter():
                if subelement.tag == "{http://www.leychile.cl/esquemas}NombreParte":
                    articulo['metadata']['numero'] = subelement.text
                elif subelement.tag == "{http://www.leychile.cl/esquemas}Texto":
                    articulo['content'] = subelement.text
                elif subelement.tag == "{http://www.leychile.cl/esquemas}TituloParte":
                    articulo['metadata']['titulo'] = subelement.text
            # Add additional keys from 'EstructuraFuncional' to metadata
            articulo['metadata']['transitorio'] = element.attrib.get('transitorio')
            articulo['metadata']['tipoParte'] = element.attrib.get('tipoParte')
            articulo['metadata']['fechaVersion'] = element.attrib.get('fechaVersion')
            articulo['metadata']['derogado'] = element.attrib.get('derogado')
            articulo['metadata']['idParte'] = element.attrib.get('idParte')
            # Add the article to the list of articles
            articulo['metadata']['ancestros'] = recolectar_ancestros(element, padres)



            # Añade el artículo a la lista de artículos            
            articulos.append(articulo)

    #METADATOS

    # Crea un diccionario para almacenar los metadatos
    metadatos = {}

    # Recorre todos los elementos del archivo XML
    for element in root.iter():
        if element.tag == "{http://www.leychile.cl/esquemas}Tipo":
            metadatos['Tipo'] = element.text
        elif element.tag == "{http://www.leychile.cl/esquemas}Numero":
            metadatos['numero'] = element.text
        elif element.tag == "{http://www.leychile.cl/esquemas}Materias":
            metadatos['Materias'] = element.text
        elif element.tag == "{http://www.leychile.cl/esquemas}TituloNorma":
            metadatos['TituloNorma'] = element.text
        elif element.tag == "{http://www.leychile.cl/esquemas}Organismo":
            metadatos['Organismo'] = element.text
        elif element.tag == "{http://www.leychile.cl/esquemas}Norma":
            metadatos['fechaVersion'] = element.attrib['fechaVersion']
            metadatos['normaId'] = element.attrib['normaId']
            metadatos['esTratado'] = element.attrib['esTratado']
            metadatos['derogado'] = element.attrib['derogado']
        elif element.tag == "{http://www.leychile.cl/esquemas}IdentificacionFuente":
            metadatos['IdentificacionFuente'] = element.text
        elif element.tag == "{http://www.leychile.cl/esquemas}NumeroFuente":
            metadatos['NumeroFuente'] = element.text
        elif element.tag == "{http://www.leychile.cl/esquemas}Identificador":
            metadatos['fechaPromulgacion'] = element.attrib['fechaPromulgacion']
            metadatos['fechaPublicacion'] = element.attrib['fechaPublicacion']
        elif element.tag == "{http://www.leychile.cl/esquemas}Encabezado":
            for subelement in element.iter():
                if subelement.tag == "{http://www.leychile.cl/esquemas}Texto":
                    metadatos['TextoEncabezado'] = subelement.text
        elif element.tag == "{http://www.leychile.cl/esquemas}Promulgacion":
                    for subelement in element.iter():
                        if subelement.tag == "{http://www.leychile.cl/esquemas}Texto":
                            metadatos['firmantes'] = subelement.text

    result = defaultdict(lambda: {'count': 0, 'texts': []})



    return articulos,metadatos


import requests
#url="https://www.leychile.cl/Consulta/obtxml?opt=7&idNorma=1186683"
#url="https://www.leychile.cl/Consulta/obtxml?opt=7&idNorma=1039424"
url="https://www.leychile.cl/Consulta/obtxml?opt=7&idNorma=1026260"
doc_xml=requests.get(url).content.decode()
articulos,metadatos = parse_XML(doc_xml)

#print(articulos[23])
print(metadatos)
