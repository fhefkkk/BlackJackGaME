# Blackjack
# From 1 to 7 players compete against a dealer

import cards, games


class BJ_Card(cards.Card):
    """ A Blackjack Card. """
    ACE_VALUE = 1

    @property
    def value(self):
        if self.is_face_up:
            v = BJ_Card.RANKS.index(self.rank) + 1
            if v > 10:
                v = 10
        else:
            v = None
        return v


class BJ_Deck(cards.Deck):
    """ A Blackjack Deck. """

    def populate(self):
        for suit in BJ_Card.SUITS:
            for rank in BJ_Card.RANKS:
                self.cards.append(BJ_Card(rank, suit))


class BJ_Hand(cards.Hand):
    """ A Blackjack Hand. """

    def __init__(self, name):
        super(BJ_Hand, self).__init__()
        self.name = name

    def __str__(self):
        rep = self.name + ":\t" + super(BJ_Hand, self).__str__()
        if self.total:
            rep += "(" + str(self.total) + ")"
        return rep

    @property
    def total(self):
        # 如果当前这手牌中有一张牌的value为None·则total为None。

        for card in self.cards:
            if not card.value:
                return None

        # 把牌的点数加起来，A的点数记为1

        t = 0
        for card in self.cards:
            t += card.value

        # 判断当前这手牌中有没有A

        contains_ace = False
        for card in self.cards:
            if card.value == BJ_Card.ACE_VALUE:
                contains_ace = True

        # 如果有A,且total够小、则将A记为11
        if contains_ace and t <= 11:
            # add only 10 since we've already added 1 for the Ace
            t += 10

        return t

    def is_busted(self):
        return self.total > 21


class BJ_Player(BJ_Hand):
    """ A Blackjack Player. """

    def is_hitting(self):  # 多态
        response = games.ask_yes_no("\n" + self.name + ", do you want a hit? (Y/N): ")
        return response == "y"

    def bust(self):  # 多态
        print(self.name, "busts.")
        self.lose()

    def lose(self):
        print(self.name, "loses.")

    def win(self):
        print(self.name, "wins.")

    def push(self):
        print(self.name, "pushes.")


class BJ_Dealer(BJ_Hand):
    """ A Blackjack Dealer. """

    def is_hitting(self):  # 多态
        return self.total < 17

    def bust(self):  # 多态
        print(self.name, "busts.")

    def flip_first_card(self):
        first_card = self.cards[0]
        first_card.flip()


class BJ_Game(object):
    """ A Blackjack Game. """

    def __init__(self, names):
        self.players = []
        for name in names:
            player = BJ_Player(name)
            self.players.append(player)

        self.dealer = BJ_Dealer("Dealer")

        self.deck = BJ_Deck()
        self.deck.populate()
        self.deck.shuffle()

    @property
    def still_playing(self):
        sp = []
        for player in self.players:
            if not player.is_busted():
                sp.append(player)
        return sp

    def __additional_cards(self, player):
        while not player.is_busted() and player.is_hitting():
            self.deck.deal([player])
            print(player)
            if player.is_busted():
                player.bust()  # is_busrt多态

    def play(self):
        # 先给每个人发两张牌
        self.deck.deal(self.players + [self.dealer], per_hand=2)
        self.dealer.flip_first_card()  # 隐藏庄家的第一张牌
        for player in self.players:
            print(player)
        print(self.dealer)

        # 给所有玩家加牌
        for player in self.players:
            self.__additional_cards(player)

        self.dealer.flip_first_card()  # 翻开庄家的第一张牌
        if not self.still_playing:
            # 由于所有玩家都爆掉了，因此直接亮出庄家手中的牌即可
            print(self.dealer)
        else:
            # 给庄家加牌

            print(self.dealer)
            self.__additional_cards(self.dealer)

            if self.dealer.is_busted():
                # 所有还在玩的玩家都获胜
                for player in self.still_playing:
                    player.win()
            else:
                # 每位还在玩的玩家分别跟庄家比点数
                for player in self.still_playing:
                    if player.total > self.dealer.total:
                        player.win()
                    elif player.total < self.dealer.total:
                        player.lose()
                    else:
                        player.push()

        # 请空所有人的牌
        for player in self.players:
            player.clear()
        self.dealer.clear()


def main():
    print("\t\tWelcome to Blackjack!\n")

    names = []
    number = games.ask_number("How many players? (1 - 7): ", low=1, high=8)
    for i in range(number):
        name = input("Enter player name: ")
        names.append(name)
    print()

    game = BJ_Game(names)

    again = None
    while again != "n":
        game.play()
        again = games.ask_yes_no("\nDo you want to play again?: ")


main()
input("\n\nPress the enter key to exit.")
