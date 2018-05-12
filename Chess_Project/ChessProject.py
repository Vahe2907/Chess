from pygame import *
import sys
import random

class Board:
    def __init__(self):
        self.wind = image.load(r'PS\ChessBoard.png')
        self.act = image.load(r'PS\active.png')
        self.kontur = image.load(r'PS\kontur.png')
        self.stop = image.load(r'PS\stop.png')
        self.eat = image.load(r'PS\can_eat.png')
        self.mode = False
        self.player_color = None
    def render(self, active = None, act_figure = None):
        if active != None:
            if len(active[0][1:]) == 0 and len(active[1]) == 0:
                self.wind.blit(self.stop, active[0][0])
            else:
                self.wind.blit(self.kontur, active[0][0])
                for c in active[0][1:]:
                    self.wind.blit(self.act, c)
                for c in active[1]:
                    self.wind.blit(self.eat, c)
                if isinstance(act_figure, King):
                    for c in active[2]:
                        self.wind.blit(self.act, c)
        else:
            SpawnAll()        

class Pawn:
    def __init__(self, color, coord):
        self.color = color.lower()
        self.coord = coord
        self.move = False
        self.steps_count = 0
        self.add_steps = []
        self.steps = [[], [], []]
        if self.color == 'white':
            self.pic = image.load('Figures\White_Pawn.png')
            board.wind.blit(self.pic, self.coord)
        else:
            self.pic = image.load('Figures\Black_Pawn.png')
            board.wind.blit(self.pic, self.coord)
    def get_pos(self):
        return self.coord
    def update(self, new_coord):
        self.coord = new_coord
    def return_color(self):
        return self.color
    def show(self):
        board.wind.blit(self.pic, self.coord)
    def update_steps(self):  
        x, y = self.coord
        self.steps = [[(x - 25, y - 10)], [], []]
        self.protect_figures = []
        self.attack_figures = []        
        if self.color == 'white':
            if  y - 100 >= 10 and dosk[x, y - 100] == None:
                if y == 610:
                    if dosk[x, y - 200] == None:
                        self.steps[0] += [(x - 25, y - 110), (x - 25, y - 210)]
                    else:
                        self.steps[0].append((x - 25, y - 110))
                else:
                    self.steps[0].append((x - 25, y - 110))
            if x + 100 <= 725 and y - 100 >= 10:
                self.steps[2].append((x + 75, y - 110))
            if x - 100 >= 25 and y - 100 >= 10:
                self.steps[2].append((x - 125, y - 110))
            if x + 100 <= 725 and y - 100 >= 10 and dosk[(x + 100, y - 100)] != None and dosk[(x + 100, y - 100)].return_color() == 'black':
                self.steps[1].append((x + 75, y - 110))
                self.attack_figures.append(dosk[(x + 100, y - 100)])
                if isinstance(dosk[x + 100, y - 100], King):
                    black_king.check = True
                    if dosk[self.coord] != None:
                        black_king.check_figure = dosk[self.coord]                   
            elif x + 100 <= 725 and y - 100 >= 10 and dosk[(x + 100, y - 100)] != None and dosk[(x + 100, y - 100)].return_color() == 'white':
                if not isinstance(dosk[(x + 100, y - 100)], King):
                    self.protect_figures.append(dosk[(x + 100, y - 100)])
            if x - 100 >= 25 and y - 100 >= 10 and dosk[(x - 100, y - 100)] != None and dosk[(x - 100, y - 100)].return_color() == 'black':
                self.steps[1].append((x - 125, y - 110))
                self.attack_figures.append(dosk[(x - 100, y - 100)])
                if isinstance(dosk[x - 100, y - 100], King):
                    black_king.check = True
                    if dosk[self.coord] != None:
                        black_king.check_figure = dosk[self.coord]                    
            elif x - 100 >= 25 and y - 100 >= 10 and dosk[(x - 100, y - 100)] != None and dosk[(x - 100, y - 100)].return_color() == 'white':
                if not isinstance(dosk[(x - 100, y - 100)], King):
                    self.protect_figures.append(dosk[(x - 100, y - 100)])            
        else:
            if y + 100 <= 710 and dosk[x, y + 100] == None:
                if y == 110:
                    if dosk[x, y + 200] == None:
                        self.steps[0] += [(x - 25, y + 90), (x - 25, y + 190)]
                    else:
                        self.steps[0].append((x - 25, y + 90))
                else:
                    self.steps[0].append((x - 25, y + 90))
            if x + 100 <= 725 and y + 100 <= 710:
                self.steps[2].append((x + 75, y + 90))
            if x - 100 >= 25 and y + 100 <= 710:
                self.steps[2].append((x - 125, y + 90))
            if x + 100 <= 725 and y + 100 <= 710 and dosk[(x + 100, y + 100)] != None and dosk[(x + 100, y + 100)].return_color() == 'white':
                self.steps[1].append((x + 75, y + 90))
                self.attack_figures.append(dosk[(x + 100, y + 100)])
                if isinstance(dosk[x + 100, y + 100], King):
                    white_king.check = True
                    if dosk[self.coord] != None:
                        white_king.check_figure = dosk[self.coord]                
            elif x + 100 <= 725 and y + 100 <= 710 and dosk[(x + 100, y + 100)] != None and dosk[(x + 100, y + 100)].return_color() == 'black':
                if not isinstance(dosk[(x + 100, y + 100)], King):
                    self.protect_figures.append(dosk[(x + 100, y + 100)])                
            if x - 100 >= 25 and y + 100 <= 710 and dosk[(x - 100, y + 100)] != None and dosk[(x - 100, y + 100)].return_color() == 'white':
                self.steps[1].append((x - 125, y + 90))
                self.attack_figures.append(dosk[(x - 100, y + 100)])
                if isinstance(dosk[x - 100, y + 100], King):
                    white_king.check = True
                    if dosk[self.coord] != None:
                        white_king.check_figure = dosk[self.coord]                  
            elif x - 100 >= 25 and y + 100 <= 710 and dosk[(x - 100, y + 100)] != None and dosk[(x - 100, y + 100)].return_color() == 'black':
                if not isinstance(dosk[(x - 100, y + 100)], King):
                    self.protect_figures.append(dosk[(x - 100, y + 100)])
        if self.color == 'white':
            if white_king.check:
                new_steps = [[(x - 25, y - 10)], [], []]           
                if isinstance(white_king.check_figure, Bishop):
                    for step in self.steps[0][1:]:     
                        if get_rotation(white_king.check_figure.coord, (step[0] + 25, step[1] + 10), 'Bishop', white_king):
                            new_steps[0].append(step)
                    for step in self.steps[1]:
                        if white_king.check_figure.coord == (step[0] + 25, step[1] + 10):
                            new_steps[1].append(step)
                elif isinstance(white_king.check_figure, Knight) or isinstance(white_king.check_figure, Pawn):
                    for step in self.steps[1]:
                        if white_king.check_figure.coord == (step[0] + 25, step[1] + 10):
                            new_steps[1].append(step)
                elif isinstance(white_king.check_figure, Rook):
                    for step in self.steps[0][1:]:     
                        if get_rotation(white_king.check_figure.coord, (step[0] + 25, step[1] + 10), 'Rook', white_king):
                            new_steps[0].append(step)
                    for step in self.steps[1]:
                        if white_king.check_figure.coord == (step[0] + 25, step[1] + 10):
                            new_steps[1].append(step)
                elif isinstance(white_king.check_figure, Queen):
                    for step in self.steps[0][1:]:     
                        if get_rotation(white_king.check_figure.coord, (step[0] + 25, step[1] + 10), 'Queen', white_king):
                            new_steps[0].append(step)
                    for step in self.steps[1]:
                        if white_king.check_figure.coord == (step[0] + 25, step[1] + 10):
                            new_steps[1].append(step)                    
                self.steps = new_steps                        
            else:
                for ex_fig in [black_rook1, black_rook2, black_bishop1, black_bishop2, black_queen]:
                    if dosk[self.coord] in ex_fig.attack_figures:
                        if isinstance(ex_fig, Rook):
                            if get_rotation(ex_fig.coord, self.coord, 'Rook', white_king):
                                cond = True
                                for w_fig in white_figures:
                                    if get_rotation(self.coord, w_fig.coord, 'Rook', white_king):
                                        cond = False
                                        break
                                if cond:                                 
                                    new_steps = [[(x - 25, y - 10)], [], []]
                                    for step in self.steps[0][1:]:
                                        if get_rotation(ex_fig.coord, (step[0] + 25, step[1] + 10), 'Rook', white_king):
                                            new_steps[0].append(step) 
                                    for step in self.steps[1]:
                                        if ex_fig.coord == (step[0] + 25, step[1] + 10):
                                            new_steps[1].append(step)
                                    self.steps = new_steps
                                    break
                        elif isinstance(ex_fig, Bishop):
                            if get_rotation(ex_fig.coord, self.coord, 'Bishop', white_king):
                                cond = True
                                for w_fig in white_figures:
                                    if get_rotation(self.coord, w_fig.coord, 'Bishop', white_king):
                                        cond = False
                                        break
                                if cond:                                
                                    new_steps = [[(x - 25, y - 10)], [], []]
                                    for step in self.steps[0][1:]:
                                        if get_rotation(ex_fig.coord, (step[0] + 25, step[1] + 10), 'Bishop', white_king):
                                            new_steps[0].append(step) 
                                    for step in self.steps[1]:
                                        if ex_fig.coord == (step[0] + 25, step[1] + 10):
                                            new_steps[1].append(step)
                                    self.steps = new_steps
                                    break                                        
                        elif isinstance(ex_fig, Queen):
                            if get_rotation(ex_fig.coord, self.coord, 'Queen', white_king):
                                cond = True
                                for w_fig in white_figures:
                                    if get_rotation(self.coord, w_fig.coord, 'Queen', white_king):
                                        cond = False
                                        break
                                if cond:                                 
                                    new_steps = [[(x - 25, y - 10)], [], []]
                                    for step in self.steps[0][1:]:
                                        if get_rotation(ex_fig.coord, (step[0] + 25, step[1] + 10), 'Queen', white_king):
                                            new_steps[0].append(step) 
                                    for step in self.steps[1]:
                                        if ex_fig.coord == (step[0] + 25, step[1] + 10):
                                            new_steps[1].append(step)
                                    self.steps = new_steps
                                    break
            if self.coord[1] == 310:
                if self.coord[0] + 100 <= 725:
                    if isinstance(dosk[(self.coord[0] + 100, self.coord[1])], Pawn) and dosk[(self.coord[0] + 100, self.coord[1])].color == 'black' and dosk[(self.coord[0] + 100, self.coord[1])].steps_count == 1:
                        self.steps[1].append((self.coord[0] + 75, self.coord[1] - 110))
                if self.coord[0] - 100 >= 25:
                    if isinstance(dosk[(self.coord[0] - 100, self.coord[1])], Pawn) and dosk[(self.coord[0] - 100, self.coord[1])].color == 'black' and dosk[(self.coord[0] - 100, self.coord[1])].steps_count == 1:
                        self.steps[1].append((self.coord[0] - 125, self.coord[1] - 110))
        else:
            if black_king.check:
                new_steps = [[(x - 25, y - 10)], [], []]           
                if isinstance(black_king.check_figure, Bishop):
                    for step in self.steps[0][1:]:     
                        if get_rotation(black_king.check_figure.coord, (step[0] + 25, step[1] + 10), 'Bishop', black_king):
                            new_steps[0].append(step)
                    for step in self.steps[1]:
                        if black_king.check_figure.coord == (step[0] + 25, step[1] + 10):
                            new_steps[1].append(step)
                elif isinstance(black_king.check_figure, Knight) or isinstance(black_king.check_figure, Pawn):
                    for step in self.steps[1]:
                        if black_king.check_figure.coord == (step[0] + 25, step[1] + 10):
                            new_steps[1].append(step)
                elif isinstance(black_king.check_figure, Rook):
                    print(self.coord)
                    for step in self.steps[0][1:]:     
                        if get_rotation(black_king.check_figure.coord, (step[0] + 25, step[1] + 10), 'Rook', black_king):
                            new_steps[0].append(step)
                    for step in self.steps[1]:
                        if black_king.check_figure.coord == (step[0] + 25, step[1] + 10):
                            new_steps[1].append(step)
                elif isinstance(black_king.check_figure, Queen):
                    for step in self.steps[0][1:]:     
                        if get_rotation(black_king.check_figure.coord, (step[0] + 25, step[1] + 10), 'Queen', black_king):
                            new_steps[0].append(step)
                    for step in self.steps[1]:
                        if black_king.check_figure.coord == (step[0] + 25, step[1] + 10):
                            new_steps[1].append(step)                    
                self.steps = new_steps
            else:
                for ex_fig in [white_rook1, white_rook2, white_bishop1, white_bishop2, white_queen]:
                    if dosk[self.coord] in ex_fig.attack_figures:
                        if isinstance(ex_fig, Rook):
                            if get_rotation(ex_fig.coord, self.coord, 'Rook', black_king):
                                cond = True
                                for b_fig in black_figures:
                                    if get_rotation(self.coord, b_fig.coord, 'Rook', black_king):
                                        cond = False
                                        break
                                if cond:                                
                                    new_steps = [[(x - 25, y - 10)], [], []]
                                    for step in self.steps[0][1:]:
                                        if get_rotation(ex_fig.coord, (step[0] + 25, step[1] + 10), 'Rook', black_king):
                                            new_steps[0].append(step) 
                                    for step in self.steps[1]:
                                        if ex_fig.coord == (step[0] + 25, step[1] + 10):
                                            new_steps[1].append(step)
                                    self.steps = new_steps
                                    break                            
                        elif isinstance(ex_fig, Bishop):
                            if get_rotation(ex_fig.coord, self.coord, 'Bishop', black_king):
                                cond = True
                                for b_fig in black_figures:
                                    if get_rotation(self.coord, b_fig.coord, 'Bishop', black_king):
                                        cond = False
                                        break
                                if cond:
                                    new_steps = [[(x - 25, y - 10)], [], []]
                                    for step in self.steps[0][1:]:
                                        if get_rotation(ex_fig.coord, (step[0] + 25, step[1] + 10), 'Bishop', black_king):
                                            new_steps[0].append(step) 
                                    for step in self.steps[1]:
                                        if ex_fig.coord == (step[0] + 25, step[1] + 10):
                                            new_steps[1].append(step)
                                    self.steps = new_steps
                                break                                        
                        elif isinstance(ex_fig, Queen):
                            if get_rotation(ex_fig.coord, self.coord, 'Queen', black_king):
                                cond = True
                                for b_fig in black_figures:
                                    if get_rotation(self.coord, b_fig.coord, 'Queen', black_king):
                                        cond = False
                                        break
                                if cond:                                
                                    new_steps = [[(x - 25, y - 10)], [], []]
                                    for step in self.steps[0][1:]:
                                        if get_rotation(ex_fig.coord, (step[0] + 25, step[1] + 10), 'Queen', black_king):
                                            new_steps[0].append(step) 
                                    for step in self.steps[1]:
                                        if ex_fig.coord == (step[0] + 25, step[1] + 10):
                                            new_steps[1].append(step)
                                    self.steps = new_steps
                                    break
            if self.coord[1] == 410:
                    if self.coord[0] + 100 <= 725:
                        if isinstance(dosk[(self.coord[0] + 100, self.coord[1])], Pawn) and dosk[(self.coord[0] + 100, self.coord[1])].color == 'white' and dosk[(self.coord[0] + 100, self.coord[1])].steps_count == 1:
                            self.steps[1].append((self.coord[0] + 75, self.coord[1] + 90))
                    if self.coord[0] - 100 >= 25:
                        if isinstance(dosk[(self.coord[0] - 100, self.coord[1])], Pawn) and dosk[(self.coord[0] - 100, self.coord[1])].color == 'white' and dosk[(self.coord[0] - 100, self.coord[1])].steps_count == 1:
                            self.steps[1].append((self.coord[0] - 125, self.coord[1] + 90))
                    
    def pos(self):
        SpawnAll()
        self.update_steps()
        board.render(self.steps)
                            
class Rook:
    def __init__(self, color, coord):
        self.color = color
        self.coord = coord
        self.move = False
        self.steps = [[], []]
        self.attack_figures = []
        self.protect_figures = []
        self.count_steps = 0
        if self.color.lower() == 'white':
            self.pic = image.load('Figures\White_Rook.png')
            board.wind.blit(self.pic, self.coord)
        else:
            self.pic = image.load('Figures\Black_Rook.png')
            board.wind.blit(self.pic, self.coord)
    def get_pos(self):
        return self.coord
    def update(self, new_coord):
        self.coord = new_coord
    def return_color(self):
        return self.color        
    def show(self):
        board.wind.blit(self.pic, self.coord)
    def update_steps(self):
        end1 = False
        end2 = False
        x, y = self.coord
        self.steps = [[(x - 25, y - 10)], []]
        self.protect_figures = []
        self.attack_figures = []
        self.ignore_attack_figures = []
        self.ignore_protect_figures = []
        x1, x2 = x, x
        y1, y2 = y, y
        while x1 > 25:
            x1 -= 100
            if dosk[x1, y] == None:
                self.steps[0].append((x1 - 25, y - 10))
            else:
                if self.color == 'white':
                    if dosk[x1, y].return_color() == 'black':
                        self.steps[1].append((x1 - 25, y - 10))
                        self.attack_figures.append(dosk[x1, y])
                        if isinstance(dosk[x1, y], King):
                            black_king.check = True
                            if dosk[self.coord] != None:
                                black_king.check_figure = dosk[self.coord]                        
                        break
                    else:
                        if not isinstance(dosk[x1, y], King):
                            self.protect_figures.append(dosk[x1, y])
                else:
                    if dosk[x1, y].return_color() == 'white':
                        self.steps[1].append((x1 - 25, y - 10))
                        self.attack_figures.append(dosk[x1, y])
                        if isinstance(dosk[x1, y], King):
                            white_king.check = True
                            if dosk[self.coord] != None:
                                white_king.check_figure = dosk[self.coord]
                        break
                    else:
                        if not isinstance(dosk[x1, y], King):
                            self.protect_figures.append(dosk[x1, y])               
                break
        while x2 < 725:
            x2 += 100
            if dosk[x2, y] == None:
                self.steps[0].append((x2 - 25, y - 10))
            else:
                if self.color == 'white':
                    if dosk[x2, y].return_color() == 'black':
                        self.steps[1].append((x2 - 25, y - 10))
                        self.attack_figures.append(dosk[x2, y])
                        if isinstance(dosk[x2, y], King):
                            black_king.check = True
                            if dosk[self.coord] != None:
                                black_king.check_figure = dosk[self.coord]                          
                        break
                    else:
                        if not isinstance(dosk[x2, y], King):
                            self.protect_figures.append(dosk[x2, y])
                else:
                    if dosk[x2, y].return_color() == 'white':
                        self.steps[1].append((x2 - 25, y - 10))
                        self.attack_figures.append(dosk[x2, y])
                        if isinstance(dosk[x2, y], King):
                            white_king.check = True
                            if dosk[self.coord] != None:
                                white_king.check_figure = dosk[self.coord]                        
                        break
                    else:
                        if not isinstance(dosk[x2, y], King):
                            self.protect_figures.append(dosk[x2, y])
                break
        while y1 > 10:
            y1 -= 100
            if dosk[x, y1] == None:
                self.steps[0].append((x - 25, y1 - 10))
            else:
                if self.color == 'white':
                    if dosk[x, y1].return_color() == 'black':
                        self.steps[1].append((x - 25, y1 - 10))
                        self.attack_figures.append(dosk[x, y1])
                        if isinstance(dosk[x, y1], King):
                            black_king.check = True
                            if dosk[self.coord] != None:
                                black_king.check_figure = dosk[self.coord]                        
                        break
                    else:
                        if not isinstance(dosk[x, y1], King):
                            self.protect_figures.append(dosk[x, y1])
                else:
                    if dosk[x, y1].return_color() == 'white':
                        self.steps[1].append((x - 25, y1 - 10))
                        self.attack_figures.append(dosk[x, y1])
                        if isinstance(dosk[x, y1], King):
                            white_king.check = True
                            if dosk[self.coord] != None:
                                white_king.check_figure = dosk[self.coord]                         
                        break
                    else:
                        if not isinstance(dosk[x, y1], King):
                            self.protect_figures.append(dosk[x, y1])                      
                break
        while y2 < 710:
            y2 += 100
            if dosk[x, y2] == None:
                self.steps[0].append((x - 25, y2 - 10))
            else:
                if self.color == 'white':
                    if dosk[x, y2].return_color() == 'black':
                        self.steps[1].append((x - 25, y2 - 10))
                        self.attack_figures.append(dosk[x, y2])
                        if isinstance(dosk[x, y2], King):
                            black_king.check = True
                            if dosk[self.coord] != None:
                                black_king.check_figure = dosk[self.coord]                          
                        break
                    else:
                        if not isinstance(dosk[x, y2], King):
                            self.protect_figures.append(dosk[x, y2]) 
                else:
                    if dosk[x, y2].return_color() == 'white':
                        self.steps[1].append((x - 25, y2 - 10))
                        self.attack_figures.append(dosk[x, y2])
                        if isinstance(dosk[x, y2], King):
                            white_king.check = True
                            if dosk[self.coord] != None:
                                white_king.check_figure = dosk[self.coord]                        
                        break
                    else:
                        if not isinstance(dosk[x, y2], King):
                            self.protect_figures.append(dosk[x, y2])                        
                break
        if self.color == 'white':
            if white_king.check:
                new_steps = [[(x - 25, y - 10)], [], []]           
                if isinstance(white_king.check_figure, Bishop):
                    for step in self.steps[0][1:]:     
                        if get_rotation(white_king.check_figure.coord, (step[0] + 25, step[1] + 10), 'Bishop', white_king):
                            new_steps[0].append(step)
                    for step in self.steps[1]:
                        if white_king.check_figure.coord == (step[0] + 25, step[1] + 10):
                            new_steps[1].append(step)
                elif isinstance(white_king.check_figure, Knight) or isinstance(white_king.check_figure, Pawn):
                    for step in self.steps[1]:
                        if white_king.check_figure.coord == (step[0] + 25, step[1] + 10):
                            new_steps[1].append(step)
                elif isinstance(white_king.check_figure, Rook):
                    for step in self.steps[0][1:]:     
                        if get_rotation(white_king.check_figure.coord, (step[0] + 25, step[1] + 10), 'Rook', white_king):
                            new_steps[0].append(step)
                    for step in self.steps[1]:
                        if white_king.check_figure.coord == (step[0] + 25, step[1] + 10):
                            new_steps[1].append(step)
                elif isinstance(white_king.check_figure, Queen):
                    for step in self.steps[0][1:]:     
                        if get_rotation(white_king.check_figure.coord, (step[0] + 25, step[1] + 10), 'Queen', white_king):
                            new_steps[0].append(step)
                    for step in self.steps[1]:
                        if white_king.check_figure.coord == (step[0] + 25, step[1] + 10):
                            new_steps[1].append(step)                    
                self.steps = new_steps                        
            else:
                for ex_fig in [black_rook1, black_rook2, black_bishop1, black_bishop2, black_queen]:
                    if dosk[self.coord] in ex_fig.attack_figures:
                        if isinstance(ex_fig, Rook):
                            if get_rotation(ex_fig.coord, self.coord, 'Rook', white_king):
                                new_steps = [[(x - 25, y - 10)], [], []]
                                for step in self.steps[0][1:]:
                                    if get_rotation(ex_fig.coord, (step[0] + 25, step[1] + 10), 'Rook', white_king):
                                        new_steps[0].append(step) 
                                for step in self.steps[1]:
                                    if ex_fig.coord == (step[0] + 25, step[1] + 10):
                                        new_steps[1].append(step)
                                self.steps = new_steps
                                break
                        elif isinstance(ex_fig, Bishop):
                            if get_rotation(ex_fig.coord, self.coord, 'Bishop', white_king):
                                new_steps = [[(x - 25, y - 10)], [], []]
                                for step in self.steps[0][1:]:
                                    if get_rotation(ex_fig.coord, (step[0] + 25, step[1] + 10), 'Bishop', white_king):
                                        new_steps[0].append(step) 
                                for step in self.steps[1]:
                                    if ex_fig.coord == (step[0] + 25, step[1] + 10):
                                        new_steps[1].append(step)
                                self.steps = new_steps
                                break                                        
                        elif isinstance(ex_fig, Queen):
                            if get_rotation(ex_fig.coord, self.coord, 'Queen', white_king):
                                new_steps = [[(x - 25, y - 10)], [], []]
                                for step in self.steps[0][1:]:
                                    if get_rotation(ex_fig.coord, (step[0] + 25, step[1] + 10), 'Queen', white_king):
                                        new_steps[0].append(step) 
                                for step in self.steps[1]:
                                    if ex_fig.coord == (step[0] + 25, step[1] + 10):
                                        new_steps[1].append(step)
                                self.steps = new_steps
                                break                                            
        else:
            if black_king.check:
                new_steps = [[(x - 25, y - 10)], [], []]           
                if isinstance(black_king.check_figure, Bishop):
                    for step in self.steps[0][1:]:     
                        if get_rotation(black_king.check_figure.coord, (step[0] + 25, step[1] + 10), 'Bishop', black_king):
                            new_steps[0].append(step)
                    for step in self.steps[1]:
                        if black_king.check_figure.coord == (step[0] + 25, step[1] + 10):
                            new_steps[1].append(step)
                elif isinstance(black_king.check_figure, Knight) or isinstance(black_king.check_figure, Pawn):
                    for step in self.steps[1]:
                        if black_king.check_figure.coord == (step[0] + 25, step[1] + 10):
                            new_steps[1].append(step)
                elif isinstance(black_king.check_figure, Rook):
                    for step in self.steps[0][1:]:     
                        if get_rotation(black_king.check_figure.coord, (step[0] + 25, step[1] + 10), 'Rook', black_king):
                            new_steps[0].append(step)
                    for step in self.steps[1]:
                        if black_king.check_figure.coord == (step[0] + 25, step[1] + 10):
                            new_steps[1].append(step)
                elif isinstance(black_king.check_figure, Queen):
                    for step in self.steps[0][1:]:     
                        if get_rotation(black_king.check_figure.coord, (step[0] + 25, step[1] + 10), 'Queen', black_king):
                            new_steps[0].append(step)
                    for step in self.steps[1]:
                        if black_king.check_figure.coord == (step[0] + 25, step[1] + 10):
                            new_steps[1].append(step)                    
                self.steps = new_steps
            else:
                for ex_fig in [white_rook1, white_rook2, white_bishop1, white_bishop2, white_queen]:
                    if dosk[self.coord] in ex_fig.attack_figures:
                        if isinstance(ex_fig, Rook):
                            if get_rotation(ex_fig.coord, self.coord, 'Rook', black_king):
                                new_steps = [[(x - 25, y - 10)], [], []]
                                for step in self.steps[0][1:]:
                                    if get_rotation(ex_fig.coord, (step[0] + 25, step[1] + 10), 'Rook', black_king):
                                        new_steps[0].append(step) 
                                for step in self.steps[1]:
                                    if ex_fig.coord == (step[0] + 25, step[1] + 10):
                                        new_steps[1].append(step)
                                self.steps = new_steps
                                break                            
                        elif isinstance(ex_fig, Bishop):
                            if get_rotation(ex_fig.coord, self.coord, 'Bishop', black_king):
                                new_steps = [[(x - 25, y - 10)], [], []]
                                for step in self.steps[0][1:]:
                                    if get_rotation(ex_fig.coord, (step[0] + 25, step[1] + 10), 'Bishop', black_king):
                                        new_steps[0].append(step) 
                                for step in self.steps[1]:
                                    if ex_fig.coord == (step[0] + 25, step[1] + 10):
                                        new_steps[1].append(step)
                                self.steps = new_steps
                                break                                        
                        elif isinstance(ex_fig, Queen):
                            if get_rotation(ex_fig.coord, self.coord, 'Queen', black_king):
                                new_steps = [[(x - 25, y - 10)], [], []]
                                for step in self.steps[0][1:]:
                                    if get_rotation(ex_fig.coord, (step[0] + 25, step[1] + 10), 'Queen', black_king):
                                        new_steps[0].append(step) 
                                for step in self.steps[1]:
                                    if ex_fig.coord == (step[0] + 25, step[1] + 10):
                                        new_steps[1].append(step)
                                self.steps = new_steps
                                break
    def pos(self):
        SpawnAll()
        self.update_steps()     
        board.render(self.steps)
        
class Knight:
    def __init__(self, color, coord):
        self.color = color
        self.coord = coord
        self.move = False
        self.steps = [[], []]
        self.attack_figures = []
        self.protect_figures = []          
        self.count_steps = 0
        if self.color.lower() == 'white':
            self.pic = image.load('Figures\White_Knight.png')
            board.wind.blit(self.pic, self.coord)
        else:
            self.pic = image.load('Figures\Black_Knight.png')
            board.wind.blit(self.pic, self.coord)
    def get_pos(self):
        return self.coord
    def update(self, new_coord):
        self.coord = new_coord
    def return_color(self):
        return self.color        
    def show(self):
        board.wind.blit(self.pic, self.coord)
    def update_steps(self):  
        x, y = self.coord
        self.steps = [[(x - 25, y - 10)], []]
        self.protect_figures = []
        self.attack_figures = []        
        for cor in coords:
            if abs((coords[cor][0] - x) * (coords[cor][1] - y)) == 20000:
                if dosk[coords[cor]] == None:
                    self.steps[0].append((coords[cor][0] - 25, coords[cor][1] - 10))
                else:
                    if self.color == 'white':
                        if dosk[coords[cor]].return_color() == 'black':
                            self.steps[1].append((coords[cor][0] - 25, coords[cor][1] - 10))
                            self.attack_figures.append(dosk[coords[cor]])
                            if isinstance(dosk[coords[cor]], King):
                                black_king.check = True
                                if dosk[self.coord] != None:
                                    black_king.check_figure = dosk[self.coord]                             
                        else:
                            if not isinstance(dosk[coords[cor]], King):
                                self.protect_figures.append(dosk[coords[cor]])
                    else:
                        if dosk[coords[cor]].return_color() == 'white':
                            self.steps[1].append((coords[cor][0] - 25, coords[cor][1] - 10))
                            self.attack_figures.append(dosk[coords[cor]])
                            if isinstance(dosk[coords[cor]], King):
                                white_king.check = True
                                if dosk[self.coord] != None:
                                    white_king.check_figure = dosk[self.coord]                             
                        else:
                            if not isinstance(dosk[coords[cor]], King):
                                self.protect_figures.append(dosk[coords[cor]])
        if self.color == 'white':
            if white_king.check:
                new_steps = [[(x - 25, y - 10)], [], []]           
                if isinstance(white_king.check_figure, Bishop):
                    for step in self.steps[0][1:]:     
                        if get_rotation(white_king.check_figure.coord, (step[0] + 25, step[1] + 10), 'Bishop', white_king):
                            new_steps[0].append(step)
                    for step in self.steps[1]:
                        if white_king.check_figure.coord == (step[0] + 25, step[1] + 10):
                            new_steps[1].append(step)
                elif isinstance(white_king.check_figure, Knight) or isinstance(white_king.check_figure, Pawn):
                    for step in self.steps[1]:
                        if white_king.check_figure.coord == (step[0] + 25, step[1] + 10):
                            new_steps[1].append(step)
                elif isinstance(white_king.check_figure, Rook):
                    for step in self.steps[0][1:]:     
                        if get_rotation(white_king.check_figure.coord, (step[0] + 25, step[1] + 10), 'Rook', white_king):
                            new_steps[0].append(step)
                    for step in self.steps[1]:
                        if white_king.check_figure.coord == (step[0] + 25, step[1] + 10):
                            new_steps[1].append(step)
                elif isinstance(white_king.check_figure, Queen):
                    for step in self.steps[0][1:]:     
                        if get_rotation(white_king.check_figure.coord, (step[0] + 25, step[1] + 10), 'Queen', white_king):
                            new_steps[0].append(step)
                    for step in self.steps[1]:
                        if white_king.check_figure.coord == (step[0] + 25, step[1] + 10):
                            new_steps[1].append(step)                    
                self.steps = new_steps                        
            else:
                for ex_fig in [black_rook1, black_rook2, black_bishop1, black_bishop2, black_queen]:
                    if dosk[self.coord] in ex_fig.attack_figures:
                        if isinstance(ex_fig, Rook):
                            if get_rotation(ex_fig.coord, self.coord, 'Rook', white_king):
                                cond = True
                                for w_fig in white_figures:
                                    if get_rotation(self.coord, w_fig.coord, 'Rook', white_king):
                                        cond = False
                                        break
                                if cond:                                 
                                    new_steps = [[(x - 25, y - 10)], [], []]
                                    for step in self.steps[0][1:]:
                                        if get_rotation(ex_fig.coord, (step[0] + 25, step[1] + 10), 'Rook', white_king):
                                            new_steps[0].append(step) 
                                    for step in self.steps[1]:
                                        if ex_fig.coord == (step[0] + 25, step[1] + 10):
                                            new_steps[1].append(step)
                                    self.steps = new_steps
                                    break
                        elif isinstance(ex_fig, Bishop):
                            if get_rotation(ex_fig.coord, self.coord, 'Bishop', white_king):
                                cond = True
                                for w_fig in white_figures:
                                    if get_rotation(self.coord, w_fig.coord, 'Bishop', white_king):
                                        cond = False
                                        break
                                if cond:                                
                                    new_steps = [[(x - 25, y - 10)], [], []]
                                    for step in self.steps[0][1:]:
                                        if get_rotation(ex_fig.coord, (step[0] + 25, step[1] + 10), 'Bishop', white_king):
                                            new_steps[0].append(step) 
                                    for step in self.steps[1]:
                                        if ex_fig.coord == (step[0] + 25, step[1] + 10):
                                            new_steps[1].append(step)
                                    self.steps = new_steps
                                    break                                        
                        elif isinstance(ex_fig, Queen):
                            if get_rotation(ex_fig.coord, self.coord, 'Queen', white_king):
                                cond = True
                                for w_fig in white_figures:
                                    if get_rotation(self.coord, w_fig.coord, 'Queen', white_king):
                                        cond = False
                                        break
                                if cond:                                 
                                    new_steps = [[(x - 25, y - 10)], [], []]
                                    for step in self.steps[0][1:]:
                                        if get_rotation(ex_fig.coord, (step[0] + 25, step[1] + 10), 'Queen', white_king):
                                            new_steps[0].append(step) 
                                    for step in self.steps[1]:
                                        if ex_fig.coord == (step[0] + 25, step[1] + 10):
                                            new_steps[1].append(step)
                                    self.steps = new_steps
                                    break                                   
        else:
            if black_king.check:
                new_steps = [[(x - 25, y - 10)], [], []]           
                if isinstance(black_king.check_figure, Bishop):
                    for step in self.steps[0][1:]:     
                        if get_rotation(black_king.check_figure.coord, (step[0] + 25, step[1] + 10), 'Bishop', black_king):
                            new_steps[0].append(step)
                    for step in self.steps[1]:
                        if black_king.check_figure.coord == (step[0] + 25, step[1] + 10):
                            new_steps[1].append(step)
                elif isinstance(black_king.check_figure, Knight) or isinstance(black_king.check_figure, Pawn):
                    for step in self.steps[1]:
                        if black_king.check_figure.coord == (step[0] + 25, step[1] + 10):
                            new_steps[1].append(step)
                elif isinstance(black_king.check_figure, Rook):
                    print(self.coord)
                    for step in self.steps[0][1:]:     
                        if get_rotation(black_king.check_figure.coord, (step[0] + 25, step[1] + 10), 'Rook', black_king):
                            new_steps[0].append(step)
                    for step in self.steps[1]:
                        if black_king.check_figure.coord == (step[0] + 25, step[1] + 10):
                            new_steps[1].append(step)
                elif isinstance(black_king.check_figure, Queen):
                    for step in self.steps[0][1:]:     
                        if get_rotation(black_king.check_figure.coord, (step[0] + 25, step[1] + 10), 'Queen', black_king):
                            new_steps[0].append(step)
                    for step in self.steps[1]:
                        if black_king.check_figure.coord == (step[0] + 25, step[1] + 10):
                            new_steps[1].append(step)                    
                self.steps = new_steps
            else:
                for ex_fig in [white_rook1, white_rook2, white_bishop1, white_bishop2, white_queen]:
                    if dosk[self.coord] in ex_fig.attack_figures:
                        if isinstance(ex_fig, Rook):
                            if get_rotation(ex_fig.coord, self.coord, 'Rook', black_king):
                                cond = True
                                for b_fig in black_figures:
                                    if get_rotation(self.coord, b_fig.coord, 'Rook', black_king):
                                        cond = False
                                        break
                                if cond:                                
                                    new_steps = [[(x - 25, y - 10)], [], []]
                                    for step in self.steps[0][1:]:
                                        if get_rotation(ex_fig.coord, (step[0] + 25, step[1] + 10), 'Rook', black_king):
                                            new_steps[0].append(step) 
                                    for step in self.steps[1]:
                                        if ex_fig.coord == (step[0] + 25, step[1] + 10):
                                            new_steps[1].append(step)
                                    self.steps = new_steps
                                    break                            
                        elif isinstance(ex_fig, Bishop):
                            if get_rotation(ex_fig.coord, self.coord, 'Bishop', black_king):
                                cond = True
                                for b_fig in black_figures:
                                    if get_rotation(self.coord, b_fig.coord, 'Bishop', black_king):
                                        cond = False
                                        break
                                if cond:
                                    new_steps = [[(x - 25, y - 10)], [], []]
                                    for step in self.steps[0][1:]:
                                        if get_rotation(ex_fig.coord, (step[0] + 25, step[1] + 10), 'Bishop', black_king):
                                            new_steps[0].append(step) 
                                    for step in self.steps[1]:
                                        if ex_fig.coord == (step[0] + 25, step[1] + 10):
                                            new_steps[1].append(step)
                                    self.steps = new_steps
                                break                                        
                        elif isinstance(ex_fig, Queen):
                            if get_rotation(ex_fig.coord, self.coord, 'Queen', black_king):
                                cond = True
                                for b_fig in black_figures:
                                    if get_rotation(self.coord, b_fig.coord, 'Queen', black_king):
                                        cond = False
                                        break
                                if cond:                                
                                    new_steps = [[(x - 25, y - 10)], [], []]
                                    for step in self.steps[0][1:]:
                                        if get_rotation(ex_fig.coord, (step[0] + 25, step[1] + 10), 'Queen', black_king):
                                            new_steps[0].append(step) 
                                    for step in self.steps[1]:
                                        if ex_fig.coord == (step[0] + 25, step[1] + 10):
                                            new_steps[1].append(step)
                                    self.steps = new_steps
                                    break
    def pos(self):
        SpawnAll()
        self.update_steps()       
        board.render(self.steps)
    
class Bishop:
    def __init__(self, color, coord):
        self.color = color
        self.coord = coord
        self.move = False
        self.steps = [[], []]
        self.attack_figures = []
        self.protect_figures = []          
        self.count_steps = 0
        if self.color.lower() == 'white':
            self.pic = image.load('Figures\White_Bishop.png')
            board.wind.blit(self.pic, self.coord)
        else:
            self.pic = image.load('Figures\Black_Bishop.png')
            board.wind.blit(self.pic, self.coord)
    def get_pos(self):
        return self.coord
    def update(self, new_coord):
        self.coord = new_coord
    def return_color(self):
        return self.color        
    def show(self):
        board.wind.blit(self.pic, self.coord)
    def update_steps(self):      
        x, y = self.coord
        self.steps = [[(x - 25, y - 10)], []]
        self.attack_figures = []
        self.protect_figures = []
        x1, y1 = x, y
        x2, y2 = x, y
        x3, y3 = x, y
        x4, y4 = x, y
        while x1 < 725 and y1 > 10:
            x1 += 100
            y1 -= 100
            if dosk[x1, y1] == None:
                self.steps[0].append((x1 - 25, y1 - 10))
            else:
                if self.color == 'white':
                    if dosk[x1, y1].return_color() == 'black':
                        self.steps[1].append((x1 - 25, y1 - 10))
                        self.attack_figures.append(dosk[x1, y1])
                        if isinstance(dosk[x1, y1], King):
                            black_king.check = True
                            if dosk[self.coord] != None:
                                black_king.check_figure = dosk[self.coord]                          
                        break
                    else:
                        if not isinstance(dosk[x1, y1], King):
                            self.protect_figures.append(dosk[x1, y1])
                else:
                    if dosk[x1, y1].return_color() == 'white':
                        self.steps[1].append((x1 - 25, y1 - 10))
                        self.attack_figures.append(dosk[x1, y1])
                        if isinstance(dosk[x1, y1], King):
                            white_king.check = True
                            if dosk[self.coord] != None:
                                white_king.check_figure = dosk[self.coord]                         
                        break
                    else:
                        if not isinstance(dosk[x1, y1], King):
                            self.protect_figures.append(dosk[x1, y1])                   
                break
        while x2 > 25 and y2 > 10:
            x2 -= 100
            y2 -= 100
            if dosk[x2, y2] == None:
                self.steps[0].append((x2 - 25, y2 - 10))
            else:
                if self.color == 'white':
                    if dosk[x2, y2].return_color() == 'black':
                        self.steps[1].append((x2 - 25, y2 - 10))
                        self.attack_figures.append(dosk[x2, y2])
                        if isinstance(dosk[x2, y2], King):
                            black_king.check = True
                            if dosk[self.coord] != None:
                                black_king.check_figure = dosk[self.coord]                        
                        break
                    else:
                        if not isinstance(dosk[x2, y2], King):
                            self.protect_figures.append(dosk[x2, y2])
                else:
                    if dosk[x2, y2].return_color() == 'white':
                        self.steps[1].append((x2 - 25, y2 - 10))
                        self.attack_figures.append(dosk[x2, y2])
                        if isinstance(dosk[x2, y2], King):
                            white_king.check = True
                            if dosk[self.coord] != None:
                                white_king.check_figure = dosk[self.coord]                          
                        break
                    else:
                        if not isinstance(dosk[x2, y2], King):
                            self.protect_figures.append(dosk[x2, y2])                      
                break
        while x3 < 725 and y3 < 710:
            x3 += 100
            y3 += 100
            if dosk[x3, y3] == None:
                self.steps[0].append((x3 - 25, y3 - 10))
            else:
                if self.color == 'white':
                    if dosk[x3, y3].return_color() == 'black':
                        self.steps[1].append((x3 - 25, y3 - 10))
                        self.attack_figures.append(dosk[x3, y3])
                        if isinstance(dosk[x3, y3], King):
                            black_king.check = True
                            if dosk[self.coord] != None:
                                black_king.check_figure = dosk[self.coord]                         
                        break
                    else:
                        if not isinstance(dosk[x3, y3], King):
                            self.protect_figures.append(dosk[x3, y3])
                else:
                    if dosk[x3, y3].return_color() == 'white':
                        self.steps[1].append((x3 - 25, y3 - 10))
                        self.attack_figures.append(dosk[x3, y3])
                        if isinstance(dosk[x3, y3], King):
                            white_king.check = True
                            if dosk[self.coord] != None:
                                white_king.check_figure = dosk[self.coord]                         
                        break
                    else:
                        if not isinstance(dosk[x3, y3], King):
                            self.protect_figures.append(dosk[x3, y3])                       
                break
        while x4 > 25 and y4 < 710:
            x4 -= 100
            y4 += 100
            if dosk[x4, y4] == None:
                self.steps[0].append((x4 - 25, y4 - 10))
            else:
                if self.color == 'white':
                    if dosk[x4, y4].return_color() == 'black':
                        self.steps[1].append((x4 - 25, y4 - 10))
                        self.attack_figures.append(dosk[x4, y4])
                        if isinstance(dosk[x4, y4], King):
                            black_king.check = True
                            if dosk[self.coord] != None:
                                black_king.check_figure = dosk[self.coord]                        
                        break
                    else:
                        if not isinstance(dosk[x4, y4], King):
                            self.protect_figures.append(dosk[x4, y4])
                else:
                    if dosk[x4, y4].return_color() == 'white':
                        self.steps[1].append((x4 - 25, y4 - 10))
                        self.attack_figures.append(dosk[x4, y4])
                        if isinstance(dosk[x4, y4], King):
                            white_king.check = True
                            if dosk[self.coord] != None:
                                white_king.check_figure = dosk[self.coord]                        
                        break
                    else:
                        if not isinstance(dosk[x4, y4], King):
                            self.protect_figures.append(dosk[x4, y4])                      
                break
        if self.color == 'white':
            if white_king.check:
                new_steps = [[(x - 25, y - 10)], [], []]           
                if isinstance(white_king.check_figure, Bishop):
                    for step in self.steps[0][1:]:     
                        if get_rotation(white_king.check_figure.coord, (step[0] + 25, step[1] + 10), 'Bishop', white_king):
                            new_steps[0].append(step)
                    for step in self.steps[1]:
                        if white_king.check_figure.coord == (step[0] + 25, step[1] + 10):
                            new_steps[1].append(step)
                elif isinstance(white_king.check_figure, Knight) or isinstance(white_king.check_figure, Pawn):
                    for step in self.steps[1]:
                        if white_king.check_figure.coord == (step[0] + 25, step[1] + 10):
                            new_steps[1].append(step)
                elif isinstance(white_king.check_figure, Rook):
                    for step in self.steps[0][1:]:     
                        if get_rotation(white_king.check_figure.coord, (step[0] + 25, step[1] + 10), 'Rook', white_king):
                            new_steps[0].append(step)
                    for step in self.steps[1]:
                        if white_king.check_figure.coord == (step[0] + 25, step[1] + 10):
                            new_steps[1].append(step)
                elif isinstance(white_king.check_figure, Queen):
                    for step in self.steps[0][1:]:     
                        if get_rotation(white_king.check_figure.coord, (step[0] + 25, step[1] + 10), 'Queen', white_king):
                            new_steps[0].append(step)
                    for step in self.steps[1]:
                        if white_king.check_figure.coord == (step[0] + 25, step[1] + 10):
                            new_steps[1].append(step)                    
                self.steps = new_steps                        
            else:
                for ex_fig in [black_rook1, black_rook2, black_bishop1, black_bishop2, black_queen]:
                    if dosk[self.coord] in ex_fig.attack_figures:
                        if isinstance(ex_fig, Rook):
                            if get_rotation(ex_fig.coord, self.coord, 'Rook', white_king):
                                cond = True
                                for w_fig in white_figures:
                                    if get_rotation(self.coord, w_fig.coord, 'Rook', white_king):
                                        cond = False
                                        break
                                if cond:                                 
                                    new_steps = [[(x - 25, y - 10)], [], []]
                                    for step in self.steps[0][1:]:
                                        if get_rotation(ex_fig.coord, (step[0] + 25, step[1] + 10), 'Rook', white_king):
                                            new_steps[0].append(step) 
                                    for step in self.steps[1]:
                                        if ex_fig.coord == (step[0] + 25, step[1] + 10):
                                            new_steps[1].append(step)
                                    self.steps = new_steps
                                    break
                        elif isinstance(ex_fig, Bishop):
                            if get_rotation(ex_fig.coord, self.coord, 'Bishop', white_king):
                                cond = True
                                for w_fig in white_figures:
                                    if get_rotation(self.coord, w_fig.coord, 'Bishop', white_king):
                                        cond = False
                                        break
                                if cond:                                
                                    new_steps = [[(x - 25, y - 10)], [], []]
                                    for step in self.steps[0][1:]:
                                        if get_rotation(ex_fig.coord, (step[0] + 25, step[1] + 10), 'Bishop', white_king):
                                            new_steps[0].append(step) 
                                    for step in self.steps[1]:
                                        if ex_fig.coord == (step[0] + 25, step[1] + 10):
                                            new_steps[1].append(step)
                                    self.steps = new_steps
                                    break                                        
                        elif isinstance(ex_fig, Queen):
                            if get_rotation(ex_fig.coord, self.coord, 'Queen', white_king):
                                cond = True
                                for w_fig in white_figures:
                                    if get_rotation(self.coord, w_fig.coord, 'Queen', white_king):
                                        cond = False
                                        break
                                if cond:                                 
                                    new_steps = [[(x - 25, y - 10)], [], []]
                                    for step in self.steps[0][1:]:
                                        if get_rotation(ex_fig.coord, (step[0] + 25, step[1] + 10), 'Queen', white_king):
                                            new_steps[0].append(step) 
                                    for step in self.steps[1]:
                                        if ex_fig.coord == (step[0] + 25, step[1] + 10):
                                            new_steps[1].append(step)
                                    self.steps = new_steps
                                    break                                   
        else:
            if black_king.check:
                new_steps = [[(x - 25, y - 10)], [], []]           
                if isinstance(black_king.check_figure, Bishop):
                    for step in self.steps[0][1:]:     
                        if get_rotation(black_king.check_figure.coord, (step[0] + 25, step[1] + 10), 'Bishop', black_king):
                            new_steps[0].append(step)
                    for step in self.steps[1]:
                        if black_king.check_figure.coord == (step[0] + 25, step[1] + 10):
                            new_steps[1].append(step)
                elif isinstance(black_king.check_figure, Knight) or isinstance(black_king.check_figure, Pawn):
                    for step in self.steps[1]:
                        if black_king.check_figure.coord == (step[0] + 25, step[1] + 10):
                            new_steps[1].append(step)
                elif isinstance(black_king.check_figure, Rook):
                    print(self.coord)
                    for step in self.steps[0][1:]:     
                        if get_rotation(black_king.check_figure.coord, (step[0] + 25, step[1] + 10), 'Rook', black_king):
                            new_steps[0].append(step)
                    for step in self.steps[1]:
                        if black_king.check_figure.coord == (step[0] + 25, step[1] + 10):
                            new_steps[1].append(step)
                elif isinstance(black_king.check_figure, Queen):
                    for step in self.steps[0][1:]:     
                        if get_rotation(black_king.check_figure.coord, (step[0] + 25, step[1] + 10), 'Queen', black_king):
                            new_steps[0].append(step)
                    for step in self.steps[1]:
                        if black_king.check_figure.coord == (step[0] + 25, step[1] + 10):
                            new_steps[1].append(step)                    
                self.steps = new_steps
            else:
                for ex_fig in [white_rook1, white_rook2, white_bishop1, white_bishop2, white_queen]:
                    if dosk[self.coord] in ex_fig.attack_figures:
                        if isinstance(ex_fig, Rook):
                            if get_rotation(ex_fig.coord, self.coord, 'Rook', black_king):
                                cond = True
                                for b_fig in black_figures:
                                    if get_rotation(self.coord, b_fig.coord, 'Rook', black_king):
                                        cond = False
                                        break
                                if cond:                                
                                    new_steps = [[(x - 25, y - 10)], [], []]
                                    for step in self.steps[0][1:]:
                                        if get_rotation(ex_fig.coord, (step[0] + 25, step[1] + 10), 'Rook', black_king):
                                            new_steps[0].append(step) 
                                    for step in self.steps[1]:
                                        if ex_fig.coord == (step[0] + 25, step[1] + 10):
                                            new_steps[1].append(step)
                                    self.steps = new_steps
                                    break                            
                        elif isinstance(ex_fig, Bishop):
                            if get_rotation(ex_fig.coord, self.coord, 'Bishop', black_king):
                                cond = True
                                for b_fig in black_figures:
                                    if get_rotation(self.coord, b_fig.coord, 'Bishop', black_king):
                                        cond = False
                                        break
                                if cond:
                                    new_steps = [[(x - 25, y - 10)], [], []]
                                    for step in self.steps[0][1:]:
                                        if get_rotation(ex_fig.coord, (step[0] + 25, step[1] + 10), 'Bishop', black_king):
                                            new_steps[0].append(step) 
                                    for step in self.steps[1]:
                                        if ex_fig.coord == (step[0] + 25, step[1] + 10):
                                            new_steps[1].append(step)
                                    self.steps = new_steps
                                break                                        
                        elif isinstance(ex_fig, Queen):
                            if get_rotation(ex_fig.coord, self.coord, 'Queen', black_king):
                                cond = True
                                for b_fig in black_figures:
                                    if get_rotation(self.coord, b_fig.coord, 'Queen', black_king):
                                        cond = False
                                        break
                                if cond:                                
                                    new_steps = [[(x - 25, y - 10)], [], []]
                                    for step in self.steps[0][1:]:
                                        if get_rotation(ex_fig.coord, (step[0] + 25, step[1] + 10), 'Queen', black_king):
                                            new_steps[0].append(step) 
                                    for step in self.steps[1]:
                                        if ex_fig.coord == (step[0] + 25, step[1] + 10):
                                            new_steps[1].append(step)
                                    self.steps = new_steps
                                    break             
    def pos(self):
        SpawnAll()
        self.update_steps()
        board.render(self.steps)
    
class Queen:
    def __init__(self, color, coord):
        self.color = color
        self.coord = coord
        self.move = False
        self.steps = [[], []]
        self.attack_figures = []
        self.protect_figures = []          
        self.count_steps = 0
        if self.color.lower() == 'white':
            self.pic = image.load('Figures\White_Queen.png')
            board.wind.blit(self.pic, self.coord)
        else:
            self.pic = image.load('Figures\Black_Queen.png')
            board.wind.blit(self.pic, self.coord)
    def get_pos(self):
        return self.coord
    def update(self, new_coord):
        self.coord = new_coord
    def return_color(self):
        return self.color        
    def show(self):
        board.wind.blit(self.pic, self.coord)
    def update_steps(self):  
        x, y = self.coord
        self.steps = [[(x - 25, y - 10)], []]
        self.protect_figures = []
        self.attack_figures = []        
        x1, x2 = x, x
        y1, y2 = y, y        
        while x1 > 25:
            x1 -= 100
            if dosk[x1, y] == None:
                self.steps[0].append((x1 - 25, y - 10))
            else:
                if self.color == 'white':
                    if dosk[x1, y].return_color() == 'black':
                        self.steps[1].append((x1 - 25, y - 10))
                        self.attack_figures.append(dosk[x1, y])
                        if isinstance(dosk[x1, y], King):
                            black_king.check = True
                            if dosk[self.coord] != None:
                                black_king.check_figure = dosk[self.coord]                        
                        break
                    else:
                        if not isinstance(dosk[x1, y], King):
                            self.protect_figures.append(dosk[x1, y])
                else:
                    if dosk[x1, y].return_color() == 'white':
                        self.steps[1].append((x1 - 25, y - 10))
                        self.attack_figures.append(dosk[x1, y])
                        if isinstance(dosk[x1, y], King):
                            white_king.check = True
                            if dosk[self.coord] != None:
                                white_king.check_figure = dosk[self.coord]
                        break
                    else:
                        if not isinstance(dosk[x1, y], King):
                            self.protect_figures.append(dosk[x1, y])               
                break
        while x2 < 725:
            x2 += 100
            if dosk[x2, y] == None:
                self.steps[0].append((x2 - 25, y - 10))
            else:
                if self.color == 'white':
                    if dosk[x2, y].return_color() == 'black':
                        self.steps[1].append((x2 - 25, y - 10))
                        self.attack_figures.append(dosk[x2, y])
                        if isinstance(dosk[x2, y], King):
                            black_king.check = True
                            if dosk[self.coord] != None:
                                black_king.check_figure = dosk[self.coord]                          
                        break
                    else:
                        if not isinstance(dosk[x2, y], King):
                            self.protect_figures.append(dosk[x2, y])
                else:
                    if dosk[x2, y].return_color() == 'white':
                        self.steps[1].append((x2 - 25, y - 10))
                        self.attack_figures.append(dosk[x2, y])
                        if isinstance(dosk[x2, y], King):
                            white_king.check = True
                            if dosk[self.coord] != None:
                                white_king.check_figure = dosk[self.coord]                        
                        break
                    else:
                        if not isinstance(dosk[x2, y], King):
                            self.protect_figures.append(dosk[x2, y])                        
                break
        while y1 > 10:
            y1 -= 100
            if dosk[x, y1] == None:
                self.steps[0].append((x - 25, y1 - 10))
            else:
                if self.color == 'white':
                    if dosk[x, y1].return_color() == 'black':
                        self.steps[1].append((x - 25, y1 - 10))
                        self.attack_figures.append(dosk[x, y1])
                        if isinstance(dosk[x, y1], King):
                            black_king.check = True
                            if dosk[self.coord] != None:
                                black_king.check_figure = dosk[self.coord]                        
                        break
                    else:
                        if not isinstance(dosk[x, y1], King):
                            self.protect_figures.append(dosk[x, y1])
                else:
                    if dosk[x, y1].return_color() == 'white':
                        self.steps[1].append((x - 25, y1 - 10))
                        self.attack_figures.append(dosk[x, y1])
                        if isinstance(dosk[x, y1], King):
                            white_king.check = True
                            if dosk[self.coord] != None:
                                white_king.check_figure = dosk[self.coord]                         
                        break
                    else:
                        if not isinstance(dosk[x, y1], King):
                            self.protect_figures.append(dosk[x, y1])                      
                break
        while y2 < 710:
            y2 += 100
            if dosk[x, y2] == None:
                self.steps[0].append((x - 25, y2 - 10))
            else:
                if self.color == 'white':
                    if dosk[x, y2].return_color() == 'black':
                        self.steps[1].append((x - 25, y2 - 10))
                        self.attack_figures.append(dosk[x, y2])
                        if isinstance(dosk[x, y2], King):
                            black_king.check = True
                            if dosk[self.coord] != None:
                                black_king.check_figure = dosk[self.coord]                          
                        break
                    else:
                        if not isinstance(dosk[x, y2], King):
                            self.protect_figures.append(dosk[x, y2]) 
                else:
                    if dosk[x, y2].return_color() == 'white':
                        self.steps[1].append((x - 25, y2 - 10))
                        self.attack_figures.append(dosk[x, y2])
                        if isinstance(dosk[x, y2], King):
                            white_king.check = True
                            if dosk[self.coord] != None:
                                white_king.check_figure = dosk[self.coord]                        
                        break
                    else:
                        if not isinstance(dosk[x, y2], King):
                            self.protect_figures.append(dosk[x, y2])                        
                break
        x1, y1 = x, y
        x2, y2 = x, y
        x3, y3 = x, y
        x4, y4 = x, y
        while x1 < 725 and y1 > 10:
            x1 += 100
            y1 -= 100
            if dosk[x1, y1] == None:
                self.steps[0].append((x1 - 25, y1 - 10))
            else:
                if self.color == 'white':
                    if dosk[x1, y1].return_color() == 'black':
                        self.steps[1].append((x1 - 25, y1 - 10))
                        self.attack_figures.append(dosk[x1, y1])
                        if isinstance(dosk[x1, y1], King):
                            black_king.check = True
                            if dosk[self.coord] != None:
                                black_king.check_figure = dosk[self.coord]                          
                        break
                    else:
                        if not isinstance(dosk[x1, y1], King):
                            self.protect_figures.append(dosk[x1, y1])
                else:
                    if dosk[x1, y1].return_color() == 'white':
                        self.steps[1].append((x1 - 25, y1 - 10))
                        self.attack_figures.append(dosk[x1, y1])
                        if isinstance(dosk[x1, y1], King):
                            white_king.check = True
                            if dosk[self.coord] != None:
                                white_king.check_figure = dosk[self.coord]                         
                        break
                    else:
                        if not isinstance(dosk[x1, y1], King):
                            self.protect_figures.append(dosk[x1, y1])                   
                break
        while x2 > 25 and y2 > 10:
            x2 -= 100
            y2 -= 100
            if dosk[x2, y2] == None:
                self.steps[0].append((x2 - 25, y2 - 10))
            else:
                if self.color == 'white':
                    if dosk[x2, y2].return_color() == 'black':
                        self.steps[1].append((x2 - 25, y2 - 10))
                        self.attack_figures.append(dosk[x2, y2])
                        if isinstance(dosk[x2, y2], King):
                            black_king.check = True
                            if dosk[self.coord] != None:
                                black_king.check_figure = dosk[self.coord]                        
                        break
                    else:
                        if not isinstance(dosk[x2, y2], King):
                            self.protect_figures.append(dosk[x2, y2])
                else:
                    if dosk[x2, y2].return_color() == 'white':
                        self.steps[1].append((x2 - 25, y2 - 10))
                        self.attack_figures.append(dosk[x2, y2])
                        if isinstance(dosk[x2, y2], King):
                            white_king.check = True
                            if dosk[self.coord] != None:    
                                white_king.check_figure = dosk[self.coord]                          
                        break
                    else:
                        if not isinstance(dosk[x2, y2], King):
                            self.protect_figures.append(dosk[x2, y2])                      
                break
        while x3 < 725 and y3 < 710:
            x3 += 100
            y3 += 100
            if dosk[x3, y3] == None:
                self.steps[0].append((x3 - 25, y3 - 10))
            else:
                if self.color == 'white':
                    if dosk[x3, y3].return_color() == 'black':
                        self.steps[1].append((x3 - 25, y3 - 10))
                        self.attack_figures.append(dosk[x3, y3])
                        if isinstance(dosk[x3, y3], King):
                            black_king.check = True
                            if dosk[self.coord] != None:
                                black_king.check_figure = dosk[self.coord]                         
                        break
                    else:
                        if not isinstance(dosk[x3, y3], King):
                            self.protect_figures.append(dosk[x3, y3])
                else:
                    if dosk[x3, y3].return_color() == 'white':
                        self.steps[1].append((x3 - 25, y3 - 10))
                        self.attack_figures.append(dosk[x3, y3])
                        if isinstance(dosk[x3, y3], King):
                            white_king.check = True
                            if dosk[self.coord] != None:
                                white_king.check_figure = dosk[self.coord]                         
                        break
                    else:
                        if not isinstance(dosk[x3, y3], King):
                            self.protect_figures.append(dosk[x3, y3])                       
                break
        while x4 > 25 and y4 < 710:
            x4 -= 100
            y4 += 100
            if dosk[x4, y4] == None:
                self.steps[0].append((x4 - 25, y4 - 10))
            else:
                if self.color == 'white':
                    if dosk[x4, y4].return_color() == 'black':
                        self.steps[1].append((x4 - 25, y4 - 10))
                        self.attack_figures.append(dosk[x4, y4])
                        if isinstance(dosk[x4, y4], King):
                            black_king.check = True
                            if dosk[self.coord] != None:
                                black_king.check_figure = dosk[self.coord]                        
                        break
                    else:
                        if not isinstance(dosk[x4, y4], King):
                            self.protect_figures.append(dosk[x4, y4])
                else:
                    if dosk[x4, y4].return_color() == 'white':
                        self.steps[1].append((x4 - 25, y4 - 10))
                        self.attack_figures.append(dosk[x4, y4])
                        if isinstance(dosk[x4, y4], King):
                            white_king.check = True
                            if dosk[self.coord] != None:    
                                white_king.check_figure = dosk[self.coord]                        
                        break
                    else:
                        if not isinstance(dosk[x4, y4], King):
                            self.protect_figures.append(dosk[x4, y4])                      
                break
        if self.color == 'white':
            if white_king.check:
                new_steps = [[(x - 25, y - 10)], [], []]           
                if isinstance(white_king.check_figure, Bishop):
                    for step in self.steps[0][1:]:     
                        if get_rotation(white_king.check_figure.coord, (step[0] + 25, step[1] + 10), 'Bishop', white_king):
                            new_steps[0].append(step)
                    for step in self.steps[1]:
                        if white_king.check_figure.coord == (step[0] + 25, step[1] + 10):
                            new_steps[1].append(step)
                elif isinstance(white_king.check_figure, Knight) or isinstance(white_king.check_figure, Pawn):
                    for step in self.steps[1]:
                        if white_king.check_figure.coord == (step[0] + 25, step[1] + 10):
                            new_steps[1].append(step)
                elif isinstance(white_king.check_figure, Rook):
                    for step in self.steps[0][1:]:     
                        if get_rotation(white_king.check_figure.coord, (step[0] + 25, step[1] + 10), 'Rook', white_king):
                            new_steps[0].append(step)
                    for step in self.steps[1]:
                        if white_king.check_figure.coord == (step[0] + 25, step[1] + 10):
                            new_steps[1].append(step)
                elif isinstance(white_king.check_figure, Queen):
                    for step in self.steps[0][1:]:     
                        if get_rotation(white_king.check_figure.coord, (step[0] + 25, step[1] + 10), 'Queen', white_king):
                            new_steps[0].append(step)
                    for step in self.steps[1]:
                        if white_king.check_figure.coord == (step[0] + 25, step[1] + 10):
                            new_steps[1].append(step)                    
                self.steps = new_steps                        
            else:
                for ex_fig in [black_rook1, black_rook2, black_bishop1, black_bishop2, black_queen]:
                    if dosk[self.coord] in ex_fig.attack_figures:
                        if isinstance(ex_fig, Rook):
                            if get_rotation(ex_fig.coord, self.coord, 'Rook', white_king):
                                cond = True
                                for w_fig in white_figures:
                                    if get_rotation(self.coord, w_fig.coord, 'Rook', white_king):
                                        cond = False
                                        break
                                if cond:                                 
                                    new_steps = [[(x - 25, y - 10)], [], []]
                                    for step in self.steps[0][1:]:
                                        if get_rotation(ex_fig.coord, (step[0] + 25, step[1] + 10), 'Rook', white_king):
                                            new_steps[0].append(step) 
                                    for step in self.steps[1]:
                                        if ex_fig.coord == (step[0] + 25, step[1] + 10):
                                            new_steps[1].append(step)
                                    self.steps = new_steps
                                    break
                        elif isinstance(ex_fig, Bishop):
                            if get_rotation(ex_fig.coord, self.coord, 'Bishop', white_king):
                                cond = True
                                for w_fig in white_figures:
                                    if get_rotation(self.coord, w_fig.coord, 'Bishop', white_king):
                                        cond = False
                                        break
                                if cond:                                
                                    new_steps = [[(x - 25, y - 10)], [], []]
                                    for step in self.steps[0][1:]:
                                        if get_rotation(ex_fig.coord, (step[0] + 25, step[1] + 10), 'Bishop', white_king):
                                            new_steps[0].append(step) 
                                    for step in self.steps[1]:
                                        if ex_fig.coord == (step[0] + 25, step[1] + 10):
                                            new_steps[1].append(step)
                                    self.steps = new_steps
                                    break                                        
                        elif isinstance(ex_fig, Queen):
                            if get_rotation(ex_fig.coord, self.coord, 'Queen', white_king):
                                cond = True
                                for w_fig in white_figures:
                                    if get_rotation(self.coord, w_fig.coord, 'Queen', white_king):
                                        cond = False
                                        break
                                if cond:                                 
                                    new_steps = [[(x - 25, y - 10)], [], []]
                                    for step in self.steps[0][1:]:
                                        if get_rotation(ex_fig.coord, (step[0] + 25, step[1] + 10), 'Queen', white_king):
                                            new_steps[0].append(step) 
                                    for step in self.steps[1]:
                                        if ex_fig.coord == (step[0] + 25, step[1] + 10):
                                            new_steps[1].append(step)
                                    self.steps = new_steps
                                    break                                   
        else:
            if black_king.check:
                new_steps = [[(x - 25, y - 10)], [], []]           
                if isinstance(black_king.check_figure, Bishop):
                    for step in self.steps[0][1:]:     
                        if get_rotation(black_king.check_figure.coord, (step[0] + 25, step[1] + 10), 'Bishop', black_king):
                            new_steps[0].append(step)
                    for step in self.steps[1]:
                        if black_king.check_figure.coord == (step[0] + 25, step[1] + 10):
                            new_steps[1].append(step)
                elif isinstance(black_king.check_figure, Knight) or isinstance(black_king.check_figure, Pawn):
                    for step in self.steps[1]:
                        if black_king.check_figure.coord == (step[0] + 25, step[1] + 10):
                            new_steps[1].append(step)
                elif isinstance(black_king.check_figure, Rook):
                    print(self.coord)
                    for step in self.steps[0][1:]:     
                        if get_rotation(black_king.check_figure.coord, (step[0] + 25, step[1] + 10), 'Rook', black_king):
                            new_steps[0].append(step)
                    for step in self.steps[1]:
                        if black_king.check_figure.coord == (step[0] + 25, step[1] + 10):
                            new_steps[1].append(step)
                elif isinstance(black_king.check_figure, Queen):
                    for step in self.steps[0][1:]:     
                        if get_rotation(black_king.check_figure.coord, (step[0] + 25, step[1] + 10), 'Queen', black_king):
                            new_steps[0].append(step)
                    for step in self.steps[1]:
                        if black_king.check_figure.coord == (step[0] + 25, step[1] + 10):
                            new_steps[1].append(step)                    
                self.steps = new_steps
            else:
                for ex_fig in [white_rook1, white_rook2, white_bishop1, white_bishop2, white_queen]:
                    if dosk[self.coord] in ex_fig.attack_figures:
                        if isinstance(ex_fig, Rook):
                            if get_rotation(ex_fig.coord, self.coord, 'Rook', black_king):
                                cond = True
                                for b_fig in black_figures:
                                    if get_rotation(self.coord, b_fig.coord, 'Rook', black_king):
                                        cond = False
                                        break
                                if cond:                                
                                    new_steps = [[(x - 25, y - 10)], [], []]
                                    for step in self.steps[0][1:]:
                                        if get_rotation(ex_fig.coord, (step[0] + 25, step[1] + 10), 'Rook', black_king):
                                            new_steps[0].append(step) 
                                    for step in self.steps[1]:
                                        if ex_fig.coord == (step[0] + 25, step[1] + 10):
                                            new_steps[1].append(step)
                                    self.steps = new_steps
                                    break                            
                        elif isinstance(ex_fig, Bishop):
                            if get_rotation(ex_fig.coord, self.coord, 'Bishop', black_king):
                                cond = True
                                for b_fig in black_figures:
                                    if get_rotation(self.coord, b_fig.coord, 'Bishop', black_king):
                                        cond = False
                                        break
                                if cond:
                                    new_steps = [[(x - 25, y - 10)], [], []]
                                    for step in self.steps[0][1:]:
                                        if get_rotation(ex_fig.coord, (step[0] + 25, step[1] + 10), 'Bishop', black_king):
                                            new_steps[0].append(step) 
                                    for step in self.steps[1]:
                                        if ex_fig.coord == (step[0] + 25, step[1] + 10):
                                            new_steps[1].append(step)
                                    self.steps = new_steps
                                break                                        
                        elif isinstance(ex_fig, Queen):
                            if get_rotation(ex_fig.coord, self.coord, 'Queen', black_king):
                                cond = True
                                for b_fig in black_figures:
                                    if get_rotation(self.coord, b_fig.coord, 'Queen', black_king):
                                        cond = False
                                        break
                                if cond:                                
                                    new_steps = [[(x - 25, y - 10)], [], []]
                                    for step in self.steps[0][1:]:
                                        if get_rotation(ex_fig.coord, (step[0] + 25, step[1] + 10), 'Queen', black_king):
                                            new_steps[0].append(step) 
                                    for step in self.steps[1]:
                                        if ex_fig.coord == (step[0] + 25, step[1] + 10):
                                            new_steps[1].append(step)
                                    self.steps = new_steps
                                    break            
    def pos(self):
        SpawnAll()
        self.update_steps()       
        board.render(self.steps)
            
class King:
    def __init__(self, color, coord):
        self.color = color
        self.coord = coord
        self.move = False
        self.check = False
        self.steps = [[], []]
        self.protect_figures = []
        self.count_steps = 0
        if self.color.lower() == 'white':
            self.pic = image.load('Figures\White_King.png')
            board.wind.blit(self.pic, self.coord)
        else:
            self.pic = image.load('Figures\Black_King.png')
            board.wind.blit(self.pic, self.coord)
    def get_pos(self):
        return self.coord
    def update(self, new_coord):
        self.coord = new_coord
    def return_color(self):
        return self.color        
    def show(self):
        board.wind.blit(self.pic, self.coord)
    def update_steps(self):       
        x, y = self.coord
        self.steps = [[(x - 25, y - 10)], [], []]
        self.current_steps = [[], [], []]
        self.attack_figures = []
        self.protect_figures = []        
        self.step = []
        self.protects = []
        if self.color == 'white':
            if self.check:
                self.check_figure.update_steps()
                if dosk[self.coord] not in self.check_figure.attack_figures:
                    self.check = False
            for fig in black_figures:
                if not isinstance(fig, Pawn):
                    self.step += fig.steps[0][1:] + fig.steps[1]
                else:
                    self.step += fig.steps[2]
                self.protects += fig.protect_figures
            self.protects += black_king.protect_figures
        else:
            if self.check:
                self.check_figure.update_steps()
                if dosk[self.coord] not in self.check_figure.attack_figures:
                    self.check = False
            for fig in white_figures:
                if not isinstance(fig, Pawn):
                    self.step += fig.steps[0][1:] + fig.steps[1]
                else:
                    self.step += fig.steps[2]
                self.protects += fig.protect_figures
            self.protects += white_king.protect_figures
        for cor in [(x, y + 100), (x + 100, y - 100), (x + 100, y), (x + 100, y + 100), (x, y - 100), (x - 100 , y + 100), (x - 100, y), (x - 100, y - 100)]:
            x1, y1 = cor
            if x1 >= 25 and x1 <= 725 and y1 >= 10 and y1 <= 710:
                if dosk[x1, y1] == None:
                    if (x1 - 25, y1 - 10) not in self.step:                     
                        if self.color == 'white':
                            a, b = black_king.coord
                            if not (abs(x1 - a) + abs(y1 - b) == 100 or abs(x1 - a) * abs(y1 - b) == 10000):
                                self.steps[0].append((x1 - 25, y1 - 10))
                        else:
                            a, b = white_king.coord
                            if not (abs(x1 - a) + abs(y1 - b) == 100 or abs(x1 - a) * abs(y1 - b) == 10000):
                                self.steps[0].append((x1 - 25, y1 - 10))                            
                else:
                    if self.color == 'white':
                        if dosk[x1, y1].return_color() == 'black':
                            if dosk[x1, y1] not in self.protects:
                                self.steps[1].append((x1 - 25, y1 - 10))
                        else:
                            self.protect_figures.append(dosk[x1, y1])
                    else:
                        if dosk[x1, y1].return_color() == 'white':
                            if dosk[x1, y1] not in self.protects:
                                self.steps[1].append((x1 - 25, y1 - 10))
                        else:
                            self.protect_figures.append(dosk[x1, y1])
        if not self.check:
            if self.color == 'white':
                if not self.move:
                    if white_rook2 in figures:
                        if not white_rook2.move:
                            if dosk[(x + 100, y)] == None and dosk[(x + 200, y)] == None:
                                if (x + 75, y - 10) not in self.step and (x + 175, y - 10) not in self.step:
                                    self.steps[2].append((x + 175, y - 10))
                    if white_rook1 in figures:
                        if not white_rook1.move:
                            if dosk[(x - 100, y)] == None and dosk[(x - 200, y)] == None and dosk[(x - 300, y)] == None:
                                if (x - 125, y - 10) not in self.step and (x - 225, y - 10) not in self.step:
                                    self.steps[2].append((x - 225, y - 10))
            else:
                if not self.move:
                    if black_rook2 in figures:
                        if not black_rook2.move:
                            if dosk[(x + 100, y)] == None and dosk[(x + 200, y)] == None:
                                if (x + 75, y - 10) not in self.step and (x + 175, y - 10) not in self.step:
                                    self.steps[2].append((x + 175, y - 10))
                    if black_rook1 in figures:
                        if not black_rook1.move:
                            if dosk[(x - 100, y)] == None and dosk[(x - 200, y)] == None and dosk[(x - 300, y)] == None:
                                if (x - 125, y - 10) not in self.step and (x - 225, y - 10) not in self.step:
                                    self.steps[2].append((x - 225, y - 10))
        if self.color == 'white':
            if white_king.check:
                new_steps = [[(x - 25, y - 10)], [], []]           
                if isinstance(white_king.check_figure, Bishop):
                    for step in self.steps[0][1:]:     
                        if not get_avaible(white_king.check_figure.coord, (step[0] + 25, step[1] + 10), 'Bishop'):
                            new_steps[0].append(step)
                    for step in self.steps[1]:
                        if white_king.check_figure.coord == (step[0] + 25, step[1] + 10):
                            new_steps[1].append(step)
                elif isinstance(white_king.check_figure, Knight):
                    for step in self.steps[0][1:]:     
                        if not get_avaible(white_king.check_figure.coord, (step[0] + 25, step[1] + 10), 'Knight'):
                            new_steps[0].append(step)
                    for step in self.steps[1]:
                        if white_king.check_figure.coord == (step[0] + 25, step[1] + 10):
                            new_steps[1].append(step)
                elif isinstance(white_king.check_figure, Pawn):
                    for step in self.steps[0][1:]:     
                        if not get_avaible(white.check_figure.coord, (step[0] + 25, step[1] + 10), 'Pawn'):
                            new_steps[0].append(step)
                    for step in self.steps[1]:
                        if white_king.check_figure.coord == (step[0] + 25, step[1] + 10):
                            new_steps[1].append(step) 
                elif isinstance(white_king.check_figure, Rook):
                    for step in self.steps[0][1:]:     
                        if not get_avaible(white_king.check_figure.coord, (step[0] + 25, step[1] + 10), 'Rook'):
                            new_steps[0].append(step)
                    for step in self.steps[1]:
                        if white_king.check_figure.coord == (step[0] + 25, step[1] + 10):
                            new_steps[1].append(step)
                elif isinstance(white_king.check_figure, Queen):
                    for step in self.steps[0][1:]:     
                        if not get_avaible(white_king.check_figure.coord, (step[0] + 25, step[1] + 10), 'Queen'):
                            new_steps[0].append(step)
                    for step in self.steps[1]:
                        if white_king.check_figure.coord == (step[0] + 25, step[1] + 10):
                            new_steps[1].append(step)                    
                self.steps = new_steps
        else:
            if black_king.check:
                new_steps = [[(x - 25, y - 10)], [], []]           
                if isinstance(black_king.check_figure, Bishop):
                    for step in self.steps[0][1:]:     
                        if not get_avaible(black.check_figure.coord, (step[0] + 25, step[1] + 10), 'Bishop'):
                            new_steps[0].append(step)
                    for step in self.steps[1]:
                        if black_king.check_figure.coord == (step[0] + 25, step[1] + 10):
                            new_steps[1].append(step)
                elif isinstance(black_king.check_figure, Knight):
                    for step in self.steps[0][1:]:     
                        if not get_avaible(black_king.check_figure.coord, (step[0] + 25, step[1] + 10), 'Knight'):
                            new_steps[0].append(step)
                    for step in self.steps[1]:
                        if black_king.check_figure.coord == (step[0] + 25, step[1] + 10):
                            new_steps[1].append(step)
                elif isinstance(black_king.check_figure, Pawn):
                    for step in self.steps[0][1:]:     
                        if not get_avaible(black.check_figure.coord, (step[0] + 25, step[1] + 10), 'Pawn', 'black'):
                            new_steps[0].append(step)
                    for step in self.steps[1]:
                        if black_king.check_figure.coord == (step[0] + 25, step[1] + 10):
                            new_steps[1].append(step)                    
                elif isinstance(black_king.check_figure, Rook):
                    for step in self.steps[0][1:]:     
                        if not get_avaible(black_king.check_figure.coord, (step[0] + 25, step[1] + 10), 'Rook'):
                            new_steps[0].append(step)
                    for step in self.steps[1]:
                        if black_king.check_figure.coord == (step[0] + 25, step[1] + 10):
                            new_steps[1].append(step)
                elif isinstance(black_king.check_figure, Queen):
                    for step in self.steps[0][1:]:     
                        if not get_avaible(black_king.check_figure.coord, (step[0] + 25, step[1] + 10), 'Queen'):
                            new_steps[0].append(step)
                    for step in self.steps[1]:
                        if black_king.check_figure.coord == (step[0] + 25, step[1] + 10):
                            new_steps[1].append(step)                    
                self.steps = new_steps
    def pos(self):
        SpawnAll()
        self.update_steps()       
        board.render(self.steps, dosk[self.coord])   

def SpawnAll():
    board.wind = image.load('PS\ChessBoard.png')
    for i in figures:
        i.show()
            
def update_figures():
    for i in figures:
        i.update_steps()
    white_figures_steps = []
    black_figures_steps = []
    if white_king.check == True:
        for white_fig in white_figures + [white_king]:
            white_fig.update_steps()
            white_figures_steps += white_fig.steps[0][1:] + white_fig.steps[1]
        if len(white_figures_steps) == 0:
            black_mate.show()
    if black_king.check == True:
        for black_fig in black_figures + [black_king]:
            black_fig.update_steps()
            black_figures_steps += black_fig.steps[0][1:] + black_fig.steps[1]
        if len(black_figures_steps) == 0:
            white_mate.show()
        
def get_rotation(figure_coords, our_coords, figure, need_figure):
    x, y = our_coords
    x1, y1 = figure_coords
    x2, y2 = need_figure.coord
    if figure == 'Bishop':
        if abs(x - x2) == abs(y - y2):
            if ((x > x1 and x < x2) and (y > y1 and y < y2)) or ((x > x1 and x < x2) and (y < y1 and y > y2)) or ((x < x1 and x > x2) and (y < y1 and y > y2)) or ((x < x1 and x > x2) and (y > y1 and y < y2)):
                return True
    elif figure == 'Rook':
        if (x2 == x and y != y2) or (x2 != x and y == y2):
            if ((x == x1) and (x == x2) and (y < y1 and y > y2)) or ((x == x1) and (x == x2) and (y > y1 and y < y2)) or ((x < x1 and x > x2) and (y == y1) and (y == y2)) or ((x > x1 and x < x2) and (y == y1) and (y == y2)):
                return True
    elif figure == 'Queen':
        if abs(x - x2) == abs(y - y2):
            if ((x > x1 and x < x2) and (y > y1 and y < y2)) or ((x > x1 and x < x2) and (y < y1 and y > y2)) or ((x < x1 and x > x2) and (y < y1 and y > y2)) or ((x < x1 and x > x2) and (y > y1 and y < y2)):
                return True            
        elif (x2 == x and y != y2) or (x2 != x and y == y2):
            if ((x == x1) and (x == x2) and (y < y1 and y > y2)) or ((x == x1) and (x == x2) and (y > y1 and y < y2)) or ((x < x1 and x > x2) and (y == y1) and (y == y2)) or ((x > x1 and x < x2) and (y == y1) and (y == y2)):
                return True
            
def get_avaible(figure_coords, our_coords, figure, color = 'white'):
    x, y = our_coords
    x1, y1 = figure_coords
    if figure == 'Bishop':
        if abs(x - x1) == abs(y - y1):
            return True
    elif figure == 'Rook':
        if (x1 == x and y != y1) or (x1 != x and y == y1):
            return True
    elif figure == 'Queen':
        if (abs(x - x1) == abs(y - y1)) or ((x1 == x and y != y1) or (x1 != x and y == y1)):
            return True
    elif figure == 'Knight':
        if (abs(x - x1) == 100 and abs(y - y1) == 200) or (abs(x - x1) == 200 and abs(y - y1) == 100):
            return True
    elif figure == 'Pawn':
        if color == 'white':
            if (x == x1 - 100 and y == y1 - 100) or (x == x1 + 100 and y == y1 - 100):
                return True
        else:
            if (x == x1 - 100 and y == y1 + 100) or (x == x1 + 100 and y == y1 + 100):
                return True
                
class Menu:
    font.init()
    def __init__(self, pukts):
        self.flag = True
        self.count = 0
        self.punkts = punkts
        self.base = image.load(r'PS\board.png')
    def render(self, num_punkt = None):
        if num_punkt != None:
            for i in self.punkts:
                if i[3] == num_punkt:
                    self.base.blit(i[2], i[0])
                else:
                    self.base.blit(i[1], i[0])
        else:
            for i in self.punkts:
                self.base.blit(i[1], i[0])
    def menu(self):
        self.count += 1
        if self.count == 2:
            self.base = image.load(r'PS\board.png')
            self.punkts = [((400, 350), image.load(r'Punkts\continue.png'), image.load(r'Punkts\selected_continue.png'), 2),
                           ((400, 460), image.load(r'Punkts\quit.png'), image.load(r'Punkts\selected_quit.png'), 1)]
        flag = True
        punkt = None
        while flag:
            mousepos = mouse.get_pos()
            if_punkt = False
            for i in self.punkts:
                if mousepos[0] > i[0][0] and mousepos[0] < i[0][0] + 344 and mousepos[1] > i[0][1] and mousepos[1] < i[0][1] + 100:
                    punkt = i[3]
                    if_punkt = True
                    break
                else:
                    if_punkt = False
                    punkt = None
            if if_punkt:
                self.render(punkt)
            else:
                self.render()
            for e in event.get():
                if e.type == QUIT:
                    exit()
                elif e.type == KEYDOWN:
                    if e.key == K_ESCAPE:
                        exit()
                if e.type == MOUSEBUTTONDOWN and e.button == 1:
                    if punkt != None:
                        if punkt == 0:
                            self.base = image.load(r'PS\board.png')
                            self.base.blit(image.load(r'Punkts\selected_new_game.png'), (400, 350))
                            if gamemode.select() == True:
                                flag = False
                            else:
                                self.base = image.load(r'PS\board.png')
                                self.base.blit(image.load(r'Punkts\selected_new_game.png'), (400, 350))
                        elif punkt == 1:
                            exit()
                        elif punkt == 2:
                            flag = False
            window.blit(self.base, (0, 0))
            display.flip()
            
class GameModeSelect:
    def __init__(self, punkts):
        self.flag = True
        self.punkts = punkts
        self.flag = False
    def render(self, num_punkt = None):
        if num_punkt != None:
            for i in self.punkts:
                if i[3] == num_punkt:
                    game.base.blit(i[2], i[0])
                else:
                    game.base.blit(i[1], i[0])
        else:
            for i in self.punkts:
                game.base.blit(i[1], i[0])
    def select(self):
        flag = True
        punkt = None
        while flag:
            mousepos = mouse.get_pos()
            if_punkt = False
            for i in self.punkts:
                if mousepos[0] > i[0][0] and mousepos[0] < i[0][0] + 322 and mousepos[1] > i[0][1] and mousepos[1] < i[0][1] + 90:
                    punkt = i[3]
                    if_punkt = True
                    break
                else:
                    if_punkt = False
                    punkt = None
            if if_punkt:
                self.render(punkt)
            else:
                self.render()
            for e in event.get():
                if e.type == QUIT:
                    exit()
                if e.type == MOUSEBUTTONDOWN and e.button == 1:
                    if punkt != None:
                        if punkt == 0:
                            board.mode = True
                            game.base = image.load(r'PS\board.png')
                            game.base.blit(image.load(r'Punkts\selected_new_game.png'), (400, 350))      
                            game.base.blit(image.load(r'Punkts\selected_one_player.png'), (410, 470))
                            if colormode.select() == False:                             
                                game.base = image.load(r'PS\board.png')
                                game.base.blit(image.load(r'Punkts\selected_new_game.png'), (400, 350))      
                                game.base.blit(image.load(r'Punkts\selected_one_player.png'), (410, 470))                                
                            else:
                                return True
                        elif punkt == 1:
                            return True
                    else:
                        return False
                    
            window.blit(game.base, (0, 0))
            display.flip()
        
class ColorModeSelect:
    def __init__(self, punkts):
        self.flag = True
        self.punkts = punkts
        self.flag = False
    def render(self, num_punkt = None):
        if num_punkt != None:
            for i in self.punkts:
                if i[3] == num_punkt:
                    game.base.blit(i[2], i[0])
                else:
                    game.base.blit(i[1], i[0])
        else:
            for i in self.punkts:
                game.base.blit(i[1], i[0])
    def select(self):
        flag = True
        punkt = None
        while flag:
            mousepos = mouse.get_pos()
            if_punkt = False
            for i in self.punkts:
                if mousepos[0] > i[0][0] and mousepos[0] < i[0][0] + 300 and mousepos[1] > i[0][1] and mousepos[1] < i[0][1] + 80:
                    punkt = i[3]
                    if_punkt = True
                    break
                else:
                    if_punkt = False
                    punkt = None
            if if_punkt:
                self.render(punkt)
            else:
                self.render()
            for e in event.get():
                if e.type == QUIT:
                    exit()
                if e.type == MOUSEBUTTONDOWN and e.button == 1:
                    if punkt != None:
                        if punkt == 0:                         
                            board.player_color = 'white'
                            return True
                        elif punkt == 1:
                            board.player_color = 'black'
                            return True
                    else:
                        return False
                    
            window.blit(game.base, (0, 0))
            display.flip()
        
class WhiteFigurSelect:
    def __init__(self, punkts):
        self.punkts = punkts
        self.base = image.load(r'PS\figurselect.png')
        self.base1 = image.load(r'PS\selectbase.png')
    def render(self, num_punkt = None):
        if num_punkt != None:
            for i in self.punkts:
                if i[3] == num_punkt:
                    self.base.blit(i[2], i[0])
                else:
                    self.base.blit(i[1], i[0])
        else:
            for i in self.punkts:
                self.base.blit(i[1], i[0])
    def select(self):
        flag = True
        punkt = None
        count = 0
        while flag:
            mousepos = mouse.get_pos()
            if_punkt = False
            for i in self.punkts:
                if mousepos[0] > i[0][0] and mousepos[0] < i[0][0] + 123 and mousepos[1] > i[0][1] and mousepos[1] < i[0][1] + 200:
                    punkt = i[3]
                    if_punkt = True
                    break
                else:
                    if_punkt = False
                    punkt = None
            if if_punkt:
                self.render(punkt)
            else:
                self.render()
                
            for e in event.get():
                if e.type == QUIT:
                    exit()
                    
                if e.type == MOUSEBUTTONDOWN and e.button == 1:
                    if punkt != None:
                        if punkt == 0:
                            return 1
                        elif punkt == 1:
                            return 2
                        elif punkt == 2:
                            return 3
                        elif punkt == 3:
                            return 4
                        
            if count == 0:
                window.blit(self.base1, (0, 0))
                count += 1
            window.blit(self.base, (0, 0))
            display.flip()
            
class BlackFigurSelect:
    def __init__(self, punkts):
        self.punkts = punkts
        self.base = image.load(r'PS\figurselect.png')
        self.base1 = image.load(r'PS\selectbase.png')
    def render(self, num_punkt = None):
        if num_punkt != None:
            for i in self.punkts:
                if i[3] == num_punkt:
                    self.base.blit(i[2], i[0])
                else:
                    self.base.blit(i[1], i[0])
        else:
            for i in self.punkts:
                self.base.blit(i[1], i[0])
    def select(self):
        flag = True
        punkt = None
        count = 0
        while flag:
            mousepos = mouse.get_pos()
            if_punkt = False
            for i in punkts:
                if mousepos[0] > i[0][0] and mousepos[0] < i[0][0] + 123 and mousepos[1] > i[0][1] and mousepos[1] < i[0][1] + 200:
                    punkt = i[3]
                    if_punkt = True
                    break
                else:
                    if_punkt = False
                    punkt = None
            if if_punkt:
                self.render(punkt)
            else:
                self.render()
                
            for e in event.get():
                if e.type == QUIT:
                    exit()
                    if e.type == MOUSEBUTTONDOWN and e.button == 1:
                        if punkt != None:
                            if punkt == 0:
                                return 1
                            elif punkt == 1:
                                return 2
                            elif punkt == 2:
                                return 3
                            elif punkt == 3:
                                return 4                
            if count == 0:
                window.blit(self.base1, (0, 0))
            window.blit(self.base, (0, 0))
            display.flip()
            
class Mate:
    def __init__(self, color):
        self.punkts = [((250, 650), image.load(r'Punkts\quit.png'), image.load(r'Punkts\selected_quit.png'), 0)]
        if color == 'white':
            self.base = image.load(r'PS\white_mate.png')
        elif color == 'black':
            self.base = image.load(r'PS\black_mate.png')
    def render(self, num_punkt = None):
        if num_punkt != None:
            for i in self.punkts:
                if i[3] == num_punkt:
                    self.base.blit(i[2], i[0])
                else:
                    self.base.blit(i[1], i[0])
        else:
            for i in self.punkts:
                self.base.blit(i[1], i[0])
    def show(self):
        flag = True
        punkt = None
        count = 0
        while flag:
            mousepos = mouse.get_pos()
            if_punkt = False
            for i in self.punkts:
                if mousepos[0] > i[0][0] and mousepos[0] < i[0][0] + 344 and mousepos[1] > i[0][1] and mousepos[1] < i[0][1] + 100:
                    punkt = i[3]
                    if_punkt = True
                    break
                else:
                    if_punkt = False
                    punkt = None
            if if_punkt:
                self.render(punkt)
            else:
                self.render()
                
            for e in event.get():
                if e.type == QUIT:
                    exit()
                if e.type == MOUSEBUTTONDOWN and e.button == 1:
                    if punkt != None:
                        if punkt == 0:
                            sys.exit()
            window.blit(self.base, (0, 0))
            display.flip()    
        
def pawn_counts():
    for pawn in [black_pawn1, black_pawn2, black_pawn3, black_pawn4, black_pawn5, black_pawn6, black_pawn7, black_pawn8, white_pawn1, white_pawn2, white_pawn3, white_pawn4, white_pawn5, white_pawn6, white_pawn7, white_pawn8]:
        if pawn.steps_count == 1:
            pawn.steps_count += 1
            
class ActiveColor:
    def __init__(self):
        self.color = 'white'
    def change(self):
        if self.color == 'white':
            self.color = 'black'
        else:
            self.color = 'white'
        if board.mode:
            if self.color != board.player_color:
                if board.player_color == 'white':
                    all_steps = [[], []]
                    for figur in black_figures + [black_king]:
                        all_steps[0] += figur.steps[0][1:]
                        all_steps[1] += figur.steps[1]
                    ai_step = random.choice(all_steps[0] + all_steps[1])
                    ai_figure = None
                    if ai_step in all_steps[0]:
                        ai_eat = False
                    elif ai_step in all_steps[1]:
                        ai_eat = True
                    for figur in black_figures:
                        if ai_step in figur.steps[0] + figur.steps[1]:
                            ai_figure = figur
                    if not ai_eat:
                        if isinstance(ai_figure, King) and ai_step in ai_figure.steps[2]:
                            if ai_step[0] == 625:
                                dosk[black_rook2.coord] = None
                                black_rook2.coord = (ai_figure.coord[0] - 100, ai_figure.coord[1])
                                dosk[black_rook2.coord] = black_rook2
                            elif ai_ste[0] == 225:
                                dosk[black_rook1.coord] = None
                                black_rook1.coord = (ai_figure.coord[0] + 100, ai_figure.coord[1])
                                dosk[black_rook1.coord] = black_rook1
                        dosk[ai_figure.coord] = None
                        dosk[(ai_step[0] + 25, ai_step[1] + 10)] = ai_figure
                        ai_figure.coord = (ai_step[0] + 25, ai_step[1] + 10)
                        ai_figure.move = True
                        pawn_counts()
                        if isinstance(ai_figure, Pawn):
                            ai_figure.steps_count += 1
                        update_figures()
                        SpawnAll()
                    else:
                        if dosk[(ai_step[0] + 25, ai_step[1] + 10)] in figures:
                            del figures[figures.index(dosk[(ai_step[0] + 25, ai_step[1] + 10)])]
                            del white_figures[white_figures.index(dosk[(ai_step[0] + 25, ai_step[1] + 10)])]
                        dosk[ai_figure.coord] = None
                        dosk[(ai_step[0] + 25, ai_step[1] + 10)] = ai_figure
                        ai_figure.coord = (ai_step[0] + 25, ai_step[1] + 10)
                        ai_figure.move = True
                        pawn_counts()
                        update_figures()
                        SpawnAll()
                    self.color = 'white'
                else:
                    all_steps = [[], []]
                    for figur in white_figures + [white_king]:
                        all_steps[0] += figur.steps[0][1:]
                        all_steps[1] += figur.steps[1]
                    ai_step = random.choice(all_steps[0] + all_steps[1])
                    ai_figure = None
                    if ai_step in all_steps[0]:
                        ai_eat = False
                    elif ai_step in all_steps[1]:
                        ai_eat = True
                    for figur in white_figures:
                        if ai_step in figur.steps[0] + figur.steps[1]:
                            ai_figure = figur
                    if not ai_eat:
                        if isinstance(ai_figure, King) and ai_step in ai_figure.steps[2]:
                            if ai_step[0] == 625:
                                dosk[white_rook2.coord] = None
                                white_rook2.coord = (ai_figure.coord[0] - 100, ai_figure.coord[1])
                                dosk[white_rook2.coord] = white_rook2
                            elif ai_ste[0] == 225:
                                dosk[white_rook1.coord] = None
                                white_rook1.coord = (ai_figure.coord[0] + 100, ai_figure.coord[1])
                                dosk[white_rook1.coord] = white_rook1
                        dosk[ai_figure.coord] = None
                        dosk[(ai_step[0] + 25, ai_step[1] + 10)] = ai_figure
                        ai_figure.coord = (ai_step[0] + 25, ai_step[1] + 10)
                        ai_figure.move = True
                        pawn_counts()
                        if isinstance(ai_figure, Pawn):
                            ai_figure.steps_count += 1
                        update_figures()
                        SpawnAll()
                    else:
                        if dosk[(ai_step[0] + 25, ai_step[1] + 10)] in figures:
                            del figures[figures.index(dosk[(ai_step[0] + 25, ai_step[1] + 10)])]
                            del black_figures[black_figures.index(dosk[(ai_step[0] + 25, ai_step[1] + 10)])]
                        dosk[ai_figure.coord] = None
                        dosk[(ai_step[0] + 25, ai_step[1] + 10)] = ai_figure
                        ai_figure.coord = (ai_step[0] + 25, ai_step[1] + 10)
                        ai_figure.move = True
                        pawn_counts()
                        update_figures()
                        SpawnAll()
                    self.color = 'black'                    
                        
                        
window = display.set_mode((800, 800))
display.set_caption('Chess Master')
            
coords = {'a8': (25, 10),  'b8': (125, 10),  'c8': (225, 10),  'd8': (325, 10),  'e8': (425, 10),  'f8': (525, 10),  'g8': (625, 10),  'h8': (725, 10),
          'a7': (25, 110), 'b7': (125, 110), 'c7': (225, 110), 'd7': (325, 110), 'e7': (425, 110), 'f7': (525, 110), 'g7': (625, 110), 'h7': (725, 110),
          'a6': (25, 210), 'b6': (125, 210), 'c6': (225, 210), 'd6': (325, 210), 'e6': (425, 210), 'f6': (525, 210), 'g6': (625, 210), 'h6': (725, 210),
          'a5': (25, 310), 'b5': (125, 310), 'c5': (225, 310), 'd5': (325, 310), 'e5': (425, 310), 'f5': (525, 310), 'g5': (625, 310), 'h5': (725, 310),
          'a4': (25, 410), 'b4': (125, 410), 'c4': (225, 410), 'd4': (325, 410), 'e4': (425, 410), 'f4': (525, 410), 'g4': (625, 410), 'h4': (725, 410),
          'a3': (25, 510), 'b3': (125, 510), 'c3': (225, 510), 'd3': (325, 510), 'e3': (425, 510), 'f3': (525, 510), 'g3': (625, 510), 'h3': (725, 510),
          'a2': (25, 610), 'b2': (125, 610), 'c2': (225, 610), 'd2': (325, 610), 'e2': (425, 610), 'f2': (525, 610), 'g2': (625, 610), 'h2': (725, 610),
          'a1': (25, 710), 'b1': (125, 710), 'c1': (225, 710), 'd1': (325, 710), 'e1': (425, 710), 'f1': (525, 710), 'g1': (625, 710), 'h1': (725, 710)}

board = Board()
board.wind = image.load('PS\ChessBoard.png')
white_rook1 = Rook('white', coords['a1'])
white_rook2 = Rook('white', coords['h1'])
black_rook1 = Rook('black', coords['a8'])
black_rook2 = Rook('black', coords['h8'])
white_bishop1 = Bishop('white', coords['c1'])
white_bishop2 = Bishop('white', coords['f1'])
black_bishop1 = Bishop('black', coords['c8'])
black_bishop2 = Bishop('black', coords['f8'])
white_king = King('white', coords['e1'])
black_king = King('black', coords['e8'])
white_queen = Queen('white', coords['d1'])
black_queen = Queen('black', coords['d8'])
white_knight1 = Knight('white', coords['b1'])
white_knight2 = Knight('white', coords['g1'])
black_knight1 = Knight('black', coords['b8'])
black_knight2 = Knight('black', coords['g8'])
white_pawn1 = Pawn('white', coords['a2'])
white_pawn2 = Pawn('white', coords['b2'])
white_pawn3 = Pawn('white', coords['c2'])
white_pawn4 = Pawn('white', coords['d2'])
white_pawn5 = Pawn('white', coords['e2'])
white_pawn6 = Pawn('white', coords['f2'])
white_pawn7 = Pawn('white', coords['g2'])
white_pawn8 = Pawn('white', coords['h2'])
black_pawn1 = Pawn('black', coords['a7'])
black_pawn2 = Pawn('black', coords['b7'])
black_pawn3 = Pawn('black', coords['c7'])
black_pawn4 = Pawn('black', coords['d7'])
black_pawn5 = Pawn('black', coords['e7'])
black_pawn6 = Pawn('black', coords['f7'])
black_pawn7 = Pawn('black', coords['g7'])
black_pawn8 = Pawn('black', coords['h7'])

count = 0
spawn = False
active_color = ActiveColor()
block_white = False
block_black = False

dosk = {(25, 10):black_rook1,  (125, 10):black_knight1,  (225, 10):black_bishop1,  (325, 10):black_queen,  (425, 10):black_king,   (525, 10):black_bishop2,  (625, 10):black_knight2,  (725, 10):black_rook2, 
        (25, 110):black_pawn1, (125, 110):black_pawn2,   (225, 110):black_pawn3,   (325, 110):black_pawn4, (425, 110):black_pawn5, (525, 110):black_pawn6,   (625, 110):black_pawn7,   (725, 110):black_pawn8,
        (25, 210):None,        (125, 210):None,          (225, 210):None,          (325, 210):None,        (425, 210):None,        (525, 210):None,          (625, 210):None,          (725, 210):None,
        (25, 310):None,        (125, 310):None,          (225, 310):None,          (325, 310):None,        (425, 310):None,        (525, 310):None,          (625, 310):None,          (725, 310):None,
        (25, 410):None,        (125, 410):None,          (225, 410):None,          (325, 410):None,        (425, 410):None,        (525, 410):None,          (625, 410):None,          (725, 410):None, 
        (25, 510):None,        (125, 510):None,          (225, 510):None,          (325, 510):None,        (425, 510):None,        (525, 510):None,          (625, 510):None,          (725, 510):None,
        (25, 610):white_pawn1, (125, 610):white_pawn2,   (225, 610):white_pawn3,   (325, 610):white_pawn4, (425, 610):white_pawn5, (525, 610):white_pawn6,   (625, 610):white_pawn7,   (725, 610):white_pawn8,
        (25, 710):white_rook1, (125, 710):white_knight1, (225, 710):white_bishop1, (325, 710):white_queen, (425, 710):white_king,  (525, 710):white_bishop2, (625, 710):white_knight2, (725, 710):white_rook2 }

black_figures = [black_pawn1, black_pawn2, black_pawn3, black_pawn4, black_pawn5, black_pawn6, black_pawn7, black_pawn8, black_bishop1, black_bishop2, black_knight1, black_knight2, black_rook1, black_rook2, black_queen]
white_figures = [white_pawn1, white_pawn2, white_pawn3, white_pawn4, white_pawn5, white_pawn6, white_pawn7, white_pawn8, white_bishop1, white_bishop2, white_knight1, white_knight2, white_rook1, white_rook2, white_queen]
figures = white_figures + black_figures + [white_king, black_king]

for figur in figures:
    figur.update_steps()
    
punkts = [((400, 350), image.load(r'Punkts\new_game.png'), image.load(r'Punkts\selected_new_game.png'), 0),
          ((400, 460), image.load(r'Punkts\quit.png'), image.load(r'Punkts\selected_quit.png'), 1)]

punkts2 = [[((40, 380), image.load(r'Figures\select_whiterook.png'), image.load(r'Figures\selected_whiterook.png'), 0),
            ((230, 380), image.load(r'Figures\select_whitequeen.png'), image.load(r'Figures\selected_whitequeen.png'), 1),
            ((450, 380), image.load(r'Figures\select_whiteknight.png'), image.load(r'Figures\selected_whiteknight.png'), 2),
            ((640, 380), image.load(r'Figures\select_whitebishop.png'), image.load(r'Figures\selected_whitebishop.png'), 3)],
           [((40, 380), image.load(r'Figures\select_blackrook.png'), image.load(r'Figures\selected_blackrook.png'), 0),
            ((230, 380), image.load(r'Figures\select_blackqueen.png'), image.load(r'Figures\selected_blackqueen.png'), 1),
            ((450, 380), image.load(r'Figures\select_blackknight.png'), image.load(r'Figures\selected_blackknight.png'), 2),
            ((640, 380), image.load(r'Figures\select_blackbishop.png'), image.load(r'Figures\selected_blackbishop.png'), 3)]]

punkts3 = [((410, 470), image.load(r'Punkts\one_player.png'), image.load(r'Punkts\selected_one_player.png'), 0),
           ((410, 570), image.load(r'Punkts\two_players.png'), image.load(r'Punkts\selected_two_players.png'), 1)]

punkts4 = [((420, 570), image.load(r'Punkts\white.png'), image.load(r'Punkts\selected_white.png'), 0),
           ((420, 660), image.load(r'Punkts\black.png'), image.load(r'Punkts\selected_black.png'), 1)]

colormode = ColorModeSelect(punkts4)

gamemode = GameModeSelect(punkts3)

game = Menu(punkts)
game.menu()

white_select = WhiteFigurSelect(punkts2[0])
black_select = WhiteFigurSelect(punkts2[1])
white_mate = Mate('white')
black_mate = Mate('black')

game_flag = True
while game_flag:
   
    for e in event.get():
        if e.type == QUIT:
            sys.exit()
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                game.menu()
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 1:                
                mp = mouse.get_pos()
                for i in dosk:
                    f = False
                    if mp[0] > i[0] - 25 and mp[0] < i[0] + 75 and mp[1] > i[1] - 10 and mp[1] < i[1] + 90:
                        if dosk[i] != None or (i[0] - 25, i[1] - 10) in active_figure.steps[1]:
                            if not spawn:
                                if dosk[i].color == active_color.color:
                                    active_figure = dosk[i]
                                    active_figure_pos = i
                                    dosk[i].pos()
                                    spawn = True
                            elif (i[0] - 25, i[1] - 10) in active_figure.steps[1]:
                                if isinstance(active_figure, Pawn) and (i[1] == 10 or i[1] == 710):
                                    del figures[figures.index(dosk[i])]
                                    if dosk[i].color == 'white':
                                        del white_figures[white_figures.index(dosk[i])]
                                    else:
                                        del black_figures[black_figures.index(dosk[i])]                                    
                                    dosk[active_figure.coord] = None
                                    active_figure.coord = i
                                    dosk[i] = active_figure
                                    if active_figure.color == 'white':
                                        del figures[figures.index(dosk[i])]
                                        del white_figures[white_figures.index(dosk[i])]
                                        act_figure = white_select.select()
                                        if act_figure == 1:
                                            active_figure = Rook('white', i)
                                        elif act_figure == 2:
                                            active_figure = Queen('white', i)
                                        elif act_figure == 3:
                                            active_figure = Knight('white', i)
                                        elif act_figure == 4:
                                            active_figure = Bishop('white', i)
                                        white_figures.append(active_figure)
                                    else:
                                        del figures[figures.index(dosk[i])]
                                        del black_figures[black_figures.index(dosk[i])]
                                        act_figure = black_select.select()
                                        if act_figure == 1:
                                            active_figure = Rook('black', i)
                                        elif act_figure == 2:
                                            active_figure = Queen('black', i)
                                        elif act_figure == 3:
                                            active_figure = Knight('black', i)
                                        elif act_figure == 4:
                                            active_figure = Bishop('black', i)
                                        black_figures.append(active_figure)                                            
                                    dosk[i] = active_figure
                                    figures.append(active_figure)
                                    spawn = False
                                    active_color.change()
                                    update_figures()
                                    SpawnAll()
                                    pawn_counts()
                                elif dosk[i] == None:
                                    if active_figure.color == 'white':
                                        del figures[figures.index(dosk[(i[0], i[1] + 100)])]
                                        del black_figures[black_figures.index(dosk[i[0], i[1] + 100])]
                                        dosk[(i[0], i[1] + 100)] = None
                                    else:
                                        del figures[figures.index(dosk[(i[0], i[1] - 100)])]
                                        del white_figures[white_figures.index(dosk[(i[0], i[1] - 100)])]
                                        dosk[(i[0], i[1] - 100)] = None
                                    dosk[active_figure.coord] = None
                                    dosk[i] = active_figure
                                    active_figure.coord = i
                                    active_figure.move = True
                                    spawn = False
                                    active_color.change()
                                    update_figures()
                                    SpawnAll()
                                    pawn_counts()
                                else:
                                    del figures[figures.index(dosk[i])]
                                    if active_figure.color == 'white':
                                        if white_king.check:
                                            if dosk[i] == white_king.check_figure:
                                                white_king.check = False
                                    else:
                                        if black_king.check:
                                            if dosk[i] == black_king.check_figure:
                                                black_king.check = False
                                    if dosk[i].color == 'white':
                                        del white_figures[white_figures.index(dosk[i])]
                                    else:
                                        del black_figures[black_figures.index(dosk[i])]
                                    dosk[i] = active_figure
                                    dosk[active_figure.coord] = None
                                    active_figure.coord = i
                                    active_figure.move = True
                                    spawn = False
                                    active_color.change()
                                    update_figures()
                                    SpawnAll()
                                    pawn_counts()
                            else:
                                if dosk[i].color == active_color.color:
                                    active_figure = dosk[i]
                                    active_figure_pos = i
                                    dosk[i].pos()
                                    spawn = True            
                        else:
                            if spawn:
                                if (i[0] - 25, i[1] - 10) in active_figure.steps[0][1:]:
                                    if isinstance(active_figure, Pawn):
                                        if (i[1] == 10 or i[1] == 710):
                                            dosk[active_figure.coord] = None
                                            active_figure.coord = i
                                            dosk[i] = active_figure
                                            if active_figure.color == 'white':
                                                del figures[figures.index(dosk[i])]
                                                del white_figures[white_figures.index(dosk[i])]
                                                act_figure = white_select.select()
                                                if act_figure == 1:
                                                    active_figure = Rook('white', i)
                                                elif act_figure == 2:
                                                    active_figure = Queen('white', i)
                                                elif act_figure == 3:
                                                    active_figure = Knight('white', i)
                                                elif act_figure == 4:
                                                    active_figure = Bishop('white', i)
                                                white_figures.append(active_figure)
                                            else:
                                                del figures[figures.index(dosk[i])]
                                                del black_figures[black_figures.index(dosk[i])]
                                                act_figure = black_select.select()
                                                if act_figure == 1:
                                                    active_figure = Rook('black', i)
                                                elif act_figure == 2:
                                                    active_figure = Queen('black', i)
                                                elif act_figure == 3:
                                                    active_figure = Knight('black', i)
                                                elif act_figure == 4:
                                                    active_figure = Bishop('black', i)
                                                black_figures.append(active_figure)                                            
                                            dosk[i] = active_figure
                                            figures.append(active_figure)
                                            spawn = False
                                            active_color.change()
                                            update_figures()
                                            SpawnAll()
                                            pawn_counts()
                                        else:
                                            active_figure.coord = i
                                            dosk[active_figure_pos] = None
                                            dosk[active_figure.coord] = active_figure
                                            pawn_counts()
                                            if isinstance(active_figure, Pawn):
                                                active_figure.steps_count += 1
                                            active_figure.move = True
                                            spawn = False
                                            active_color.change()
                                            update_figures()
                                            SpawnAll()
                                    else:
                                        active_figure.coord = i
                                        dosk[active_figure_pos] = None
                                        dosk[active_figure.coord] = active_figure
                                        active_figure.move = True
                                        spawn = False
                                        active_color.change()
                                        update_figures()
                                        pawn_counts()
                                        SpawnAll()
                                elif isinstance(active_figure, King):
                                    if (i[0] - 25, i[1] - 10) in active_figure.steps[2]:
                                        if active_figure.color == 'white':
                                            if i == (625, 710):
                                                dosk[white_king.coord] = None
                                                white_king.coord = i
                                                dosk[white_king.coord] = white_king
                                                dosk[white_rook2.coord] = None
                                                dosk[(i[0] - 100, i[1])] = white_rook2
                                                white_rook2.coord = (i[0] - 100, i[1])
                                                SpawnAll()
                                                white_king.move = True
                                                white_rook2.move = True                                                
                                                update_figures()
                                                spawn = False
                                                pawn_counts()
                                            else:
                                                dosk[white_king.coord] = None
                                                white_king.coord = i
                                                dosk[white_king.coord] = white_king
                                                dosk[white_rook1.coord] = None
                                                dosk[(i[0] + 100, i[1])] = white_rook1
                                                white_rook1.coord = (i[0] + 100, i[1])
                                                SpawnAll()
                                                white_king.move = True
                                                white_rook1.move = True                                                
                                                update_figures()
                                                spawn = False
                                                pawn_counts()
                                        else:
                                            if i == (625, 10):
                                                dosk[black_king.coord] = None
                                                black_king.coord = i
                                                dosk[black_king.coord] = black_king
                                                dosk[black_rook2.coord] = None
                                                dosk[(i[0] - 100, i[1])] = black_rook2
                                                black_rook2.coord = (i[0] - 100, i[1])
                                                SpawnAll()
                                                black_king.move = True
                                                black_rook2.move = True                                                
                                                update_figures()
                                                spawn = False
                                                pawn_counts()
                                            elif i == (225, 710):
                                                dosk[black_king.coord] = None
                                                black_king.coord = i
                                                dosk[black_king.coord] = black_king
                                                dosk[black_rook1.coord] = None
                                                dosk[(i[0] + 100, i[1])] = black_rook1
                                                black_rook1.coord = (i[0] + 100, i[1])
                                                SpawnAll()
                                                black_king.move = True
                                                black_rook1.move = True                                                
                                                update_figures()
                                                spawn = False
                                                pawn_counts()
                                        active_color.change()
                                    else:
                                        spawn = False
                                        SpawnAll()
                                else:                                 
                                    spawn = False
                                    SpawnAll()
                            
    window.blit(board.wind, (0, 0))
    display.flip()