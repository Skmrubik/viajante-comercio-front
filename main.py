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
                pygame.draw.circle(WIN, (255, 0, 0), (row, col), 5)
                pygame.display.update()
                print(ciudades)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    url = "http://localhost:8080/ciudades"

                    response = requests.get(url, params={"ciudades": ciudades})

    pygame.quit()

main()