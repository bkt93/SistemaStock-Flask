//Funcionalidades barra desplegable
const cloud = document.getElementById("cloud");
const barraLateral = document.querySelector(".barra-lateral")

cloud.addEventListener("click", ()=>{
    barraLateral.classList.toggle("mini-barra-lateral");
})
  