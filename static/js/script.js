document.addEventListener('DOMContentLoaded', () => {

    /* FUNCIONALIDAD PARA PRODUCTOS (Guardar datos + Efecto) */
    const botonesCompra = document.querySelectorAll('.btn-buy, .btn-comprar');

    if (botonesCompra.length > 0) {
        botonesCompra.forEach(boton => {
            boton.addEventListener('click', (e) => {
                e.preventDefault();
                
                const tarjeta = boton.closest('.product-card') || boton.closest('.slide-caption');
                let nombreProducto = "Producto Genérico";
                let precioProducto = "S/ 0.00";

                if (tarjeta) {
                    const tituloEl = tarjeta.querySelector('h3');
                    const precioEl = tarjeta.querySelector('.price');
                    
                    if (tituloEl) nombreProducto = tituloEl.innerText;
                    if (precioEl) {
                        precioProducto = precioEl.innerText;
                    } else {
                        precioProducto = "S/ 99.90"; 
                    }
                }

                localStorage.setItem('compraNombre', nombreProducto);
                localStorage.setItem('compraPrecio', precioProducto);

                const textoOriginal = boton.innerText;
                const urlDestino = boton.getAttribute('href');

                boton.innerText = "¡Añadido!";
                boton.style.backgroundColor = "#28a745"; 
                boton.style.transform = "scale(1.1)";

                setTimeout(() => {
                    window.location.href = urlDestino;
                }, 800);
            });
        });
    }

    /* LÓGICA DE LA PÁGINA DE PAGO (Cargar datos) */

    const resumenNombre = document.getElementById('resumen-nombre');
    const resumenPrecio = document.getElementById('resumen-precio');
    const resumenTotal = document.getElementById('resumen-total');

    if (resumenNombre && resumenPrecio && resumenTotal) {
        const nombreGuardado = localStorage.getItem('compraNombre');
        const precioGuardado = localStorage.getItem('compraPrecio');

        if (nombreGuardado && precioGuardado) {
            resumenNombre.innerText = nombreGuardado;
            resumenPrecio.innerText = precioGuardado;
            resumenTotal.innerText = precioGuardado;
        }
    }

    /* VALIDACIÓN FORMULARIO CONTACTO */
    const formContacto = document.querySelector('.contact-form');
    if (formContacto) {
        formContacto.addEventListener('submit', function(e) {
            e.preventDefault();
            const nombre = document.getElementById('nombre').value.trim();
            const email = document.getElementById('email').value.trim();
            
            if (nombre === "" || email === "") {
                alert("Completa los campos requeridos.");
                return;
            }
            alert(`¡Gracias ${nombre}! Mensaje enviado.`);
            this.reset();
        });
    }

    /* SIMULACIÓN DE PAGO FINAL */
    const botonPagar = document.querySelector('.btn-pay');
    if (botonPagar) {
        const formPago = botonPagar.closest('form');
        formPago.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const inputs = formPago.querySelectorAll('input');
            let valido = true;
            inputs.forEach(input => {
                if(input.value.trim() === '') {
                    valido = false;
                    input.style.border = "2px solid red";
                } else {
                    input.style.border = "1px solid #ddd";
                }
            });

            if (!valido) {
                alert("Por favor completa los datos de envío y tarjeta.");
            } else {
                botonPagar.innerText = "Procesando...";
                botonPagar.disabled = true;
                setTimeout(() => {
                    alert("¡Pago Exitoso! Gracias por tu compra.");
                    localStorage.clear();
                    botonPagar.disabled = false;
                    formPago.submit(); 
                }, 2000);
            }
        });
    }
});
