import pygame
import requests
import threading # 1. Importar hilos

FPS = 60
ciudades = []
secuencia_recibida = None  # Variable global para guardar el resultado

WIN = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Viajante del comercio')

def get_row_col_from_mouse(pos):
    x, y = pos
    return x, y

# 2. Función que se ejecutará en segundo plano
def peticion_asincrona(url, lista_ciudades):
    global secuencia_recibida
    try:
        response = requests.get(url, params={"ciudades": lista_ciudades})
        secuencia_recibida = response.json() # Guardamos el resultado al terminar
    except Exception as e:
        print(f"Error: {e}")

def main():
    global secuencia_recibida
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                ciudades.append([row,col])
                pygame.draw.circle(WIN, (255, 255, 255), (row, col), 12)
                pygame.draw.circle(WIN, (255, 0, 0), (row, col), 10)
                pygame.display.update()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    url = "http://localhost:8080/ciudades"
                    # 3. LANZAR EL HILO (Esto no bloquea la ventana)
                    hilo = threading.Thread(target=peticion_asincrona, args=(url, ciudades))
                    hilo.start()
                    print("Calculando ruta en segundo plano...")

        # 4. REVISAR SI LLEGÓ LA RESPUESTA
        if secuencia_recibida is not None:
            secuencia = secuencia_recibida
            secuencia_recibida = None # Limpiamos para que no entre mil veces
            
            # --- Tu lógica de dibujo original ---
            coordenadas_inicio = ciudades[secuencia[0]]
            coordenadas_final = ciudades[secuencia[-1]]
            pygame.draw.line(WIN, (255, 255, 255), (coordenadas_inicio[0], coordenadas_inicio[1]), (coordenadas_final[0], coordenadas_final[1]), 9)
            
            for i, ciudad in enumerate(secuencia):
                if i < len(secuencia)-1:
                    coordenadas_uno = ciudades[secuencia[i]]
                    coordenadas_dos = ciudades[secuencia[i+1]]
                    pygame.draw.line(WIN, (255, 255, 255), (coordenadas_uno[0], coordenadas_uno[1]), (coordenadas_dos[0], coordenadas_dos[1]), 9)
            
            for ciudad in ciudades:
                pygame.draw.circle(WIN, (255, 255, 255), (ciudad[0], ciudad[1]), 12)
                pygame.draw.circle(WIN, (255, 0, 0), (ciudad[0], ciudad[1]), 10)
            
            pygame.display.update()

    pygame.quit()

main()