import pygame, random, sys

# Inicializar pygame
pygame.init()
ANCHO, ALTO = 600, 400
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Recolector Verde")
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
        pantalla.fill((135, 206, 235))  # cielo celeste
        pygame.draw.rect(pantalla, (139, 69, 19), (0, 350, ANCHO, 50))  # suelo

        mostrar_texto("Recolector Verde", fuente_titulo, (0, 100, 0), 120)
        mostrar_texto("Mové al recolector con las flechas", fuente, (0, 0, 0), 200)
        mostrar_texto("Recolectá 10 basuras para limpiar el planeta", fuente, (0, 0, 0), 250)
        mostrar_texto("Presioná ESPACIO para comenzar", fuente, (0, 100, 0), 320)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                en_inicio = False

        pygame.display.flip()
        reloj.tick(30)

# Pantalla de victoria
def pantalla_final(puntaje):
    en_final = True
    while en_final:
        pantalla.fill((135, 206, 235))
        pygame.draw.rect(pantalla, (139, 69, 19), (0, 350, ANCHO, 50))
        mostrar_texto("¡Misión cumplida!", fuente_titulo, (0, 150, 0), 130)
        mostrar_texto("¡El planeta te lo agradece!", fuente, (0, 100, 0), 190)
        mostrar_texto(f"Basuras recolectadas: {puntaje}", fuente, (0, 0, 0), 250)
        mostrar_texto("Presioná R para jugar otra vez o ESC para salir", fuente, (0, 80, 0), 320)

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
    verde = (0, 200, 0)
    marron = (139, 69, 19)
    celeste = (135, 206, 235)
    gris = (100, 100, 100)

    jugador = pygame.Rect(280, 310, 40, 40)
    basuras = [pygame.Rect(random.randint(20, 560), random.randint(50, 320), 20, 20) for _ in range(5)]
    puntos = 0
    meta = 10  # ahora más largo

    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Movimiento del jugador
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]: jugador.x -= 5
        if teclas[pygame.K_RIGHT]: jugador.x += 5
        if teclas[pygame.K_UP]: jugador.y -= 5
        if teclas[pygame.K_DOWN]: jugador.y += 5

        # Limites
        jugador.x = max(0, min(jugador.x, ANCHO - jugador.width))
        jugador.y = max(0, min(jugador.y, 350 - jugador.height))

        # Colisión con basura
        for basura in basuras:
            if jugador.colliderect(basura):
                puntos += 1
                print("♻️ ¡Basura recolectada!")
                basura.x, basura.y = random.randint(20, 560), random.randint(50, 320)

        # Verificar meta
        if puntos >= meta:
            pantalla_final(puntos)

        # Dibujar
        pantalla.fill(celeste)
        pygame.draw.rect(pantalla, marron, (0, 350, ANCHO, 50))
        for basura in basuras:
            pygame.draw.rect(pantalla, gris, basura)
        pygame.draw.rect(pantalla, verde, jugador)

        # Texto de puntaje
        texto = fuente.render(f"Basuras recolectadas: {puntos}/{meta}", True, (0, 0, 0))
        pantalla.blit(texto, (10, 10))

        pygame.display.flip()
        reloj.tick(60)  #Fluidez

# Iniciar
pantalla_inicio()
juego()
