let next = document.querySelector('.next')
let prev = document.querySelector('.prev')

next.addEventListener('click', function(){
    let items = document.querySelectorAll('.item')
    document.querySelector('.slide').appendChild(items[0])
})

prev.addEventListener('click', function(){
    let items = document.querySelectorAll('.item')
    document.querySelector('.slide').prepend(items[items.length - 1])
})

// Función para avanzar automáticamente cada 4 segundos
function autoAdvance() {
    next.click();  // Simula el clic en el botón "next"
}

// Configura el intervalo para que se ejecute cada 4 segundos (4000 ms)
setInterval(autoAdvance, 6000);