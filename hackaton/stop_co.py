import pygame, random, sys

pygame.init()
pygame.mixer.init()  # inicializar mixer
pygame.mixer.music.load("musica-juego.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)  # música en bucle

# Inicialización
pygame.init()
ANCHO, ALTO = 600, 400
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Stop CO Challenge")
reloj = pygame.time.Clock()
fuente = pygame.font.Font(None, 40)
fuente_titulo = pygame.font.Font(None, 70)

# Función para mostrar texto centrado
def mostrar_texto(texto, fuente, color, y):
    render = fuente.render(texto, True, color)
    rect = render.get_rect(center=(ANCHO // 2, y))
    pantalla.blit(render, rect)

# Pantalla de inicio
def pantalla_inicio():
    en_inicio = True
    while en_inicio:
        pantalla.fill((180, 220, 255))  # cielo celeste
        mostrar_texto("Stop CO Challenge", fuente_titulo, (0, 100, 0), 120)
        mostrar_texto("Mové el auto con flechas (<),(>)", fuente, (0, 0, 0), 200)
        mostrar_texto("Evita el humo y sumá puntos", fuente, (0, 0, 0), 250)
        mostrar_texto("Presioná ESPACIO para comenzar", fuente, (0, 100, 0), 320)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                en_inicio = False

        pygame.display.flip()
        reloj.tick(30)

# Pantalla de Game Over
def pantalla_game_over(puntos):
    en_final = True
    while en_final:
        pantalla.fill((255, 180, 180))
        mostrar_texto("GAME OVER", fuente_titulo, (150, 0, 0), 120)
        mostrar_texto(f"Puntos: {puntos}", fuente, (0, 0, 0), 200)
        mostrar_texto("Presioná R para reiniciar o ESC para salir", fuente, (50, 50, 50), 280)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                    juego()
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        reloj.tick(30)

# Pantalla de Victoria
def pantalla_victoria(puntos):
    en_victoria = True
    while en_victoria:
        pantalla.fill((180, 255, 180))
        mostrar_texto("¡Ganaste!", fuente_titulo, (0, 150, 0), 120)
        mostrar_texto(f"Puntos: {puntos}", fuente, (0, 0, 0), 200)
        mostrar_texto("Presioná R para jugar otra vez o ESC para salir", fuente, (0, 80, 0), 280)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                    juego()
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        reloj.tick(30)

# Juego principal
def juego():
    auto = pygame.Rect(275, 350, 50, 30)
    humo = pygame.Rect(random.randint(0, ANCHO - 20), 0, 20, 20)
    puntos = 0
    meta = 10
    velocidad_humo = 5

    corriendo = True
    while corriendo:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Movimiento del auto
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]: auto.x -= 5
        if teclas[pygame.K_RIGHT]: auto.x += 5

        # Mantener dentro de pantalla
        auto.x = max(0, min(auto.x, ANCHO - auto.width))

        # Movimiento del humo
        humo.y += velocidad_humo
        if humo.y > ALTO:
            humo.y = 0
            humo.x = random.randint(0, ANCHO - humo.width)
            puntos += 1
            if puntos >= meta:
                pantalla_victoria(puntos)

        # Colisión
        if auto.colliderect(humo):
            print("¡Contaminación detectada!")
            pantalla_game_over(puntos)

        # Dibujar
        pantalla.fill((180, 220, 255))  # fondo celeste
        pygame.draw.rect(pantalla, (0, 255, 0), auto)  # auto verde
        pygame.draw.rect(pantalla, (80, 80, 80), humo)  # humo gris

        # Mostrar puntaje
        texto = fuente.render(f"Puntos: {puntos}", True, (0, 0, 0))
        pantalla.blit(texto, (10, 10))

        pygame.display.flip()
        reloj.tick(30)

# Iniciar juego
pantalla_inicio()
juego()
