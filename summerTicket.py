"""
COMP.CS.100 Programming 1 / Ohjelmointi 1 - July 2023
Creator: Caijing Yang <caijing.yang@tuni.fi>
Student ID: 151525340
13.10 Project: Graphical User Interface

        Final Project - Summer Ticket - (Advanced GUI)

This program is a simulation game. Game player has two targets:
    1. Pay off the debt
    2. Earn another 3000€ to go home

The game has these systems:
    Black market: The main way to earn money. Buy low, sell high.
    Jail: Trading in black market brings player closer to jail.
          Doing favors keep player away from the jail.
    Health: Doing favors costs health. Health can't be 0.
            Hospital recovers health. Health can't be over 100.
    Bank: save and withdraw. Interests depend on game difficulty.
    Post: pay off debt or borrow more.
    Hospital: pay to recover health.

How to play:
    1. Select difficulty. Only two buttons('Game Difficulty' and
        'QUIT GAME') are active at the beginning.
    2. After selecting difficulty, the 'START / RESET' button activates.
    3. Press 'START / RESET' button, then game begins.
    4. Press 'New Day' will refresh the selling prices.
    5. Game over if distance to jail <= 0 when new day comes.
    6. Once cleared the debt in 15 days, the 'CALL' button activates.
    7. Pay 3000€ cash by 'CALL'.
    8. Congratulations!
"""

from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.simpledialog import askstring
import random


T_F = ('Helvetica', 20) # Title Font
M_F = ('Helvetica', 12) # Mini Font
N_F = ('Helvetica', 18) # Normal Font
E_F = ('Helvetica', 12, 'bold') # Emphasized Font
S_F = ('Helvetica', 15, 'italic') # Special Font


class Moneygame:

    LEVEL1, LEVEL2, LEVEL3 = 'Monkey', 'Normal', 'My Life Sucks' # Game difficulty
    DIFFICULTY = {LEVEL1: [1.15, 1.2], LEVEL2: [1.2, 1.15], \
                  LEVEL3: [1.25, 1.1]} # [debt interest, saving interest]

    def __init__(self):
        self.__mw = Tk()
        self.__mw.title("Summer Ticket")
        self.__mw.geometry('1200x650')
        self.__mw.resizable(0, 0)

        # GIF download from https://www.freepik.com;
        # Free for using but need source.
        img = PhotoImage(file='bg.gif', master=self.__mw)
        img_label = Label(self.__mw, image=img)
        img_label.image = img
        img_label.place(x=0, y=0)

        # Dict of trading items. Key: Items name. Value: amounts.
        self.__item1 = 'salmiakki'
        self.__item2 = 'snus'
        self.__item3 = 'suspicious leaf'
        self.__item4 = 'absolutely legal candy'
        self.__item5 = 'my summer car'
        self.__items = {self.__item1:0, self.__item2:0, \
                        self.__item3:0, self.__item4:0, self.__item5:0}

        # All the objects that frequently changes are created as StringVar.
        self.__hp = StringVar()
        self.__dist = StringVar()
        self.__cash = StringVar()
        self.__savings = StringVar()
        self.__debt = StringVar()
        self.__day = StringVar()

        self.__item1_price = StringVar()
        self.__item2_price = StringVar()
        self.__item3_price = StringVar()
        self.__item4_price = StringVar()
        self.__item5_price = StringVar()

        self.__item1_qty = StringVar()
        self.__item2_qty = StringVar()
        self.__item3_qty = StringVar()
        self.__item4_qty = StringVar()
        self.__item5_qty = StringVar()

        # initialize game panel display before game start
        self.__hp.set(100)
        self.__dist.set(100)
        self.__cash.set(0)
        self.__savings.set(0)
        self.__debt.set(0)
        self.__day.set(0)

        self.__item1_price.set(0)
        self.__item2_price.set(0)
        self.__item3_price.set(0)
        self.__item4_price.set(0)
        self.__item5_price.set(0)

        self.__item1_qty.set(0)
        self.__item2_qty.set(0)
        self.__item3_qty.set(0)
        self.__item4_qty.set(0)
        self.__item5_qty.set(0)

        # original value of items' price.
        self.__item1_price_orig = 10
        self.__item2_price_orig = 20
        self.__item3_price_orig = 100
        self.__item4_price_orig = 500
        self.__item5_price_orig = 2000

        # Frame for the 'BASIC STATUS'.
        # It displays HP, Distance to the jail, cash, savings and Debt.
        b_s = Frame(self.__mw, width=250, height=220)
        b_s.grid(row=0, column=0, padx=30, pady=20, ipadx=20, ipady=20)
        Label(b_s, text="BASIC STATUS", font=T_F, relief=FLAT).place(x=40, y=5)
        Label(b_s, text="Health:", fg='black', font=N_F).place(x=15, y=50)
        Label(b_s, textvariable=self.__hp, fg='darkgreen', font=N_F).place(x=200, y=50)
        Label(b_s, text="Distance to jail:", fg='black', font=N_F).place(x=15, y=80)
        Label(b_s, textvariable=self.__dist, fg='black', font=N_F).place(x=200, y=80)
        Label(b_s, text="Cash:", font=N_F).place(x=15, y=130)
        Label(b_s, textvariable=self.__cash, width=7, \
                    bg='black', fg='green', font=N_F).place(x=125, y=130)
        Label(b_s, text="€", font=N_F).place(x=250, y=130)
        Label(b_s, text="Savings:", font=N_F).place(x=15, y=170)
        Label(b_s, textvariable=self.__savings, width=7, \
                    bg='black', fg='green', font=N_F).place(x=125, y=170)
        Label(b_s, text="€", font=N_F).place(x=250, y=170)
        Label(b_s, text="Debt:", fg='red', font=N_F).place(x=15, y=210)
        Label(b_s, textvariable=self.__debt, width=7, \
                    bg='black', fg='red', font=N_F).place(x=125, y=210)
        Label(b_s, text="€", font=N_F).place(x=250, y=210)


        # Frame for the community.
        # It contains Bank, Post and Hospital buttons.
        community = Frame(self.__mw, width=250, height=250)
        community.grid(row=1, column=0,  padx=30, pady=20, ipadx=20, ipady=20)
        Label(community, text='BANK', font=N_F).place(x=5, y=5)
        self._deposit_btn = Button(community, text='Deposit', font=M_F, \
                                   state=DISABLED, command=self.deposit)
        self._withdraw_btn = Button(community, text='Withdraw', font=M_F, \
                                    state=DISABLED, command=self.withdraw)
        Label(community, text="*"*50).place(x=15, y=85)
        Label(community, text='POST', font=N_F).place(x=5, y=105)
        self._payoff_btn = Button(community, text='Pay off', font=M_F, \
                                  state=DISABLED, command=self.payoff)
        self._takeout_btn = Button(community, text='Take out', font=M_F, \
                                   state=DISABLED, command=self.takeout)
        Label(community, text="*"*50).place(x=15, y=185)
        Label(community, text='HOSPITAL', font=N_F).place(x=5, y=205)
        self._recover_btn = Button(community, text='Recover', font=M_F, \
                                   state=DISABLED, command=self.recover_hp)

        self._deposit_btn.place(x=60, y=40)
        self._withdraw_btn.place(x=180, y=40)
        self._payoff_btn.place(x=60, y=140)
        self._takeout_btn.place(x=180, y=140)
        self._recover_btn.place(x=60, y=235)


        # Frame displays player items and amounts.
        pocket = Frame(self.__mw, width=330, height=220)
        pocket.grid(row=0, column=1, padx=20, pady=20, ipadx=20, ipady=20)
        Label(pocket, text="MY POCKET", fg='black', font=T_F, relief=FLAT)\
            .place(x=180, y=5, anchor='n')
        Label(pocket, text="NO. ITEMS", font=M_F).place(x=5, y=55)
        Label(pocket, text="1. "+self.__item1, font=S_F).place(x=5, y=90)
        Label(pocket, text="2. "+self.__item2, font=S_F).place(x=5, y=120)
        Label(pocket, text="3. "+self.__item3, font=S_F).place(x=5, y=150)
        Label(pocket, text="4. "+self.__item4, font=S_F).place(x=5, y=180)
        Label(pocket, text="5. "+self.__item5, font=S_F).place(x=5, y=210)
        Label(pocket, text="QUANTITY", font=M_F).place(x=250, y=55)
        item1_qty_pocket = Label(pocket, textvariable=self.__item1_qty, \
                                 width=6, fg='green', font=S_F)
        item2_qty_pocket = Label(pocket, textvariable=self.__item2_qty, \
                                 width=6, fg='green', font=S_F)
        item3_qty_pocket = Label(pocket, textvariable=self.__item3_qty, \
                                 width=6, fg='green', font=S_F)
        item4_qty_pocket = Label(pocket, textvariable=self.__item4_qty, \
                                 width=6, fg='green', font=S_F)
        item5_qty_pocket = Label(pocket, textvariable=self.__item5_qty, \
                                 width=6, fg='green', font=S_F)

        item1_qty_pocket.place(x=250, y=90)
        item2_qty_pocket.place(x=250, y=120)
        item3_qty_pocket.place(x=250, y=150)
        item4_qty_pocket.place(x=250, y=180)
        item5_qty_pocket.place(x=250, y=210)


        # Frame displays black market items and prices.
        market = Frame(self.__mw, width=330, height=220)
        market.grid(row=0, column=2, columnspan=2, padx=20, pady=20, ipadx=20, ipady=20)
        Label(market, text="BLACK MARKET", fg='black', \
                    font=T_F, relief=FLAT).place(x=80, y=5)
        Label(market, text="NO. ITEMS", font=M_F).place(x=5, y=55)
        Label(market, text="1. "+self.__item1, font=S_F).place(x=5, y=90)
        Label(market, text="2. "+self.__item2, font=S_F).place(x=5, y=120)
        Label(market, text="3. "+self.__item3, font=S_F).place(x=5, y=150)
        Label(market, text="4. "+self.__item4, font=S_F).place(x=5, y=180)
        Label(market, text="5. "+self.__item5, font=S_F).place(x=5, y=210)
        Label(market, text="PRICE", font=M_F).place(x=265, y=55)
        item1_price = Label(market, textvariable=self.__item1_price, \
                            width=6, bg='black', fg='green', font=S_F)
        item2_price = Label(market, textvariable=self.__item2_price, \
                            width=6, bg='black', fg='green', font=S_F)
        item3_price = Label(market, textvariable=self.__item3_price, \
                            width=6, bg='black', fg='green', font=S_F)
        item4_price = Label(market, textvariable=self.__item4_price, \
                            width=6, bg='black', fg='green', font=S_F)
        item5_price = Label(market, textvariable=self.__item5_price, \
                            width=6, bg='black', fg='green', font=S_F)

        item1_price.place(x=255, y=90)
        item2_price.place(x=255, y=120)
        item3_price.place(x=255, y=150)
        item4_price.place(x=255, y=180)
        item5_price.place(x=255, y=210)

        # Frame for displaying the day information.
        # It also contains 'New Day', 'Trade' and 'Call' button.
        trade = Frame(self.__mw, width=120, height=250)
        trade.grid(row=1, column=2, padx=10, pady=10, ipadx=20, ipady=20)
        Label(trade, text='DAY:', width=6, font=N_F).place(x=5, y=35)
        Label(trade, textvariable=self.__day, width=3, fg='red', font=S_F)\
            .place(x=85, y=35)
        self._newDay_btn = Button(trade, text='NEW DAY', width=9, font=M_F, \
                                  state=DISABLED, command=self.new_day)
        self._trade_btn = Button(trade, text='TRADE', width=6, font=M_F, \
                                 state=DISABLED, command=self.trade)
        self._call_btn = Button(trade, text='CALL', width=6, font=M_F, \
                                state=DISABLED, command=self.call_guy)
        self._newDay_btn.place(x=30, y=95)
        self._trade_btn.place(x=40, y=150)
        self._call_btn.place(x=40, y=200)


        # Event related frame.
        event = Frame(self.__mw, width=350, height=250)
        event.grid(row=1, column=1, padx=20, pady=20, ipadx=20, ipady=20)
        Label(event, text="One favor a day, keeps the jail away", \
                    font=S_F).place(x=5, y=20)
        Label(event, text="Help Dr. J on archaeological research.", \
                    width=35, anchor=W, font=M_F).place(x=25, y=80)
        Label(event, text="Help Dr. O to catch wild animals.", \
                    width=35, anchor=W, font=M_F).place(x=25, y=120)
        Label(event, text="Help Prof. S to make medicines.", \
                    width=35, anchor=W, font=M_F).place(x=25, y=160)
        Label(event, text="Help Mr. S to repair his garbage ship", \
                    width=35, anchor=W, font=M_F).place(x=25, y=200)

        self._go1 = Button(event, text='GO', state=DISABLED, command=self.go_DrJ)
        self._go2 = Button(event, text='GO', state=DISABLED, command=self.go_DrO)
        self._go3 = Button(event, text='GO', state=DISABLED, command=self.go_ProfS)
        self._go4 = Button(event, text='GO', state=DISABLED, command=self.go_MrS)
        self._go1.place(x=330, y=80)
        self._go2.place(x=330, y=120)
        self._go3.place(x=330, y=160)
        self._go4.place(x=330, y=200)

        # Frame of control panel.
        ctrl = Frame(self.__mw, width=180, height=150)
        ctrl.grid(row=1, column=3)
        self._start_btn = Button(ctrl, text='START / RESTART', width=15, \
                                 fg='#2c3e50', font=E_F, state=DISABLED, \
                                 command=self.new_game)
        self._level_btn = Button(ctrl, text='Game Difficulty', width=12, \
                                 fg='#2c3e50', font=E_F, command=self.game_level)
        Button(ctrl, text='QUIT GAME', width=13, font=M_F, command=self.quit)\
            .place(x=20, y=105)
        self._start_btn.place(x=10, y=15)
        self._level_btn.place(x=25, y=60)

        # Guide for the player
        messagebox.showinfo("Hello there!", "At first, click \"Game Difficulty\" "
                                            "to select game level.")


    def start(self): # start game
        self.__mw.mainloop()

    def quit(self): # quit game
        self.__mw.destroy()

    def switchButtonState(self):
        """ This function activates buttons (set buttons clickable).

        """
        self._newDay_btn.config(state=NORMAL)
        self._trade_btn.config(state=NORMAL)
        self._deposit_btn.config(state=NORMAL)
        self._withdraw_btn.config(state=NORMAL)
        self._payoff_btn.config(state=NORMAL)
        self._takeout_btn.config(state=NORMAL)
        self._recover_btn.config(state=NORMAL)
        self._go1.config(state=NORMAL)
        self._go2.config(state=NORMAL)
        self._go3.config(state=NORMAL)
        self._go4.config(state=NORMAL)


    def game_level(self):
        """ This function creates a popup window.
            A combobox is used to select game difficulty.

        """
        self.__level_panel = Toplevel()
        self.__level_panel.geometry('250x150+880+450')
        Label(self.__level_panel, text='Select the game level you want to play:')\
            .place(x=5, y=15)
        self.__level_panel.attributes('-topmost', True) # keep the window on top
        self.__option = ttk.Combobox(self.__level_panel, state='readonly')
        self.__option.place(x=25, y=50)
        self.__option['value'] = (Moneygame.LEVEL1, Moneygame.LEVEL2, Moneygame.LEVEL3)
        Button(self.__level_panel, text='SET', width=5, command=self.set_level)\
            .place(x=80, y=100)


    @classmethod
    def adjust_interest(cls, interest1, interest2):
        """ This function set the interests.
        :param interest1: float, the debt interest.
        :param interest2: float, the bank save interest.
        """
        cls.__debt_interest = interest1 # debt interest
        cls.__bank_interest = interest2 # save interest


    def set_level(self):
        """ This function gets user selection information and
            set game difficulty by calling Moneygame.adjust_interest()
            to adjust the interests in the game.

        """
        player_choice = self.__option.get() # read difficulty
        match player_choice:
            case Moneygame.LEVEL1: # Monkey
                Moneygame.adjust_interest(Moneygame.DIFFICULTY[Moneygame.LEVEL1][0], \
                                          Moneygame.DIFFICULTY[Moneygame.LEVEL1][1])
                self._start_btn.config(state=NORMAL)
                self._level_btn.config(state=DISABLED)
                self.__level_panel.destroy()

            case Moneygame.LEVEL2: # Normal
                Moneygame.adjust_interest(Moneygame.DIFFICULTY[Moneygame.LEVEL2][0], \
                                          Moneygame.DIFFICULTY[Moneygame.LEVEL2][1])
                self._start_btn.config(state=NORMAL)
                self._level_btn.config(state=DISABLED)
                self.__level_panel.destroy()

            case Moneygame.LEVEL3: # My life sucks
                Moneygame.adjust_interest(Moneygame.DIFFICULTY[Moneygame.LEVEL3][0], \
                                          Moneygame.DIFFICULTY[Moneygame.LEVEL3][1])
                self._start_btn.config(state=NORMAL)
                self._level_btn.config(state=DISABLED)
                self.__level_panel.destroy()

        messagebox.showinfo('INFORMATION', 'Thanks! You can start game now.')


    def set_market_price(self):
        """ This function set the market price.
            Market price is randomly set from 20% to 220% of original price.

        """
        self.__item1_price_cur = int(self.__item1_price_orig * (2 * (0.2+random.random())))
        self.__item2_price_cur = int(self.__item2_price_orig * (2 * (0.2+random.random())))
        self.__item3_price_cur = int(self.__item3_price_orig * (2 * (0.2+random.random())))
        self.__item4_price_cur = int(self.__item4_price_orig * (2 * (0.2+random.random())))
        self.__item5_price_cur = int(self.__item5_price_orig * (2 * (0.2+random.random())))

        self.__item1_price.set(self.__item1_price_cur)
        self.__item2_price.set(self.__item2_price_cur)
        self.__item3_price.set(self.__item3_price_cur)
        self.__item4_price.set(self.__item4_price_cur)
        self.__item5_price.set(self.__item5_price_cur)


    def new_game(self):
        """ This function does:
            1. Popup message boxes to provide the background information
            2. Set the initial values of the game.
            3. Activate buttons.

        """
        messagebox.showinfo('Surprise!',
                            'You are visiting Tatooinekylä.\n'
                            'Someone stole everything from you.\n'
                            'A very generous guy lent you 1000€.\n'
                            'He said you can pay him back in 15 days.\n'
                            'He also said he has some bounty hunter friends.\n'
                            'And your Air Ticket home must count on him.\n'
                            )
        messagebox.showinfo('Nooooo!',
                            'Now, TRADE in the black market is your only hope.\n'
                            'Prices in the market change everyday. Be wise.\n'
                            'It brings you closer to jail, so you need do FAVORS.\n'
                            'You can transfer money with big guy by POST.\n'
                            'HOSPITAL recovers your health.\n'
                            'BANK gives you a little interests. Better than nothing.\n')
        messagebox.showinfo('Reminder', 'Take action now. '
                                        'Remember: market price changes every day.')

        self.__day.set(1) # initialize day
        self.__debt.set(-1000) # set debt
        self.__cash.set(1000) # set cash
        self.__hp.set(100) # set health
        self.__dist.set(80) # get involved with bad guy, distance to jail -20
        self.set_market_price() # set black market price
        self.switchButtonState() # Activate buttons
        # initialize the dict of items qty
        self.__items = {self.__item1:0, self.__item2:0, \
                        self.__item3:0, self.__item4:0, self.__item5:0}
        self.__item1_qty.set(0)
        self.__item2_qty.set(0)
        self.__item3_qty.set(0)
        self.__item4_qty.set(0)
        self.__item5_qty.set(0)


    def judgement(self):
        """ This function does:
            1. decide if player goes to jail. If so, give bad ending
            2. At day 15, decide cash and debt status. if
                2.1 cannot pay debt, give a bad ending
                2.2 can pay debt but did not, give another bad ending

        """
        count = 0
        if int(self.__dist.get()) <= 0: # if player goes to jail
            messagebox.showwarning('WARNING', 'Food in jail is terrible. '
                                              'Be smarter on your choice next time.')
            messagebox.showwarning('WARNING', 'GAME OVER!')
            self.__mw.destroy()

        if int(self.__day.get()) >= 15: # At day 15
            # if player cannot pay debt, give a bad ending
            if abs(int(self.__debt.get())) > 0 \
                    and int(self.__cash.get()) < abs(int(self.__debt.get())):
                messagebox.showwarning('WARNING', 'Bounty hunters are coming for you...RUN!')
                messagebox.showwarning('WARNING', 'GAME OVER!')
                self.__mw.destroy()

            # if player can but did not pay the debt, give another bad ending
            if abs(int(self.__debt.get())) > 0 \
                    and int(self.__cash.get()) > abs(int(self.__debt.get())):
                if count == 0:
                    messagebox.showwarning('WARNING', 'You love your money more than yourself???')
                    count += 1
                elif count == 1:
                    messagebox.showwarning('WARNING', 'You really love your '
                                                      'money more than yourself???')
                    count += 1
                else:
                    messagebox.showwarning('WARNING', 'Human creatures of diversity...')
                    messagebox.showwarning('WARNING', 'GAME OVER!')
                    self.__mw.destory()


    def new_day(self):
        """ This function does:
            1. call set_market_price() to set the market price.
            2. change day, debt and saving values
            3. call switchButtonState() to activate
            4. call judgement() to judge game progress

        """
        self.set_market_price()
        self.__day.set(int(self.__day.get()) + 1)
        self.__debt.set(int(int(self.__debt.get()) * self.__debt_interest))
        self.__savings.set(int(int(self.__savings.get()) * self.__bank_interest))
        self.switchButtonState()
        self.judgement()



    def recover_hp(self):
        """ This function costs money and sets the player's HP to 100.

        """
        if int(self.__hp.get()) < 100: # if need recover
            if int(self.__cash.get()) >= 100: # if enough cash
                self.__cash.set(int(self.__cash.get()) - 100) # Pay 100€
                self.__hp.set(100) # full recover HP
            else:
                messagebox.showwarning('ERROR', 'You don\'t have enough money. '
                                                'We are not charities.')
        else:
            messagebox.showinfo('INFORMATION', 'No need. You are healthy.')

    @staticmethod
    def check_input(amount):
        try:
            amount = int(amount)
            # differentiate to provide different messages
            if amount > 0:
                return 'validInput'
            else:
                return 'negInput' # Negative number
        except:
            return False # Invalid input

    def deposit(self):
        """ This function change cash to savings.

        """
        amount = askstring('Count on bank', 'How much do you want to save in the bank?')
        if Moneygame.check_input(amount) == 'validInput':
            amount = int(amount)
            if amount <= int(self.__cash.get()): # if enough cash, cash->savings
                self.__cash.set(int(self.__cash.get()) - amount)
                self.__savings.set(int(self.__savings.get()) + amount)

            else:
                messagebox.showwarning('ERROR', 'Dear customer, you don\'t have enough money.\n'
                                                'Welcome back at any time.')

        elif Moneygame.check_input(amount) == 'negInput':
            messagebox.showwarning('ERROR', 'Dear customer, please enter a positive number.\n'
                                            'Welcome back at any time.')

        elif Moneygame.check_input(amount) == False:
            messagebox.showwarning('ERROR', 'Dear customer, please enter a valid amount.\n'
                                            'Welcome back at any time.')


    def withdraw(self):
        """ This function change savings to cash.

        """
        amount = askstring('Count on bank', 'How much do you want to withdraw from the bank?')
        if Moneygame.check_input(amount) == 'validInput':
            amount = int(amount)
            if amount <= int(self.__savings.get()): # if enough savings, savings->cash
                self.__savings.set(int(self.__savings.get()) - amount)
                self.__cash.set(int(self.__cash.get()) + amount)
            else:
                messagebox.showwarning('ERROR', 'Dear customer, '
                                                'you don\'t have enough savings.\n'
                                                'Welcome back at any time.')
        elif Moneygame.check_input(amount) == 'negInput':
            messagebox.showwarning('ERROR', 'Dear customer, '
                                            'please enter a positive number.\n'
                                            'Welcome back at any time.')
        elif Moneygame.check_input(amount) == False:
            messagebox.showwarning('ERROR', 'Dear customer, please enter a valid amount.\n'
                                            'Welcome back at any time.')

    def payoff(self):
        """ This function does:
            1. minus both cash and debt.
            2. Give feedback for player's entry
            3. Activate the 'CALL' button if all debt are paid.

        """
        amount = askstring('Money issue', 'How much do you want to repay?')
        if Moneygame.check_input(amount) == 'validInput':
            amount = int(amount)
            if amount <= int(self.__cash.get()): # payback value <= cash
                # if payback value < debt, only pay
                if amount < abs(int(self.__debt.get())):
                    self.__cash.set(int(self.__cash.get()) - amount)
                    self.__debt.set(int(self.__debt.get()) + amount)

                # if payback value == debt, go stage 2.
                elif amount == abs(int(self.__debt.get())):
                    messagebox.showinfo('TICKET', 'I am the one who have your ticket.\n'
                                                  'Call me when you have 3000€. '
                                                  'I will send you home.')
                    messagebox.showwarning('ATTENTION', 'I\'m busy. '
                                                        'NEVER call me without enough money.')
                    self.__cash.set(int(self.__cash.get()) - amount)
                    self.__debt.set(0)
                    self._call_btn.config(state=NORMAL)

                else: # if payback value > debt, pop up a message box and go stage 2.
                    messagebox.showinfo('RICH GUY:)', 'I won\'t give extra money back. '
                                                      'I\'ll buy myself some salmiakki.')
                    messagebox.showinfo('RICH GUY:)', 'I am the one who have your ticket.\n'
                                                      'Call me when you have 3000€. '
                                                      'I will send you home.')
                    self.__cash.set(int(self.__cash.get()) - amount)
                    self.__debt.set(0)
                    self._call_btn.config(state=NORMAL)

            else: # if payback value > cash
                messagebox.showwarning('ERROR', 'You are wasting Big Brother\'s time!')
                messagebox.showwarning('WARNING', 'Eat BIG BROTHER\'s punch!' )
                # Reduce HP if it > 5, otherwise increase Debt.
                if int(self.__hp.get()) > 5:
                    self.__hp.set(int(self.__hp.get())-5)
                    messagebox.showinfo('INFORMATION', 'HP-5')
                else:
                    self.__debt.set(int(self.__debt.get())-100)
                    messagebox.showinfo('INFORMATION', 'Debt+100')

        elif Moneygame.check_input(amount) == 'negInput':
            messagebox.showwarning('ERROR', 'You are wasting Big Brother\'s time!')
            messagebox.showwarning('WARNING', 'Eat BIG BROTHER\'s punch!')
            if int(self.__hp.get()) > 5:
                self.__hp.set(int(self.__hp.get()) - 5)
                messagebox.showinfo('INFORMATION', 'HP-5')
            else:
                self.__debt.set(int(self.__debt.get()) - 100)
                messagebox.showinfo('INFORMATION', 'Debt+100')

        elif Moneygame.check_input(amount) == False:
            messagebox.showwarning('ERROR', 'You don\'t mess with Big Brother!')
            messagebox.showwarning('WARNING', 'Eat BIG BROTHER\'s punch!')
            if int(self.__hp.get()) > 5:
                self.__hp.set(int(self.__hp.get())-5)
                messagebox.showinfo('INFORMATION', 'HP-5')
            else:
                self.__debt.set(int(self.__debt.get())-100)
                messagebox.showinfo('INFORMATION', 'Debt+100')


    def takeout(self):
        """ This function plus both cash and debt. It means you borrow more money.

        """
        amount = askstring('Money issue', 'Good, Good. The more you borrow, '
                                          'the more you pay back.\n'
                                          'How much do you want?')
        if Moneygame.check_input(amount) == 'validInput':
            amount = int(amount)
            if amount > 1000: # cannot borrow too much
                messagebox.showwarning('WARNING', 'No way! You don\'t have three kidneys!')
            else:
                self.__debt.set(int(self.__debt.get()) - amount)
                self.__cash.set(int(self.__cash.get()) + amount)

        elif Moneygame.check_input(amount) == 'negInput':
            messagebox.showwarning('ERROR', 'You are wasting Big Brother\'s time!')
            messagebox.showwarning('WARNING', 'Eat BIG BROTHER\'s punch!')
            if int(self.__hp.get()) > 5:
                self.__hp.set(int(self.__hp.get()) - 5)
                messagebox.showinfo('INFORMATION', 'HP-5')
            else:
                self.__debt.set(int(self.__debt.get()) - 100)
                messagebox.showinfo('INFORMATION', 'Debt+100')

        elif Moneygame.check_input(amount) == False:
            messagebox.showwarning('ERROR', 'You don\'t mess with Big Brother!')
            messagebox.showwarning('WARNING', 'Eat BIG BROTHER\'s punch!')
            if int(self.__hp.get()) > 5:
                self.__hp.set(int(self.__hp.get())-5)
                messagebox.showinfo('INFORMATION', 'HP-5')
            else:
                self.__debt.set(int(self.__debt.get())-100)
                messagebox.showinfo('INFORMATION', 'Debt+100')


    def dist_decrease(self):
        """ This function set player nearer to jail.

        """
        distanceVary = 20 # distance nearer to jail
        self.__dist.set(int(self.__dist.get()) - distanceVary)


    # Following four functions costs HP but keep player away from jail.
    # They also deactivate the button after clicking.
    def go_DrJ(self):
        if int(self.__hp.get()) > 30:
            self.__hp.set(int(self.__hp.get()) - 30)
            self.__dist.set(int(self.__dist.get()) + 35)
            self._go1.config(state=DISABLED)
            messagebox.showinfo('INFORMATION', 'HP-30\n'
                                               'Distance+35.')
        else:
            messagebox.showwarning('ERROR', 'You are too tired to go there.')


    def go_DrO(self):
        if int(self.__hp.get()) > 50:
            self.__hp.set(int(self.__hp.get()) - 50)
            self.__dist.set(int(self.__dist.get()) + 25)
            self._go2.config(state=DISABLED)
            messagebox.showinfo('INFORMATION', 'HP-50\n'
                                               'Distance+25.')
        else:
            messagebox.showwarning('ERROR', 'You are too tired to go there.')


    def go_MrS(self):
        if int(self.__hp.get()) > 40:
            self.__hp.set(int(self.__hp.get()) - 40)
            self.__dist.set(int(self.__dist.get()) +20)
            self._go4.config(state=DISABLED)
            messagebox.showinfo('INFORMATION', 'HP-40\n'
                                               'Distance+20.')
        else:
            messagebox.showwarning('ERROR', 'You are too tired to go there.')


    def go_ProfS(self):
        if int(self.__hp.get()) > 20:
            self.__hp.set(int(self.__hp.get()) - 20)
            self.__dist.set(int(self.__dist.get()) +15)
            self._go3.config(state=DISABLED)
            messagebox.showinfo('INFORMATION', 'HP-20\n'
                                               'Distance+15.')
        else:
            messagebox.showwarning('ERROR', 'You are too tired to go there.')


    def trade(self):
        """ This function create a popup window for trading in black market.

        """
        trade_panel = Toplevel()
        trade_panel.geometry('250x220+880+450')
        Label(trade_panel, text='Select the item you want to trade:').place(x=5, y=15)
        trade_panel.attributes('-topmost', True)
        self.__trade_option1 = ttk.Combobox(trade_panel, state='readonly') #Player can't input
        self.__trade_option1.place(x=25, y=50)
        self.__trade_option1['value'] = (self.__item1, self.__item2, \
                                         self.__item3, self.__item4, self.__item5)


        Label(trade_panel, text='Select the amount you want to trade:')\
            .place(x=5, y=105)
        self.__trade_option2 = Entry(trade_panel, width=15, font=M_F)
        self.__trade_option2.place(x=25, y=140)


        Button(trade_panel, text='BUY', width=5, command=self.buy_option)\
            .place(x=55, y=185)
        Button(trade_panel, text='SELL', width=5, command=self.sell_option)\
            .place(x=125, y=185)


    def buy_option(self):
        """ This function Does:
            1. get which item and how much to buy
            2. give error message if input incorrectly
            3. calculate and set cash
            4. set item amounts
            5. set player nearer to jail

        """
        select1 = self.__trade_option1.get() # item to buy
        select2 = self.__trade_option2.get() # amount to buy

        if Moneygame.check_input(select2) == 'validInput': #Valid input
            select2 = int(select2)
            match select1: # match which item to buy
                case self.__item1:
                    # if not enough money
                    if int(self.__cash.get()) < self.__item1_price_cur * select2:
                        messagebox.showwarning(title='WARNING', \
                                               message='You don\'t have enough money.')
                    else:
                        self.__items[select1] += int(select2) # add amount
                        self.__item1_qty.set(self.__items[select1]) # update display amount
                        self.__cash.set(int(int(self.__cash.get()) - self.__item1_price_cur * select2)) # set cash
                        self.dist_decrease() # set distance to jail


                case self.__item2:
                    if int(self.__cash.get()) < self.__item2_price_cur * select2:
                        messagebox.showwarning(title='WARNING', \
                                               message='You don\'t have enough money.')
                    else:
                        self.__items[select1] += int(select2)
                        self.__item2_qty.set(self.__items[select1])
                        self.__cash.set(int(int(self.__cash.get()) - self.__item2_price_cur * select2))
                        self.dist_decrease()

                case self.__item3:
                    if int(self.__cash.get()) < self.__item3_price_cur * select2:
                        messagebox.showwarning(title='WARNING', \
                                               message='You don\'t have enough money.')
                    else:
                        self.__items[select1] += int(select2)
                        self.__item3_qty.set(self.__items[select1])
                        self.__cash.set(int(int(self.__cash.get()) - self.__item3_price_cur * select2))
                        self.dist_decrease()

                case self.__item4:
                    if int(self.__cash.get()) < self.__item4_price_cur * select2:
                        messagebox.showwarning(title='WARNING', \
                                               message='You don\'t have enough money.')
                    else:
                        self.__items[select1] += int(select2)
                        self.__item4_qty.set(self.__items[select1])
                        self.__cash.set(int(int(self.__cash.get()) - self.__item4_price_cur * select2))
                        self.dist_decrease()

                case self.__item5:
                    if int(self.__cash.get()) < self.__item5_price_cur * select2:
                        messagebox.showwarning(title='WARNING', \
                                               message='You don\'t have enough money.')
                    else:
                        self.__items[select1] += int(select2)
                        self.__item5_qty.set(self.__items[select1])
                        self.__cash.set(int(int(self.__cash.get()) - self.__item5_price_cur * select2))
                        self.dist_decrease()

        elif Moneygame.check_input(select2) == 'negInput': # Negative input
            messagebox.showwarning(title='WARNING', \
                                   message='Don\'t waste each other\'s time,\n'
                                            'the seller shouted to you.')
        elif Moneygame.check_input(select2) == False: # Invalid input
            messagebox.showwarning('ERROR', 'Please enter a number.')

    def sell_option(self):
        """ This function helps to:
            1. get which item and how much to sell
            2. give error message if input incorrectly
            3. calculate and set cash
            4. set item amounts
            5. set player nearer to jail

        """
        select1 = self.__trade_option1.get() # which item to sell
        select2 = self.__trade_option2.get() # how many items to sell

        if Moneygame.check_input(select2) == 'validInput': # valid input
            select2 = int(select2)
            if select2 > self.__items[select1]: # cannot sell more items than held
                messagebox.showwarning(title='WARNING', message='You don\'t have so many items.')

            # match which items to sell
            else:
                self.__items[select1] -= int(select2)
                match select1:
                    case self.__item1:
                        self.__item1_qty.set(self.__items[select1])  # set amount
                        # refresh display amount
                        self.__cash.set(int(int(self.__cash.get()) + self.__item1_price_cur * select2))
                        self.dist_decrease()  # set player nearer to jail

                    case self.__item2:
                        self.__item2_qty.set(self.__items[select1])
                        self.__cash.set(int(int(self.__cash.get()) + self.__item2_price_cur * select2))
                        self.dist_decrease()

                    case self.__item3:
                        self.__item3_qty.set(self.__items[select1])
                        self.__cash.set(int(int(self.__cash.get()) + self.__item3_price_cur * select2))
                        self.dist_decrease()

                    case self.__item4:
                        self.__item4_qty.set(self.__items[select1])
                        self.__cash.set(int(int(self.__cash.get()) + self.__item4_price_cur * select2))
                        self.dist_decrease()

                    case self.__item5:
                        self.__item5_qty.set(self.__items[select1])
                        self.__cash.set(int(int(self.__cash.get()) + self.__item5_price_cur * select2))
                        self.dist_decrease()


        elif Moneygame.check_input(select2) =='negInput': # Negative input
            messagebox.showwarning(title='WARNING', message='Don\'t waste each other\'s time,\n'
                                                            'the buyer shouted to you.')

        elif Moneygame.check_input(select2) == False: # Invalid input
            messagebox.showwarning('ERROR', 'Please enter a number.')


    def call_guy(self):
        """ This function set the game to the second stage.
            It destroys the main window if the second game target
            is completed (cash >= 3000).

        """
        if int(self.__cash.get()) >= 3000:
            self.__cash.set(int(self.__cash.get()) - 3000)
            messagebox.showinfo('CONGRATULATIONS', 'You are tough and smart. '
                                                   'You survived and get a ticket home!')
            messagebox.showinfo('CONGRATULATIONS', 'All missions accomplished.')
            messagebox.showinfo('ACKNOWLEDGEMENT', 'Thank you for your time!\n'
                                                   'Hope you get some fun with this little game.')
            self.__mw.destroy()

        elif (int(self.__cash.get()) < 3000) and (int(self.__savings.get()) >= 3000):
            messagebox.showwarning('WARNING', 'I don\'t care about your savings.\n'
                                              'I only accept cash.')
            messagebox.showwarning('WARNING', 'Eat BIG BROTHER\'s punch!')
            if int(self.__hp.get()) > 5:
                self.__hp.set(int(self.__hp.get())-5)
                messagebox.showinfo('INFORMATION', 'HP-5')
            else:
                self.__debt.set(int(self.__debt.get())-100)
                messagebox.showinfo('INFORMATION', 'Debt+100')

        elif int(self.__cash.get()) >= 500:
            self.__cash.set(int(self.__cash.get()) - 500)
            messagebox.showwarning('WARNING', 'Big guy is angry because you waste his time. '
                                              'He need 500€ to calm down.')
            messagebox.showinfo('INFORMATION', 'CASH-500')

        else:
            self.__debt.set(-500)
            messagebox.showwarning('WARNING', 'Big guy is angry because you waste his time. '
                                              'He need 500€ to calm down.')
            messagebox.showinfo('INFORMATION', 'DEBT+500')



def main():

    mg = Moneygame()
    mg.start()

if __name__ == "__main__":
    main()
