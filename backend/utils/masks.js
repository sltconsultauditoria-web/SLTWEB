

export const masks = {

  cnpj: "99.999.999/9999-99",

  cpf: "999.999.999-99",

  cep: "99999-999",

  telefone: "(99) 99999-9999"

}

export function formatMoney(value){

  return new Intl.NumberFormat("pt-BR",{
    style:"currency",
    currency:"BRL"
  }).format(value)

}

export function formatDate(date){

  return new Date(date).toLocaleDateString("pt-BR")

}
