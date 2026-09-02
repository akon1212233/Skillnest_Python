function mostrar(id){

  let pantallas = document.querySelectorAll(".pantalla");

  pantallas.forEach(pantalla => {
    pantalla.classList.remove("active");
  });

  document.getElementById(id).classList.add("active");
}