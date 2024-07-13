import random
import pandas as pd
import os
import sys
import pygame
from pygame.locals import *

class ChartGame:
    def __init__(self,dirpath):
        self.dirpath = dirpath
        self.csv_files=os.listdir(self.dirpath)
        self.candle_width=10
        self.start_money=8_000
        
    def new_chart(self):
        filename=random.choice(self.csv_files)
        file=self.dirpath+"/"+filename
        df = pd.read_csv(file)
        df["Open"]=df["Open"]/max(df["Open"])
        df["Adj Close"]=df["Adj Close"]/max(df["Adj Close"])
        self.current_df=df
        
        self.close_min=min(self.current_df["Adj Close"][:len(self.current_df)//2])
        self.close_max=max(self.current_df["Adj Close"][:len(self.current_df)//2])
        
        self.money=self.start_money
        self.invested=0
        self.buy_price=0
        self.day=0
        self.current_price=0
        self.stock=filename.split(".")[0]
        self.shift=[0,0]
        self.zoom=4
        self.investment_days=0
        
    def save_score(self):
        file=open("scores.txt","a")
        file.write(str(round(self.money,2))+" "+str(self.day)+" "+str(self.start_money)+"\n")
        file.close()
        
    def end_game(self):
        self.sell()
        self.save_score()
        self.new_chart()
    
    def buy(self,n=-1):
        if self.invested==0:
            if n<0: n=self.money
            self.invested=n
            self.money-=n
            self.buy_price = self.current_price
    
    def sell(self):
        if self.invested!=0:
            self.money+=self.invested*(self.current_price/self.buy_price)
            self.invested=0
            self.buy_price=0
    
    def new_day(self,n=1):
        if self.day+n>=len(self.current_df)//2:
            self.end_game()
        else:
            self.close_min=min(self.current_df["Adj Close"][:len(self.current_df)//2+self.day])
            self.close_max=max(self.current_df["Adj Close"][:len(self.current_df)//2+self.day])
            self.day+=n
            if self.invested!=0:
                self.investment_days+=n
    
    def update(self):
        chart_size=len(self.current_df)//2+self.day
        
        Open_0=self.current_df["Open"][0]
        Close_0=self.current_df["Adj Close"][0]
        Sized_Open_0=Open_0*self.zoom
        previous_p2 = (self.shift[0],height-Sized_Open_0+self.shift[1]+self.close_min*self.zoom)
        
        for i in range(1,chart_size):
            #Date=self.current_df["Date"][i]
            Close=self.current_df["Adj Close"][i]
            Sized_Close=Close*self.zoom
            
            p1=previous_p2
            p2=(i*self.candle_width+self.shift[0],height-Sized_Close+self.shift[1]+self.close_min*self.zoom)
            
            color=(0,255,0)
            if p1[1] < p2[1]:
                color=(255,0,0)
                
            pygame.draw.line(screen,color,p1,p2,2)
            previous_p2=p2
            self.current_price=Close
        
        i=0
        d=(self.close_max-self.close_min)
        color=(0,0,0)
        while i<d:
            y=height-i*self.zoom+self.shift[1]
            
            p1=(width-20,y)
            p2=(width-10,y)
            pygame.draw.line(screen,color,p1,p2)
            
            text_surface = font_small.render(str(round(i+self.close_min,2)), False, (0, 0, 0))
            screen.blit(text_surface, (width-40,y))
            
            i+=d/50
        
        if self.invested!=0:
            color=(0,255,0)
            if self.current_price<self.buy_price:
                color=(255,0,0)
            Sized_buyprice=self.buy_price*self.zoom
            p1=(0,height-Sized_buyprice+self.shift[1]+self.close_min*self.zoom)
            p2=(width,height-Sized_buyprice+self.shift[1]+self.close_min*self.zoom)
            pygame.draw.line(screen,color,p1,p2)
        

def display_text(s,pos):
    text_surface = font.render(s, False, (0, 0, 0))
    screen.blit(text_surface, pos)

game = ChartGame("chart_data")
game.new_chart()
game.zoom=20

pygame.init()
pygame.font.init()

font = pygame.font.SysFont('Arial', 30)
font_small = pygame.font.SysFont('Arial', 10)
currency="$"

fps = 60
fpsClock = pygame.time.Clock()
 
width, height = 1280, 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('STOCKS')

drag=False
drag_start=(0,0)
drag_end=(0,0)

NUMPAD_KEYS = {K_KP0:'0', K_KP1:'1', K_KP2:'2', K_KP3:'3', K_KP4:'4', K_KP5:'5', K_KP6:'6', K_KP7:'7', K_KP8:'8', K_KP9:'9'}
invest_string=""
invest_input=False
# Game loop.
while True:
    screen.fill((245, 245, 245))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONUP:
            drag=False
        if event.type == pygame.MOUSEWHEEL:
            if not (game.zoom<=4 and event.y==-1):
                game.zoom+=event.y*200
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                game.new_day()
            if event.key == pygame.K_UP:
                game.candle_width*=1.5
            if event.key == pygame.K_DOWN:
                game.candle_width/=1.5
            if event.key == pygame.K_b:
                game.buy()
            if event.key == pygame.K_s:
                game.sell()
            if event.key == pygame.K_n:
                game.end_game()
            if event.key == pygame.K_f:
                game.new_day(15)
                game.shift[0]=-game.candle_width*(len(game.current_df)//2+game.day)+width/4
            if event.key == pygame.K_SPACE:
                game.shift[0]=-game.candle_width*(len(game.current_df)//2+game.day)+width/4
            if event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()
            if event.key in NUMPAD_KEYS.keys():
                if invest_input==False:
                    invest_input=True
                
                if invest_string.isnumeric()==False:
                    invest_string=""
                invest_string+=NUMPAD_KEYS[event.key]
            if event.key == pygame.K_BACKSPACE:
                invest_string=invest_string[:-1]
            if event.key in (pygame.K_KP_ENTER,pygame.K_RETURN):
                if invest_input:
                    if invest_string.isnumeric()==True:
                        amount=int(invest_string)
                        if amount <= game.money:
                            game.buy(amount)
                            invest_string=""
                            invest_input=False
                        else:
                            invest_string="NOT ENOUGH MONEY"
        
        if pygame.mouse.get_focused()==1:
            try:
                if drag==False:
                    drag_start=event.pos
                    drag=True
                if(pygame.mouse.get_pressed()[0]):
                    game.shift[0]+=(event.pos[0]-drag_start[0])/1.1
                elif(pygame.mouse.get_pressed()[2]):
                    game.shift[1]+=(event.pos[1]-drag_start[1])/1.1
                drag_start=event.pos
            except:
                pass
            #game.shift[1]+=(event.pos[1]-drag_start[1])/1.1
            
    to_print=[
            f"INVESTED: {currency} "+str(round(game.invested,2)),
            "DAYS LEFT: "+str(len(game.current_df)//2-game.day),
            "DAY: "+str(game.day),
            "IVESTMENT DAYS: "+str(game.investment_days),
            "STOCK: "+str(game.stock)]
    
    display_text(f"{currency} "+str(round(game.money,2)),(0,0))
    if invest_input:
        display_text("Investing: "+invest_string,(0,30))
    else:
        for i in range(0,len(to_print)):
            s=to_print[i]
            display_text(s,(0,(1+i)*30))
    
    game.update()
    pygame.display.flip()
    fpsClock.tick(fps)