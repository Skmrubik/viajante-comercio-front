import pygame
import requests

FPS = 60

ciudades = []
#WIN = window
WIN = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Viajante del comercio')

def get_row_col_from_mouse(pos):
    x, y = pos
    return x, y

def main():
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
                print(ciudades)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    url = "http://localhost:8080/ciudades"

                    response = requests.get(url, params={"ciudades": ciudades})
                    print(response.json())
                    secuencia = response.json()
                    coordenadas_inicio = ciudades[secuencia[0]]
                    coordenadas_final = ciudades[secuencia[len(secuencia)-1]]
                    pygame.draw.line(WIN, (255, 255, 255), (coordenadas_inicio[0], coordenadas_inicio[1]), (coordenadas_final[0], coordenadas_final[1]), 9)
                    for i, ciudad in enumerate(secuencia):
                        if i < len(secuencia)-1:
                            coordenadas_uno = ciudades[secuencia[i]]
                            coordenadas_dos = ciudades[secuencia[i+1]]
                            print(str(coordenadas_uno)+' '+str(coordenadas_dos))
                            pygame.draw.line(WIN, (255, 255, 255), (coordenadas_uno[0], coordenadas_uno[1]), (coordenadas_dos[0], coordenadas_dos[1]), 9)
                    for i, ciudad in enumerate(ciudades):
                        pygame.draw.circle(WIN, (255, 255, 255), (ciudad[0], ciudad[1]), 12)
                        pygame.draw.circle(WIN, (255, 0, 0), (ciudad[0], ciudad[1]), 10)
                    pygame.display.update()

    pygame.quit()

main()