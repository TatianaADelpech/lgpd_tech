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

pasta_raiz = pathlib.Path(".").absolute()

for pdf in pdfs :
    if pdf != None :
        with open(pasta_raiz / pdf.name, "wb") as f:
            f.write(pdf.getbuffer())
        processo_txt = pdf.name.replace("pdf", "txt")
        arquivo_processo_txt = pasta_raiz / processo_txt
        if not arquivo_processo_txt.exists():
            parsed = parser.from_file(str(pasta_raiz / pdf.name))
            with open(arquivo_processo_txt, "w", encoding="utf_8") as f:
                f.write(parsed["content"])

        with open(arquivo_processo_txt, "r", encoding="utf_8") as f:
            processo = f.read()

        padrao1_cpf = "\d{3}\.\d{3}\.\d{3}-\d{2}"
        cpfs_encontrados = re.findall(padrao1_cpf, processo)
        contagem_cpfs = Counter(cpfs_encontrados)

        st.markdown(f"##### nome do arquivo: {pdf.name}")
        st.text(f"Foram encontrados {len(contagem_cpfs)} CPF(s) diferente(s).")

        for cpf, contagem in contagem_cpfs.items() :
            st.text(f"cpf:{aplica_mascara(cpf)} aparece {contagem} vez(es)")

if pdfs : 
    st.markdown("**É necessário esse(s) CPF(s) estar(em) exposto(s) dessa maneira?**")
    st.markdown("**Observação: Os CPFs estão mascarados por questão de segurança, no entanto estão expostos nos processos.**")



    