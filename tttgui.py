"""
Tic Tac Toe 
"""
import os,sys
import pygame
from pygame.locals import *
import tttboard
import tttai

#initialize pygame 
pygame.init()

#dimension constants
GUI_WIDTH = 400
GUI_HEIGHT = GUI_WIDTH
BAR_WIDTH = 5

def load_image(name, colorkey=None, alpha=False):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    if alpha:
        image = image.convert_alpha()
    else:
        image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

class TicTacGUI:
    """
    GUI for Tic Tac Toe game.
    """
    
    def __init__(self, size, aiplayer, aifunction, reverse=False):
        # Game board
        self._size = size
        self._bar_spacing = GUI_WIDTH // self._size
        self._halfsize = int(.4 * self._bar_spacing)         
        self._turn = tttboard.PLAYERX
        self._reverse = reverse

        # AI setup
        self._humanplayer = tttboard.switch_player(aiplayer)
        self._aiplayer = aiplayer
        self._aifunction = aifunction
       
        # Set up data structures
        self._first_load = True
        self.setup_screen()

        
    def setup_screen(self):
        """
        Create pygame display and load images
        """
        self._screen = pygame.display.set_mode((GUI_WIDTH, GUI_HEIGHT))
        self._screen_rect = self._screen.get_rect()
        pygame.display.set_caption('Tic-Tac-Toe')        
        self._background, self._background_rect = load_image('bg.jpg')
        self._start_img, dum_rec = load_image('startscreen.png', alpha=True)
        if pygame.font.get_init():
            self._font = pygame.font.Font(None,80)
        else:
            self._messagesurface = Surface((0,0))
            print 'font initialization failed'
        self.newgame()

    def newgame(self):
        """
        Start new game.
        """
        self._board = tttboard.TTTBoard(self._size, self._reverse)
        self._inprogress = True
        self._wait = False
        self._turn = tttboard.PLAYERX
        self._message = None
        self._winner = None
        if self._first_load:
            self._first_load = False
            self.startscreen()
        else:
            self.main()
            
    def draw_msg(self):
        """
        draw current message to sreen
        """
        msg = self._font.render(self._message, True,(255,0,100))
        sizex = self._font.size(self._message)[0]//2
        sizey = self._font.size(self._message)[1]//2
        self._screen.blit(msg,((self._screen_rect.centerx-sizex),
                                self._screen_rect.centery-sizey))

    def drawx(self, pos):
        """
        Draw an X on the given canvas at the given position.
        """
        pygame.draw.line(self._screen,(255,255,255),
                         (pos[0]-self._halfsize, pos[1]-self._halfsize),
                         (pos[0]+self._halfsize, pos[1]+self._halfsize),
                         BAR_WIDTH)
        pygame.draw.line(self._screen, (255,255,255),
                         (pos[0]+self._halfsize, pos[1]-self._halfsize),
                         (pos[0]-self._halfsize, pos[1]+self._halfsize),
                         BAR_WIDTH)
        
    def drawo(self, pos):
        """
        Draw an O on the given canvas at the given position.
        """
        pygame.draw.circle(self._screen, (255,255,255),
                           pos,self._halfsize, BAR_WIDTH)

    def drawgrid(self):
        """
        Draw game grid
        """
        for bar_start in range(self._bar_spacing,
                               GUI_WIDTH - 1,
                               self._bar_spacing):
            pygame.draw.line(self._screen,
                             (255,255,255),
                             (bar_start, 0),
                             (bar_start, GUI_WIDTH),
                             BAR_WIDTH)
            pygame.draw.line(self._screen,
                             (255,255,255),
                             (0, bar_start),
                             (GUI_WIDTH, bar_start),
                             BAR_WIDTH)
    def draw_moves(self):
        """
        Draw the current players' moves
        """
        for row in range(self._size):
            for col in range(self._size):
                symbol = self._board.square(row, col)
                coords = self.get_coords_from_grid(row, col)
                if symbol == tttboard.PLAYERX:
                    self.drawx(coords)
                elif symbol == tttboard.PLAYERO:
                    self.drawo(coords)
            
    def aimove(self):
        """
        make ai move.
        """ 
        if self._inprogress and (self._turn == self._aiplayer):
            row, col = self._aifunction(self._board, 
                                        self._aiplayer)   
            if self._board.square(row, col) == tttboard.EMPTY:
                self._board.move(row, col, self._aiplayer)
            self._turn = self._humanplayer
            winner = self._board.check_win()          
            if winner is not None:
                self._winner = winner
                self.game_over(winner)
                    
    def get_coords_from_grid(self, row, col):
        """
        given a grid position in the form (row, col), returns
        the coordinates on the canvas of the center of the grid.
        """
        # x coordinate = (bar spacing) * (col + 1/2)
        # y coordinate = height - (bar spacing) * (row + 1/2)
        return (int(self._bar_spacing * (col + 1.0/2)), # x
                int(self._bar_spacing * (row + 1.0/2.0))) # y
    
    def get_grid_from_coords(self, position):
        """
        given coordinates on a canvas, gets the indices of
        the grid.
        """
        posx, posy = position
        return (posy // self._bar_spacing, # row
                posx // self._bar_spacing) # col

    def click(self, event):
        """
        Make human move.
        """
        position = event.pos
        if self._inprogress and (self._turn == self._humanplayer):        
            row, col = self.get_grid_from_coords(position)
            if self._board.square(row, col) == tttboard.EMPTY:
                self._board.move(row, col, self._humanplayer)
                self._turn = self._aiplayer
                winner = self._board.check_win()           
                if winner is not None:
                    self._winner = winner
                    self.game_over(winner)
                self._wait = True
                
    def keydown(self, event):
        """
        keydown event handler
        """
        if event.key == K_ESCAPE:
            sys.exit()
        elif event.key== K_n:
            self.newgame()

    def quit(self, event):
        """
        completely exit game 
        """
        sys.exit()

    def update(self):
        """
        Updates the tic-tac-toe GUI.
        """
        # draw current board
        self.drawgrid()
        self.draw_moves()        
        # Run AI, if necessary
        if not self._wait:
            self.aimove()
        else:
            self._wait = False

    def startscreen(self):
        """
        start screen loop
        """
        clock = pygame.time.Clock()
        self._inprogress = False
        while not self._inprogress:
            clock.tick(30)
            for event in pygame.event.get():
                 if event.type == QUIT:
                     self.quit(event)
                 elif event.type == KEYDOWN:
                     if event.key == K_RETURN:
                         self.newgame()
            self._screen.blit(self._background, self._screen_rect)
            self._screen.blit(self._start_img, (75,50))
            pygame.display.flip()

    def game_over(self, winner):
        """
        game over loop
        """
        # set result message
        if winner == tttboard.DRAW:
            self._message = "It's a tie!"
        elif winner == tttboard.PLAYERX:
            self._message = "X Wins!"
        elif winner == tttboard.PLAYERO:
            self._message = "O Wins!"
            
        # game is no longer in progress
        self._inprogress = False
        # wait for input 
        clock = pygame.time.Clock()
        while self._winner:
            clock.tick(30)
            for event in pygame.event.get():
                 if event.type == QUIT:
                     self.quit(event)
                 elif event.type == KEYDOWN:
                     self.keydown(event)          
            self.draw_moves()
            self.drawgrid()
            self.draw_msg()
            pygame.display.flip()
            
    def main(self):
        """
        main game loop
        """
        clock = pygame.time.Clock()
        while 1:
            clock.tick(30)
            self._screen.blit(self._background, self._screen_rect)
            for event in pygame.event.get():
                 if event.type == QUIT:
                     self.quit(event)
                 elif event.type == KEYDOWN:
                     self.keydown(event)
                 elif event.type == MOUSEBUTTONDOWN:
                     self.click(event)
            self.update()
            pygame.display.flip()
        
def run_gui(board_size, ai_player, ai_function, reverse=False):
    """
    Instantiate and run the GUI
    """
    gui = TicTacGUI(board_size, ai_player, ai_function, reverse)


if __name__ == "__main__":
    """
    run gui when module loads
    """
    run_gui(3,tttboard.PLAYERO,tttai.mm_move_wrapper)
