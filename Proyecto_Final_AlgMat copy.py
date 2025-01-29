import pygame
import sys
import numpy as np
import random
import json

pygame.init()

# Pantalla
LARGO, ANCHO = 800, 600
pantalla = pygame.display.set_mode((LARGO, ANCHO))
pygame.display.set_caption("CATMATH")
WHITE = (0, 0, 0)

# Fuentes
fondo = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

# Imágenes para los assets
imagen_player = pygame.image.load("player.png")
imagen_player = pygame.transform.scale(imagen_player, (70, 100))

imagen_pc = pygame.image.load("pc.png")
imagen_pc = pygame.transform.scale(imagen_pc, (130, 80))

imagen_fondo = pygame.image.load("fondo.png")
imagen_fondo = pygame.transform.scale(imagen_fondo, (LARGO, ANCHO))

imagen_corazon = pygame.image.load("vidas.png")
imagen_corazon = pygame.transform.scale(imagen_corazon, (70, 70))

# Propiedades Jugador
player_pos = np.array([200, 500])
player_velocidad = 5

# PC (Puertas)
pc = [
    pygame.Rect(100, 355, 50, 100),
    pygame.Rect(320, 350, 50, 100),
    pygame.Rect(535, 350, 50, 100),
    pygame.Rect(320, 250, 50, 100)
]

# Cargar las preguntas desde preguntas.json
try:
    with open("preguntas.json", "r", encoding="utf-8") as file:
        todas_preguntas = json.load(file)
except FileNotFoundError:
    print("Error: No se encontró el archivo 'preguntas.json'.")
    sys.exit()
except json.JSONDecodeError:
    print("Error: El archivo 'preguntas.json' tiene un formato inválido.")
    sys.exit()

# Estado del juego
vidas = 3
pregunta_actual = None
pc_actual = 0
juego_activo = False  # Inicialmente el juego no está activo

# Selección de preguntas (se inicializa en cada reinicio)
preguntas = []

# Función para inicializar el juego
def inicializar_juego():
    global vidas, preguntas, pregunta_actual, pc_actual, juego_activo
    vidas = 3
    pc_actual = 0
    juego_activo = True
    pregunta_actual = None
    # Seleccionar preguntas aleatorias
    preguntas = random.sample(todas_preguntas, len(pc))  # Selecciona tantas preguntas como puertas

# Función para mostrar texto en pantalla
def dibujar_texto(text, x, y, color=(255, 255, 255)):
    # Dividir el texto por saltos de línea (\n)
    lineas = text.split('\n')
    for i, linea in enumerate(lineas):
        # Renderizar cada línea y dibujarla en la pantalla
        texto_renderizado = fondo.render(linea, True, color)
        pantalla.blit(texto_renderizado, (x, y + i * 30))  # Ajusta el desplazamiento de cada línea

# Función para mover al jugador utilizando principios matriciales
def mover_player(direction):
    global player_pos
    matriz_de_movimiento = {
        "UP": np.array([0, -player_velocidad]),
        "DOWN": np.array([0, player_velocidad]),
        "LEFT": np.array([-player_velocidad, 0]),
        "RIGHT": np.array([player_velocidad, 0])
    }
    player_pos += matriz_de_movimiento.get(direction, np.array([0, 0]))
    # Limitar el movimiento dentro de los bordes de la pantalla
    player_pos[0] = np.clip(player_pos[0], 0, LARGO - imagen_player.get_width())
    player_pos[1] = np.clip(player_pos[1], 0, ANCHO - imagen_player.get_height())

# Bucle principal del juego
while True:
    pantalla.fill(WHITE)
    
    # Si el juego no ha comenzado, mostrar el mensaje "HOLA"
    if not juego_activo:
        mensaje_rect = pygame.Rect(50, 250, LARGO - 100, 100)  # Ajusta el tamaño y la posición del fondo negro
        pygame.draw.rect(pantalla, (0, 0, 0), mensaje_rect)  # Fondo negro
        dibujar_texto("HOLA", LARGO // 2 - 50, ANCHO // 2)  # Mostrar el mensaje "HOLA"
        pygame.display.flip()

        # Esperar 10 segundos antes de comenzar el juego
        pygame.time.wait(10000)  # Espera de 10 segundos
        juego_activo = True  # Después de 10 segundos, el juego comienza

    else:
        # El código del juego sigue aquí (como el código que ya tienes para mover al jugador, colisiones, preguntas, etc.)

        # Dibujar el fondo
        pantalla.blit(imagen_fondo, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Manejo de preguntas y respuestas
            if pregunta_actual and event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                    if event.key == pygame.K_1 and pregunta_actual["options"][0] == pregunta_actual["answer"]:
                        pregunta_actual = None
                        pc_actual += 1
                        if pc_actual < len(pc):  # Si hay más puertas, activa el siguiente cuestionario
                            juego_activo = False
                    elif event.key == pygame.K_2 and pregunta_actual["options"][1] == pregunta_actual["answer"]:
                        pregunta_actual = None
                        pc_actual += 1
                        if pc_actual < len(pc):
                            juego_activo = False
                    elif event.key == pygame.K_3 and pregunta_actual["options"][2] == pregunta_actual["answer"]:
                        pregunta_actual = None
                        pc_actual += 1
                        if pc_actual < len(pc):
                            juego_activo = False
                    else:
                        # Respuesta incorrecta, perder una vida
                        vidas -= 1
                        if vidas == 0:
                            pantalla.fill(WHITE)
                            dibujar_texto("GAME OVER", LARGO // 2 - 100, ANCHO // 2, (255, 0, 0))
                            pygame.display.flip()
                            pygame.time.wait(2000)
                            pygame.quit()
                            sys.exit()

        # Movimiento del jugador
        keys = pygame.key.get_pressed()
        if juego_activo:
            if keys[pygame.K_UP]:
                mover_player("UP")
            if keys[pygame.K_DOWN]:
                mover_player("DOWN")
            if keys[pygame.K_LEFT]:
                mover_player("LEFT")
            if keys[pygame.K_RIGHT]:
                mover_player("RIGHT")

        # Detector de colisiones con pcs
        player_rect = pygame.Rect(player_pos[0], player_pos[1], imagen_player.get_width(), imagen_player.get_height())
        if juego_activo and pc_actual < len(pc):
            if player_rect.colliderect(pc[pc_actual]):
                pregunta_actual = preguntas[pc_actual]
                juego_activo = False  # El juego se pone en pausa para que se responda la pregunta

        # Dibujar jugador y pc
        pantalla.blit(imagen_player, player_pos)
        for i, door in enumerate(pc):
            if i >= pc_actual:  # Solo dibujar las puertas que no han sido "desactivadas"
                pantalla.blit(imagen_pc, door.topleft)

        # Dibujar vidas
        for i in range(vidas):
            pantalla.blit(imagen_corazon, (340 + i * 40, 157))

        # Mostrar pregunta
        if pregunta_actual:
            pregunta_rect = pygame.Rect(70, 220, LARGO - 140, 150)  # Ajusta el tamaño y la posición según sea necesario
            pygame.draw.rect(pantalla, (0, 0, 0), pregunta_rect)
            dibujar_texto(pregunta_actual["pregunta"], 75, 230)
            for i, option in enumerate(pregunta_actual["options"]):
                dibujar_texto(f"{i + 1}. {option}", 75, 260 + i * 40)

        # Dibujar un fondo negro detrás del mensaje
        if pc_actual >= len(pc):
            mensaje_rect = pygame.Rect(50, 250, LARGO - 100, 100)  # Ajusta el tamaño y posición del fondo negro
            pygame.draw.rect(pantalla, (0, 0, 0), mensaje_rect)  # Fondo negro
            dibujar_texto("¡Felicidades, Lograste desactivar la IA y salvar a la PUCE!", 50, 300)  # Mostrar el mensaje sobre el fondo
            pygame.display.flip()
            pygame.time.wait(2000)  # Pausa de 2 segundos antes de salir o reiniciar
            inicializar_juego()  # Reiniciar el juego al final

    pygame.display.flip()
    clock.tick(30)
