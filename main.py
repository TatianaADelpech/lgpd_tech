"""PROJETO PRINCÍPIO DA NECESSIDADE LGPD - CPF EM PROCESSOS JUDICIAIS"""

from collections import Counter
import pathlib
import re

import streamlit as st
from tika import parser

def aplica_mascara(recebe_cpf):
   return(recebe_cpf[:3]+".***.***-"+recebe_cpf[-2:])

st.markdown("# PROJETO PRINCÍPIO DA NECESSIDADE LGPD - CPF EM PROCESSOS JUDICIAIS ")
pdfs = st.file_uploader(
    label='Faça o upload dos pdfs (200M por arquivo) dos processos a serem analisados',
    type= 'pdf',
    accept_multiple_files=True)

pasta_raiz = pathlib.Path(".")

for pdf in pdfs :
    if pdf != None :
        txt = pdf.name.replace("pdf", "txt")
        file = pasta_raiz / txt
        if not file.exists():
            parsed = parser.from_file(pasta_raiz / pdf.name)
            with open(file, "w", encoding="utf_8") as f:
                f.write(parsed["content"])

        with open(file, "r", encoding="utf_8") as f:
            str_lawsuit = f.read()

        padrao1_cpf = "\d{3}\.\d{3}\.\d{3}-\d{2}"
        lista_padrao1 = re.findall(padrao1_cpf, str_lawsuit)
        contagem_cpfs = Counter(lista_padrao1)

        st.markdown(f"##### nome do arquivo: {pdf.name}")
        st.text(f"Foram encontrados {len(contagem_cpfs)} CPF(s) diferente(s).")

        for cpf, contagem in contagem_cpfs.items() :
            st.text(f"cpf:{aplica_mascara(cpf)} aparece {contagem} vez(es)")

if pdfs : 
    st.markdown("**É necessário esse(s) CPF(s) estar(em) exposto(s) dessa maneira?**")
    st.markdown("**Observação: Os CPFs estão mascarados por questão de segurança, no entanto estão expostos nos processos.**")



    