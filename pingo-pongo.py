import pygame
import sys
import random


def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
    ball.x = ball.x + ball_speed_x
    ball.y = ball.y + ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:  # vertical
        pygame.mixer.Sound.play(pong_sound)
        ball_speed_y = ball_speed_y * -1  # quando a bola colide com a borda da janela, inverte a velocidade da bola

    if ball.left <= 0:
        pygame.mixer.Sound.play(score_sound)
        player_score += 1
        players_restart()
        score_time = pygame.time.get_ticks()

    if ball.right >= screen_width:  # <= ao inves de = por conta da atualização de frames
        pygame.mixer.Sound.play(score_sound)
        opponent_score += 1
        players_restart()
        score_time = pygame.time.get_ticks()

    if ball.colliderect(player) and ball_speed_x > 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.right - player.left) < 10:
            ball_speed_x = ball_speed_x * -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
            ball_speed_y = ball_speed_y * -1
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y > 0:
            ball_speed_y = ball_speed_y * -1

    if ball.colliderect(opponent) and ball_speed_x < 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.left - opponent.right) < 10:
            ball_speed_x = ball_speed_x * -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
            ball_speed_y = ball_speed_y * -1
        elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y > 0:
            ball_speed_y = ball_speed_y * -1


def player_animation():  # impede o player de mover pra fora da tela
    player.y = player.y + player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height


def opponent_ai():
    if opponent.top < ball.y:
        opponent.top = opponent.top + opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom = opponent.bottom - opponent_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height


def ball_restart():
    global ball_speed_x, ball_speed_y, score_time

    current_time = pygame.time.get_ticks()
    ball.center = (screen_width/2, screen_height/2)  # teleporta a bola de volta pro centro da tela

    if current_time - score_time < 700:
        number_three = game_font.render('3', False, light_grey)
        screen.blit(number_three, (screen_width/2 - 10, screen_height/2 + 20))
    if 700 < current_time - score_time < 1400:
        number_two = game_font.render('2', False, light_grey)
        screen.blit(number_two, (screen_width/2 - 10, screen_height/2 + 20))
    if 1400 < current_time - score_time < 2100:
        number_one = game_font.render('1', False, light_grey)
        screen.blit(number_one, (screen_width/2 - 10, screen_height/2 + 20))

    if current_time - score_time < 2100:
        ball_speed_x, ball_speed_y = 0, 0
    else:
        ball_speed_y = 7 * random.choice((1, -1))
        ball_speed_x = 7 * random.choice((1, -1))
        score_time = None


def players_restart():
    player.center = (screen_width - 15, screen_height/2 - 15)
    opponent.center = (15, screen_height/2 - 35)


# General setup
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()  # Inicia os módulos do pygame
clock = pygame.time.Clock()

# Criando a janela principal
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width, screen_height))  # Cria um display e atribui uma variavel
pygame.display.set_caption('Pong')  # Título da janela

# Retângulos do jogo
ball = pygame.Rect(screen_width/2 - 15, screen_height/2 - 15, 30, 30)  # x, y do retangulo no plano, largura e altura
player = pygame.Rect(screen_width-20, screen_height/2-70, 10, 140)  # screenwidht-20 bota no canto superior esquerd
opponent = pygame.Rect(10, screen_height/2-70, 10, 140)

# Cores
bg_color = pygame.Color('grey12')
light_grey = (200, 200, 200)

# Variaveis do jogo
ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
player_speed = 0
opponent_speed = 7

# Variaveis de texto
player_score = 0
opponent_score = 0
game_font = pygame.font.Font('freesansbold.ttf', 32)

# Timer de ponto
score_time = True

# Sons
pong_sound = pygame.mixer.Sound('pong.ogg')
score_sound = pygame.mixer.Sound('score.ogg')

while True:  # Loop
    # ver o input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # fechar o jogo
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:  # Tecla pressionada
            if event.key == pygame.K_DOWN:  # Seta pra baixo
                player_speed = player_speed + 7  # Adiciona 7 na variavel player_speed
            if event.key == pygame.K_UP:  # Seta pra cima
                player_speed = player_speed - 7  # Subtrai 7 da variavel player_speed

        if event.type == pygame.KEYUP:  # Tecla deixa de estar pressionada
            if event.key == pygame.K_DOWN:  # Seta pra baixo
                player_speed = player_speed - 7  # se a seta pra baixo deixar de ser pressionada
            if event.key == pygame.K_UP:  # Seta pra cima
                player_speed = player_speed + 7

    # Lógica do jogo
    ball_animation()
    player_animation()
    opponent_ai()

    # Visuais
    screen.fill(bg_color)  # primeiro código lido, portanto camada mais profunda
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width/2, 0), (screen_width/2, screen_height))  # camada mais rasa

    if score_time:
        ball_restart()

    player_text = game_font.render(f'{player_score}', False, light_grey)
    screen.blit(player_text, (660, 470))

    opponent_text = game_font.render(f'{opponent_score}', False, light_grey)
    screen.blit(opponent_text, (600, 470))

    # Atualizar a janela
    pygame.display.flip()  # Pega tudo que veio anteriormente no loop e mostra na tela
    clock.tick(60)  # Limita quantas vezes o loop acontece (60x por segundo)
