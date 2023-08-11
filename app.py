from articulosNorma import BCNLoader
import sys
from  datos.clavesAPI import openai_api_key, api_key, environment
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain import OpenAI
#from langchain.chains import RetrievalQA
#from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import DirectoryLoader,GoogleDriveLoader,OnlinePDFLoader #pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
from langchain.docstore.document import Document
from langchain.vectorstores import Chroma, Pinecone
from langchain.chains.question_answering import load_qa_chain
import pinecone ##pip install pinecone-client

articulos=BCNLoader("https://www.leychile.cl/Consulta/obtxml?opt=7&idNorma=172986")
# articulos[O] tiene una resumen de la norma en forma de diccionario, 
# del articulos[1:]tiene un diccionaro con 2 elementos, metadata y text. 
# Metadata tiene un diccionario y text el texto del artículo
# ejemplo de la estructura articulos[:2]:
#{"resumen": {"fechaVersion": "2222-02-02", "normaId": "172986", "esTratado": "no tratado", "derogado": "no derogado", "fechaPromulgacion": "2000-05-16", "fechaPublicacion": "2000-05-30", "Tipo": "Decreto con Fuerza de Ley", "numero": "1", "Organismo": "MINISTERIO DE JUSTICIA", "TituloNorma": "FIJA TEXTO REFUNDIDO, COORDINADO Y SISTEMATIZADO DEL CODIGO CIVIL; DE LA LEY N\u00ba4.808, SOBRE REGISTRO CIVIL, DE LA LEY N\u00ba17.344, QUE AUTORIZA CAMBIO DE NOMBRES Y APELLIDOS, DE LA LEY N\u00ba 16.618, LEY DE MENORES, DE LA LEY N\u00ba 14.908, SOBRE ABANDONO DE FAMILIA Y PAGO DE PENSIONES ALIMENTICIAS, Y DE LA LEY N\u00ba16.271, DE IMPUESTO A LAS HERENCIAS, ASIGNACIONES Y DONACIONES", "Materias": "\n                  ", "IdentificacionFuente": "Bolet\u00edn de Leyes y Decretos de Gobierno", "NumeroFuente": "36676", "TextoEncabezado": "FIJA TEXTO REFUNDIDO, COORDINADO Y SISTEMATIZADO DEL CODIGO\nCIVIL; DE LA LEY N\u00ba4.808, SOBRE REGISTRO CIVIL; DE LA LEY\nN\u00ba17.344, QUE AUTORIZA CAMBIO DE NOMBRES Y APELLIDOS; DE LA\nLEY N\u00ba16.618, LEY DE MENORES; DE LA LEY N\u00ba14.908, SOBRE\nABANDONO DE FAMILIA Y PAGO DE PENSIONES ALIMENTICIAS, Y DE\nLA LEY N\u00ba16.271, DE IMPUESTO A LAS HERENCIAS, ASIGNACIONES\nY DONACIONES\n\n     D.F.L. N\u00ba 1.\n\n     Santiago, 16 de mayo del 2000.- Hoy se decret\u00f3 lo que\nsigue:\n\n     Teniendo presente:\n\n     1.- Que el art\u00edculo 8\u00ba de la ley N\u00ba 19.585, facult\u00f3\nal Presidente de la Rep\u00fablica para fijar el texto\nrefundido, coordinado y sistematizado del C\u00f3digo Civil y de\nlas leyes que se modifican expresamente en la presente ley;\ncomo, asimismo, respecto de todos aquellos cuerpos legales\nque contemplen parentescos y categor\u00edas de ascendientes,\nparientes, padres, madres, hijos, descendientes o hermanos\nleg\u00edtimos, naturales e ileg\u00edtimos, para lo cual podr\u00e1\nincorporar las modificaciones y derogaciones de que hayan\nsido objeto tanto expresa como t\u00e1citamente;\n     2.- Que entre las leyes que complementan las\ndisposiciones del C\u00f3digo Civil deben considerarse las\nsiguientes: ley N\u00ba 4.808, sobre Registro Civil; ley N\u00ba\n17.344, que autoriza cambio de nombres y apellidos; ley N\u00ba\n16.618, Ley de Menores; ley N\u00ba 14.908, sobre Abandono de\nFamilia y Pago de Pensiones Alimenticias y la ley N\u00ba\n16.271, de Impuesto a las Herencias, Asignaciones y\nDonaciones;\n     3.- Que asimismo es recomendable por razones de\nordenamiento y de utilidad pr\u00e1ctica, que en los textos\nrefundidos del C\u00f3digo Civil y de las leyes se\u00f1aladas\nprecedentemente, se indique mediante notas al margen el\norigen de las normas que conformar\u00e1n su texto legal; y\nVisto: Lo dispuesto en el art\u00edculo 8\u00ba de la ley N\u00ba\n19.585, dicta el siguiente:\n\n     Decreto con fuerza de ley:", "firmantes": "\n     An\u00f3tese, t\u00f3mese raz\u00f3n, reg\u00edstrese, comun\u00edquese y\npubl\u00edquese.- RICARDO LAGOS ESCOBAR, Presidente de la\nRep\u00fablica.- Jos\u00e9 Antonio G\u00f3mez Urrutia, Ministro de\nJusticia.\n\n     Lo que transcribo para su conocimiento.- Le saluda\natentamente.- Jaime Arellano Quintana, Subsecretario de\nJusticia."}}
#{"metadata": {"numero": "1 ", "titulo": "\u00a0", "transitorio": "no transitorio", "tipoParte": "Art\u00edculo", "fechaVersion": "2000-05-30", "derogado": "no derogado", "idParte": "8717775", "ancestros": []}, "text": "     Art\u00edculo 1\u00ba.- D\u00e9jase sin efecto el D.F.L. N\u00ba 1, de28 de octubre de 1999, del Ministerio de Justicia, tomadoraz\u00f3n por la Contralor\u00eda General de la Rep\u00fablica, sinpublicar."}
#{"metadata": {"numero": "FINAL (DEL ART. 2)", "titulo": "\u00a0", "transitorio": "no transitorio", "tipoParte": "Art\u00edculo", "fechaVersion": "2008-09-15", "derogado": "no derogado", "idParte": "8717776", "ancestros": []}, "text": "     Art\u00edculo final. El presente C\u00f3digo comenzar\u00e1 a regirdesde el 1.\u00ba de enero de 1857, y en esa fecha quedar\u00e1nderogadas, aun en la parte que no fueren contrarias a \u00e9l,las leyes preexistentes sobre todas las materias que en \u00e9lse tratan.     Sin embargo, las leyes preexistentes sobre la prueba delas obligaciones, procedimientos judiciales, confecci\u00f3n deinstrumentos p\u00fablicos y deberes de los ministros de fe,s\u00f3lo se entender\u00e1n derogadas en lo que sean contrarias alas disposiciones de este C\u00f3digo."}
#
#

# Convierte la lista de diccionarios en lista de Document, partiendo del indice 1 en adelante
documentos = []

for articulo in articulos[1:]:
    documento = Document(
        page_content=articulo["text"],
        metadata=articulo["metadata"]
    )
    documentos.append(documento)

resumen=articulos[0]["resumen"] #un diccionario con los tipos de datos


#Para guardar el archivo
#articulos_en_texto = '\n'.join(json.dumps(diccionario) for diccionario in articulos)
#with open('./datos/norma_bajada.txt', 'w') as archivo:
#    archivo.write(articulos_en_texto)

pinecone.init(
    api_key=api_key,  #  ver app.pinecone.io
    environment=environment  
)
index_name = "normas" 
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

#Hace el emabedding y luego carga a la BD.
cargaBD=Pinecone.from_documents(documentos,embedding=embeddings,index_name=index_name)
print(type(busqueda),"\n")



llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
chain=  load_qa_chain(llm, chain_type = "stuff")
query = "que debo hacer si me encuento mucho dinero en una playa"

docs = busqueda.similarity_search(query) #include_metadata=True)
print(docs,"\n+++\n")
respuesta=chain.run(input_documents=docs, question=query)
print(respuesta,"\n")
    
while True:
    query=input("Pregunta:")
    docs = busqueda.similarity_search(query) # include_metadata=True)
    respuesta=chain.run(input_documents=docs, question=query)
    print(respuesta,"\n")


sys.exit()
#print(cortadosPDFs1)
#docsearch = Pinecone(index_name=index_name, read_only=True)

# Realiza una consulta
#query = "Cuantos respaldos de se hacen y de que tipo?"
#docs = docsearch.similarity_search(query)


#docsearch=Pinecone.from_documents(cortadosPDFs1, embedding=embeddings, index_name=index_name)

#Pinecone.from_documents(docs, embedding=embeddings, index_name="langchain-self-retriever-demo")



#docsearch = Pinecone.from_texts([t.page_content for t in cortadosPDFs1], embeddings, index_name=index_name)
#query = "Cual es el tema principal?"
#docs = docsearch.similarity_search(query)
#print(len(docs))
# Here's an example of the first document that was returned
#for doc in docs:
#    print(doc.page_content,"\n0000000000000\n")


#####################################################################3
#### Conculsta Documento resume un documento
####        y luego puedes preguntarle al documento
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
#llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
#########
#*********  Las 2 formas de mas abajo usando como entrada arreglos de documentos (obtenidos de chunks )
###########

#############################
########## PARA RESUMIR   (resumen por map_reduce), si el texto es corto (8k) stuff
#############################
#chain = load_summarize_chain(llm, chain_type="map_reduce", verbose=True)
#resumen=chain.run(cortadosGDOCs1)
#print(type(resumen))
#print(resumen)

############################
############# PARA PREGUNTAR
############################
#query = "Cuantos respaldos de se hacen y de que tipo?"
#chain = load_qa_chain(llm, chain_type="map_reduce",verbose=True)
#respuesta=chain.run(input_documents=cortadosGDOCs1, question=query)
#print(type(respuesta))
#print(respuesta)


###########################
###################### Extraer datos de Youtueb
#################################

from langchain.document_loaders import YoutubeLoader
from langchain.llms import OpenAI
from langchain.chains.summarize import load_summarize_chain
#pip install youtube-transcript-api
#pip install pytube
#loader=YoutubeLoader.from_youtube_url("https://youtu.be/-87U4YLqPlQ", add_video_info=True,language="es")
#loader = YoutubeLoader('SM00cCSN6gg', language="es", add_video_info=True)
#result=loader.load()
#print (f"Found video from {result[0].metadata['author']} that is {result[0].metadata['length']} seconds long")
#print (result)





