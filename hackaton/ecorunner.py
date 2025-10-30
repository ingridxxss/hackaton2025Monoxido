import pygame, random, sys

# Inicialización
pygame.init()
ANCHO, ALTO = 800, 400
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("EcoRunner")
reloj = pygame.time.Clock()
fuente = pygame.font.Font(None, 40)
fuente_titulo = pygame.font.Font(None, 70)

# === IMÁGENES ===
# Cargá tus imágenes (asegurate de que estén en la misma carpeta del juego)
fondo_img = pygame.image.load("fondo.jpg").convert()
fondo_img = pygame.transform.scale(fondo_img, (ANCHO, ALTO))

obstaculo_img = pygame.image.load("contaminante.png").convert_alpha()
obstaculo_img = pygame.transform.scale(obstaculo_img, (30, 30))

# Imagen del jugador
jugador_img = pygame.image.load("personaje.webp").convert_alpha()
jugador_img = pygame.transform.scale(jugador_img, (40, 40))

# Función para mostrar texto centrado
def mostrar_texto(texto, fuente, color, y):
    render = fuente.render(texto, True, color)
    rect = render.get_rect(center=(ANCHO // 2, y))
    pantalla.blit(render, rect)

# Pantalla de inicio
def pantalla_inicio():
    en_inicio = True
    while en_inicio:
        pantalla.fill((180, 255, 180))
        mostrar_texto("Cuidamos el ambiente", fuente_titulo, (0, 100, 0), 120)
        mostrar_texto("Ayuda al planeta esquivando la contaminación", fuente, (0, 0, 0), 200)
        mostrar_texto("Usa ESPACIO o FLECHA ARRIBA para saltar obstáculos.", fuente, (0, 0, 0), 260)
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
def pantalla_game_over(puntaje, nivel):
    en_game_over = True
    while en_game_over:
        pantalla.fill((255, 200, 200))
        mostrar_texto("GAME OVER", fuente_titulo, (150, 0, 0), 120)
        mostrar_texto(f"Puntaje final: {puntaje}", fuente, (0, 0, 0), 200)
        mostrar_texto(f"Nivel alcanzado: {nivel}", fuente, (0, 0, 0), 240)
        mostrar_texto("Presioná R para reiniciar o ESC para salir", fuente, (50, 50, 50), 300)

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
    jugador = pygame.Rect(100, 300, 40, 40)
    salto = False
    velocidad_salto = 0
    obstaculos = []
    puntos = 0
    vidas = 3

    # Niveles
    nivel = 1
    velocidad_obstaculo = 8
    puntos_para_subir_nivel = 10

    corriendo = True
    while corriendo:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN and not salto:
                if e.key in [pygame.K_SPACE, pygame.K_UP]:
                    salto = True
                    velocidad_salto = -15

        # Movimiento del salto
        if salto:
            jugador.y += velocidad_salto
            velocidad_salto += 1
            if jugador.y >= 300:
                jugador.y = 300
                salto = False

        # Generar obstáculos aleatorios
        if random.randint(1, 40) == 1:
            obstaculos.append(pygame.Rect(ANCHO, 320, 20, 30))

        # Mover obstáculos y detectar colisiones
        for o in list(obstaculos):
            o.x -= velocidad_obstaculo
            if o.x < 0:
                obstaculos.remove(o)
                puntos += 1

            if jugador.colliderect(o):
                vidas -= 1
                obstaculos.remove(o)
                if vidas <= 0:
                    pantalla_game_over(puntos, nivel)

        # Subir de nivel
        if puntos > 0 and puntos % puntos_para_subir_nivel == 0:
            nivel = puntos // puntos_para_subir_nivel + 1
            velocidad_obstaculo = 8 + nivel * 2

        # Dibujar fondo y elementos
        pantalla.blit(fondo_img, (0, 0))  # Fondo con imagen
        pantalla.blit(jugador_img, jugador)  # Jugador con imagen

        # Obstáculos de basura
        for o in obstaculos:
            pantalla.blit(obstaculo_img, o)

        # Mostrar puntos, vidas y nivel
        pantalla.blit(fuente.render(f"Puntos: {puntos}", True, (0,0,0)), (10,10))
        pantalla.blit(fuente.render(f"Vidas: {vidas}", True, (0,0,0)), (10,50))
        pantalla.blit(fuente.render(f"Nivel: {nivel}", True, (0,0,0)), (10,90))

        pygame.display.flip()
        reloj.tick(30)

# Iniciar el juego
pantalla_inicio()
juego()