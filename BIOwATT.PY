import flet as ft
import requests
import json

def main(page: ft.Page):
    # Función para cambiar entre modo claro y oscuro y actualizar el icono
    page.theme_mode = "light"
    
    def toggle_theme(e):
        if e.control.value:  # Modo oscuro
            page.theme_mode = ft.ThemeMode.DARK
            icon_tema.name = "brightness_2"  # Luna
        else:  # Modo claro
            page.theme_mode = ft.ThemeMode.LIGHT
            icon_tema.name = "brightness_5"  # Sol
        page.update()  # Actualiza la página para aplicar el nuevo tema

    # Definir los temas claro y oscuro
    light_theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=ft.colors.BLACK,
            on_primary=ft.colors.WHITE,
            background=ft.colors.WHITE,
            on_background=ft.colors.BLACK
        )
    )

    dark_theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=ft.colors.GREEN,
            on_primary=ft.colors.BLACK,
            background=ft.colors.BLACK,
            on_background=ft.colors.GREEN
        )
    )

    # Funciones de cálculo
    def calcular_pbra(ac, rhc, irec):
        return ac * rhc * irec

    def calcular_irec(rpc, rsc, cc):
        rcs = rpc + rsc
        return rcs / cc

    def calcular_pteeb(pbra, ce):
        return pbra * ce

    # Función para guardar datos en Firebase
    def guardar_datos_en_firebase(data):
        url = "https://biowatt-22684-default-rtdb.firebaseio.com/resultados.json"  # URL para enviar datos
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("Datos guardados correctamente.")
        else:
            print(f"Error al guardar datos: {response.text}")

    # Función para manejar el botón "Calcular"
    def on_calcular_click(e):
        ac = float(texto1.value)  # Área cultivada (Ha)
        rhc = float(texto2.value)  # Rendimiento por hectárea cultivada (Ton/Ha)
        rpc = 10.0  # Valor de ejemplo para Residuos Primarios del Cultivo
        rsc = 5.0  # Valor de ejemplo para Residuos Secundarios del Cultivo
        cc = 100.0  # Valor de ejemplo para Cultivo Cosechado (Kg)
        ce = slider1.value  # Contenido Energético (obtenido del slider)

        # Calcular IReC
        irec = calcular_irec(rpc, rsc, cc)

        # Calcular PBRA
        pbra = calcular_pbra(ac, rhc, irec)

        # Calcular PTeEB
        pteeb = calcular_pteeb(pbra, ce)

        # Mostrar el resultado en el recuadro de resultado
        recuadro_resultado.content.value = f"Resultado PTeEB: {pteeb:.2f} MJ"
        page.update()

        # Crear un diccionario con los datos a enviar
        datos_a_guardar = {
            "area_cultivada": ac,
            "rendimiento_hectarea": rhc,
            "contenido_energetico": ce,
            "pbra": pbra,
            "pteeb": pteeb
        }

        # Llamar a la función para guardar los datos en Firebase
        guardar_datos_en_firebase(datos_a_guardar)

    # Función para limpiar los campos y sliders
    def on_limpiar_click(e):
        texto1.value = ""  # Limpiar campo de área cultivada
        texto2.value = "0"  # Limpiar campo de rendimiento por hectárea
        texto2.read_only = False  # Desbloquear el campo de rendimiento por hectárea
        slider1.value = 0  # Restablecer slider1 a 0
        slider2.value = 0  # Restablecer slider2 a 0
        cultivos.value = None  # Limpiar el Dropdown
        recuadro_resultado.content.value = "Resultado"  # Restablecer recuadro de resultados
        porcentaje_slider1.value = "0%"  # Limpiar porcentaje slider1
        porcentaje_slider2.value = "0%"  # Limpiar porcentaje slider2
        page.update()  # Actualizar la página para aplicar los cambios

    # Actualizar el label del slider dinámicamente
    def actualizar_slider1(e):
        porcentaje_slider1.value = f"{int(e.control.value)}%"  # Actualizar el porcentaje
        page.update()

    def actualizar_slider2(e):
        porcentaje_slider2.value = f"{int(e.control.value)}%"  # Actualizar el porcentaje
        page.update()

    # Actualizar datos al seleccionar un cultivo
    def on_cultivo_change(e):
        cultivo_seleccionado = e.control.value
        
        # Valores de ejemplo para cada cultivo
        datos_cultivos = {
            "Caña de azúcar": {"rhc": 80, "irec": 0.2},  # Valores para Caña de azúcar
            "Plátano": {"rhc": 35, "irec": 0.15},        # Valores para Plátano
            "Cacao": {"rhc": 30, "irec": 0.1},           # Valores para Cacao
            "Aceite de palma": {"rhc": 25, "irec": 0.25},  # Valores para Aceite de palma
        }

        # Obtener los valores del cultivo seleccionado
        if cultivo_seleccionado in datos_cultivos:
            rhc = datos_cultivos[cultivo_seleccionado]["rhc"]
            irec = datos_cultivos[cultivo_seleccionado]["irec"]

            # Actualizar el campo de rendimiento por hectárea y bloquearlo
            texto2.value = str(rhc)  # Rendimiento por hectárea
            texto2.read_only = True  # Deshabilitar para que no pueda ser modificado
            page.update()  # Actualizar la página para aplicar los cambios

    # Título principal: "BIO" en verde y "WATT" en negro, juntos
    title_biowatt = ft.Row([
        ft.Text("BIO", size=30, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN),
        ft.Text("WATT", size=30, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK)
    ])

    # Eslogan
    slogan = ft.Text("Potencia verde, futuro brillante")

    # Autocomplete para cultivos con texto negro en modo claro
    cultivos = ft.Dropdown(
        label="Cultivo",
        options=[
            ft.dropdown.Option("Caña de azúcar"),
            ft.dropdown.Option("Plátano"),
            ft.dropdown.Option("Cacao"),
            ft.dropdown.Option("Aceite de palma")
        ],
        on_change=on_cultivo_change  # Asociar función al cambio de selección
    )

    # Textos para introducir datos
    texto1 = ft.TextField(label="Área cultivada (Ha)")
    texto2 = ft.TextField(label="Rendimiento por hectárea (Ton/Ha)", value="0")  # Inicializar con valor 0

    # Sliders con color verde
    slider1 = ft.Slider(
        label="Contenido Energético: 0%",
        value=0,
        min=0,
        max=100,
        divisions=100,
        on_change=actualizar_slider1
    )

    slider2 = ft.Slider(
        label="Porcentaje aproximado 2: 0%",
        value=0,
        min=0,
        max=100,
        divisions=100,
        on_change=actualizar_slider2
    )

    # Porcentajes al lado de cada slider
    porcentaje_slider1 = ft.Text("0%", size=16)
    porcentaje_slider2 = ft.Text("0%", size=16)

    # Recuadro blanco para resultado, centrado y grande
    recuadro_resultado = ft.Container(
        content=ft.Text("Resultado", size=40, color=ft.colors.GREEN),  # Aumentar tamaño de letra
        bgcolor=ft.colors.WHITE,
        padding=10,
        border_radius=10,  # Bordes redondeados
        alignment=ft.alignment.center,  # Centrar el contenido
        expand=True  # Ocupa el espacio disponible
    )

    # Botones en color verde
    boton_limpiar = ft.ElevatedButton(text="Limpiar", style=ft.ButtonStyle(bgcolor=ft.colors.GREEN, color=ft.colors.WHITE), on_click=on_limpiar_click)
    boton_guardar = ft.ElevatedButton(text="Guardar", style=ft.ButtonStyle(bgcolor=ft.colors.GREEN, color=ft.colors.WHITE), on_click=on_calcular_click)
    boton_calcular = ft.ElevatedButton(text="Calcular", style=ft.ButtonStyle(bgcolor=ft.colors.GREEN, color=ft.colors.WHITE), on_click=on_calcular_click)

    # Icono de luna/sol
    icon_tema = ft.Icon(name="brightness_5", color=ft.colors.YELLOW)  # Sol por defecto (modo claro)

    # Contenido de la página
    page.add(
        ft.Column(
            [
                title_biowatt,
                slogan,
                cultivos,
                texto1,
                texto2,
                slider1,
                porcentaje_slider1,
                slider2,
                porcentaje_slider2,
                recuadro_resultado,
                boton_calcular,
                boton_guardar,
                boton_limpiar,
                ft.Row([icon_tema, ft.Switch(label="Modo Oscuro", value=False, on_change=toggle_theme)])  # Switch para cambiar entre modos
            ],
            alignment=ft.MainAxisAlignment.CENTER,  # Centrar elementos
            horizontal_alignment=ft.CrossAxisAlignment.CENTER  # Alinear horizontalmente
        )
    )

# Ejecutar la aplicación
ft.app(target=main, view=ft.AppView.WEB_BROWSER)