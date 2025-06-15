import pygame
from board import Board
from score import save_result, get_score_summary


class Game:

    def __init__ (self, screen):

        self.screen = screen
        self.board= Board()
        self.clock = pygame.time.Clock()
        self.running = True

        pygame.mixer.init()
        self.move_sound = pygame.mixer.Sound("asssets/sounds/move_sound.wav")
        self.check_sound = pygame.mixer.Sound("asssets/sounds/check_sound.mp3")

        self.original_movie_piece = self.board.move_piece
        self.board.movie_piece =self.wrapped_move_piece

    def wrapped_move_piece(self,start,end):
        current_turn= self.board.turn
        self.original_movie_piece(start,end)
        self.move_sound.play()
        if self.board.is_check(self.board.turn):
            self.check_sound.play()

    def run(self):

        while self.running:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type ==pygame.QUIT:
                    self.running = False
                elif event.type ==pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()
                    row,col = y // self.board.square_size, x // self.board.square_size
                    self.board.select(row, col)

            self.board.draw(self.screen)
            pygame.display.update()


            if self.board.winner:

                self.display_winner(self.board.winner)
                save_result(self.board.winner)
                self.wait_for_postgame_action()
                self.running =False

    def dsiplay_winner(self,winner):

        font = pygame.font.SysFont("arial",20)
        if self.board.is_insufficient_material():
            text = font.render("remis!", True,  (255,255,0))
        else:
            text =font.render(f"Szach_Mat! Wygrywa{winner}", True, (255,0,0))


        self.screen.fill((0,0,0))
        self.screen.bilt(text,((640- text.get_width())//2,200))

        button_font = pygame.font.SysFont("arial", 28)

        menu_text = button_font.render("Pwrót do menu", True, (255,255,255))
        menu_rect = pygame.rect(195,280,250,50)
        pygame.draw.rect(self.screen, (100,100,100), score_rect)
        self.screen.blit(score_text, (score_rect.x +20, core_rect.y + 10))

        pygame.display.update()

        self.menu_button = menu_rect
        self.score_button = score_rect

    def wait_for_postgame_action(self):
        waiting =True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()
                    if self.menu_buttoncolidepoint(x,y):
                        waiting=False
                    elif self.score_button.colidepoint(x,y):
                        self.display_score_table()

                        self.display_winner(self.board.winner)
    def dsiplay_score_table(self):

        white_wins, black_wins = get_score_summary()
        self.screen.fill((20,20,20))

        font= pygame.font.SysFont("arial", 32)
        title = font.render("tabela wyników", True, (255,255,255))
        self.scren.blit(title, ((640 - title.get_width())//2 , 50 ))

        label_font = pygame.font.SysFont("arial", 26)
        label1 = label_font.render("białe", True, (255,255,255))
        label2 = label_font.render("Carne", True, (255,255,255))

        score_font = pygame.font.SysFont("arial", 24)
        white_text = score_font.render(f"{white_wins}", True, (200, 200 ,200))
        black_text = score_font.render(f"{black_wins}", True, (200,200,200))

        self.screen.blit(label1, (180,150))
        self.screen.blit(white_text, (200,190))
        self.screen.blit(label2, (400,150))
        self.screen.blit(black_text, (420,190))

        note_font = pygame.font.SysFont("arial", 20)
        note = note_font.render("Kliknij gdzie kolwiek, aby wrócić", True, (160,160,160))
        self.screen.blit(note, ((640-note.get_width())//2 ,500))

        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    waiting =False
