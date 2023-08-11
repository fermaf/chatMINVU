import streamlit as st

st.write("Paz Mundial")
option = st.selectbox(
    'Selecciona la norma',
("DS49","DS01","DS19" ,"DS255",
 "RE 6042 delega faculatdes","Ley 21442 copropiedad",
 "Relamento tipo ley copropiedad","Ley 21180 transformacion digital
 "Ley 19799 firma electronica","Codigo Civil","Constitucion",
 "Baes Generales Admin Estado","Estatuto adminstrativo",
 "Procedimiento adminstrativo",
 "Ley 19886 sobre Contratos Adminstrativos de suministro y prestacion de servicios",
 "Ley 16391, Crea el Ministerio de vivieda","DL 1305, Restructura y regionaliza el Minvu"))

if option=="DS49" :
       idNorma="1039424"
elif option=="DS01" :
    idNorma="1026260"
elif option=="DS19" :
    idNorma="1092547"
elif option=="DS255":
    idNorma= "257828"
elif option=="RE 6042 delega faculatdes":
    idNorma="1103032"
elif option=="Ley 21442 copropiedad:
    dNorma=  "1174663"
elif option=="Relamento tipo ley copropiedad":
    idNorma= "1191159"
elif option=="Ley 21180 transformacion digital":
    idNorma= "1138479"
elif option=="Ley 19799 firma electronica":
    idNorma= "196640"
elif option=="Codigo Civil":
    idNorma="172986"
elif option=="Constitucion":
    idNorma="242302"
elif option=="Baes Generales Admin Estado":
    idNorma= "191865"
elif option=="Estatuto adminstrativo":
    idNorma="236392"
elif option=="Procedimiento adminstrativo":
    idNorma="210676"
elif option=="Ley 19886 sobre Contratos Adminstrativos de suministro y prestacion de servicios":
    idNorma="213004"
elif option=="Ley 16391, Crea el Ministerio de vivieda":
    idNorma="28433"
elif option=="DL 1305, Restructura y regionaliza el Minvu":
    idNorma="6564"


st.write('You selected:', option)