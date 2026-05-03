import os

arquivo = r"C:\Users\admin-local\ServerApp\consultSLTweb\frontend\src\pages\Dashboard.jsx"

novo = r'''
import React, { useEffect, useState } from "react";
import axios from "axios";

export default function Dashboard(){

const [dados,setDados] = useState({
empresas:0,
documentos:0,
guias:0,
usuarios:0,
alertas:0,
obrigacoes:0
})

useEffect(()=>{
 carregar()
},[])

async function carregar(){
 try{
   const res = await axios.get("http://localhost:8000/api/dashboard")
   setDados(res.data)
 }catch(e){
   console.log(e)
 }
}

return (
<div className="p-6">
<h1>Dashboard</h1>

<div className="grid grid-cols-3 gap-4">

<div className="card">Empresas: {dados.empresas}</div>
<div className="card">Documentos: {dados.documentos}</div>
<div className="card">Guias: {dados.guias}</div>
<div className="card">Usuários: {dados.usuarios}</div>
<div className="card">Alertas: {dados.alertas}</div>
<div className="card">Obrigações: {dados.obrigacoes}</div>

</div>
</div>
)
}
'''

open(arquivo,"w",encoding="utf8").write(novo)

print("Dashboard corrigido")