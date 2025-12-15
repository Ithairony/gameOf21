from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QHBoxLayout, QPushButton, QWidget, QVBoxLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

import sys

# this project should use a modular approach - try to keep UI logic and game logic separate
from gameLogic import Game21

# MainWindowClass
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Window settings
        self.setWindowTitle("Game of 21")
        self.setGeometry(400, 400, 800, 800)    # set the windows dimensions
        self.setStyleSheet("background-color:green")     # sets the window background to green

        # Game logic model
        self.game = Game21()    # Imports the gameLogic.py

        self.initUI()
        # Optionally start with a round automatically:
        # self.game.new_round()
        # self.new_round_setup()

    def initUI(self):
        # Dealer Section at the top
        self.dealerLabel = QLabel("Dealer Hand")
        self.dealerLabel.setStyleSheet("color: white; font-weight: bold; font-size: 24px;")
        self.dealerLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dealerTotalLabel = QLabel("")
        self.dealerTotalLabel.setStyleSheet("color: gold; font-weight: bold; font-size: 24px;")
        self.dealerTotalLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dealerCardsLayout = QHBoxLayout()  # QV : vertical layout  || QH : horizontal layout
        self.dealerCardsSlot = self.createCardsSlots(self.dealerCardsLayout, 3)  # layout for dealer cards

        # Player section at the bottom
        self.playerLabel = QLabel("Player Hand ")
        self.playerLabel.setStyleSheet("color: white; font-weight: bold; font-size: 24px;")
        self.playerLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.playerTotalLabel = QLabel()
        self.playerTotalLabel.setStyleSheet("margin-top:1px; color: gold; font-weight: bold; font-size: 24px;")
        self.playerTotalLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.playerCardsLayout = QHBoxLayout()  # QV : vertical layout  || QH : horizontal layout
        self.playerCardsSlots = self.createCardsSlots(self.playerCardsLayout, 3)  # layout for player cards

        # Buttons for hit, stand, new round
        self.hitBtn = QPushButton("Hit")  # Declares hit button
        self.hitBtn.setStyleSheet("padding: 10px; background:white; color: black;")
        self.hitBtn.clicked.connect(self.on_hit)  # Connects btn to "eventHandler"

        self.standBtn = QPushButton("Stand")  # Declares stand button
        self.standBtn.setStyleSheet("padding: 10px; background:white; color: black;")
        self.standBtn.clicked.connect(self.on_stand)  # Connects btn to "eventHandler"

        self.newRowndBtn = QPushButton("New Round")  # Declares newRound button
        self.newRowndBtn.setStyleSheet("padding: 10px; background:white; color: black;")
        self.newRowndBtn.clicked.connect(self.on_new_round)  # Connects btn to "eventHandler"

        # Feedback & scoreboard
        self.feedbackLabel = QLabel("")
        self.feedbackLayout = QHBoxLayout()

        # Additional feature: simple statistics tracker (wins/losses/pushes)
        self.scoreboardLabel = QLabel("Player: 0 | Dealer: 0 | Pushes: 0")
        self.scoreboardLabel.setStyleSheet("color: white; font-weight: bold; font-size: 22px;")
        self.scoreboardLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Overall layout
        container = QWidget()
        mainLayout = QVBoxLayout()

        # Buttons at the bottom of the screen
        buttonsLayout = QHBoxLayout()

        # Adding widgets and sections to the layout
        mainLayout.addWidget(self.dealerLabel)
        mainLayout.addWidget(self.dealerTotalLabel)
        mainLayout.addLayout(self.dealerCardsLayout)

        mainLayout.addWidget(self.playerLabel)
        mainLayout.addWidget(self.playerTotalLabel)
        mainLayout.addLayout(self.playerCardsLayout)

        mainLayout.addWidget(self.feedbackLabel)
        mainLayout.addWidget(self.scoreboardLabel)

        buttonsLayout.addWidget(self.hitBtn)
        buttonsLayout.addWidget(self.standBtn)
        buttonsLayout.addWidget(self.newRowndBtn)

        mainLayout.addLayout(buttonsLayout)

        container.setLayout(mainLayout)
        self.setCentralWidget(container)

        # At the very start, we want Hit/Stand disabled until "New Round"
        self.hitBtn.hide()
        self.standBtn.hide()
        self.hitBtn.setEnabled(False)
        self.standBtn.setEnabled(False)

    # BUTTON ACTIONS

    def on_hit(self):
        """
        Player takes a card.
        If they bust (>21), the round ends and the dealer wins.
        """
        card = self.game.player_hit()
        print("CARD RECEIVED:", repr(card))

        if card is None:
            return  # extra safety

        # Display the new player card
        self.add_card(self.playerCardsLayout, card)

        # Update totals after the hit
        self.update_totals()

        # Check for bust
        if self.game.player_total() > 21:
            # Reveal dealer cards so player can see final state
            self.game.reveal_dealer_card()
            self.update_dealer_cards(full=True)

            message = self.game.decide_winner()
            self.setFeedback(message)

            # Update totals and scoreboard at the end of the round
            self.update_totals()
            self.update_scoreboard()
            self.end_round()

    def on_stand(self):
        """
        Player ends turn; dealer reveals their hidden card and plays.
        """
        # Reveal dealer hidden card
        self.game.reveal_dealer_card()
        self.update_dealer_cards(full=True)

        # Dealer plays according to rules (hit until 17 or more)
        self.game.play_dealer_turn()
        # Update dealer cards again (in case they drew more cards)
        self.update_dealer_cards(full=True)

        # Decide winner and show feedback
        message = self.game.decide_winner()
        self.setFeedback(message)

        # Update totals and scoreboard
        self.update_totals()
        self.update_scoreboard()

        # Disable further actions until new round
        self.end_round()

    def on_new_round(self):
        """
        Start a brand-new round from the game logic
        and reset the UI to match it.
        """
        self.hitBtn.show()
        self.standBtn.show()
        self.game.new_round()
        self.new_round_setup()

    # HELPER METHODS

    def clear_layout(self, layout):
        """
        Remove all widgets from a layout.
        NOTE: For card layouts we do not want to delete the labels
        themselves (they are permanent card slots), so this method
        should be used only for non-card layouts.
        """
        # Protect card layouts from being cleared here
        if layout in (self.playerCardsLayout, self.dealerCardsLayout):
            # Just clear the card texts instead of deleting the widgets
            if layout is self.playerCardsLayout:
                for lbl in self.playerCardsSlots:
                    lbl.setText("")
            else:
                for lbl in self.dealerCardsSlot:
                    lbl.setText("")
            return

        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def add_card(self, layout, card_text):
        """
        Place a card text into the first empty card slot for the
        given layout (player or dealer).
        """
        # Pick which set of slots to use (player or dealer)
        slots = self.playerCardsSlots if layout is self.playerCardsLayout else self.dealerCardsSlot

        for label in slots:
            if label.text() == "":
                label.setText(card_text)
                return

    def update_dealer_cards(self, full=False):
        """
        Show dealer cards; hide the first card until revealed.
        If full=False, first card is shown as "??".
        If full=True, all cards are shown.
        """
        # Clear the text from the dealer slots
        for lbl in self.dealerCardsSlot:
            lbl.setText("")

        # Fill slots with current dealer hand
        for i, card in enumerate(self.game.dealer_hand):
            if i == 0 and not full:
                self.add_card(self.dealerCardsLayout, "??")   # face-down
            else:
                self.add_card(self.dealerCardsLayout, card)

        # Keep game state flag consistent
        self.game.dealer_hidden_revealed = full

    def update_totals(self):
        """
        Update the labels that show the current totals
        for player and dealer.
        """
        # Player total is always fully visible
        if self.game.player_hand:
            self.playerTotalLabel.setText(f"Player total: {self.game.player_total()}")
        else:
            self.playerTotalLabel.setText("Player total: 0")

        # Dealer total is hidden until reveal
        if not self.game.dealer_hand:
            self.dealerTotalLabel.setText("Dealer total: 0")
        else:
            if self.game.dealer_hidden_revealed:
                self.dealerTotalLabel.setText(f"Dealer total: {self.game.dealer_total()}")
            else:
                # Before reveal, just show that the dealer total is hidden
                self.dealerTotalLabel.setText("Dealer total: ?")

    def update_scoreboard(self):
        """
        Update the scoreboard label using statistics
        from the Game21 logic.
        """
        self.scoreboardLabel.setText(
            f" Player: {self.game.player_wins} | "
            f"Dealer: {self.game.dealer_wins} | "
            f"Pushes: {self.game.pushes}"
        )

    def new_round_setup(self):
        """
        Prepare a fresh visual layout for a new round:
        - Reset feedback message
        - Clear current card slots
        - Deal and display new cards for dealer and player
        - Reset totals and enable Hit/Stand buttons
        """
        self.dealerTotalLabel.setText("")

        # Deal initial cards in the game logic
        self.game.deal_initial_cards()
        self.game.dealer_hidden_revealed = False

        # Reset feedback
        self.feedbackLabel.setText("")
        self.feedbackLabel.setStyleSheet(
            "color: white; font-size: 16px;"
        )
        self.feedbackLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Clear card slots
        for lbl in self.playerCardsSlots:
            lbl.setText("")
        for lbl in self.dealerCardsSlot:
            lbl.setText("")

        # Display dealer cards, with first card hidden
        self.update_dealer_cards(full=False)

        # Display player cards
        for card in self.game.player_hand:
            self.add_card(self.playerCardsLayout, card)

        # Enable buttons for Stand and Hit
        self.standBtn.setEnabled(True)
        self.hitBtn.setEnabled(True)

        # Update totals and scoreboard
        self.update_totals()
        self.update_scoreboard()

    def end_round(self):
        """
        Disable button actions after the round ends.
        Player must press 'New Round' to continue.
        """
        self.standBtn.setEnabled(False)
        self.hitBtn.setEnabled(False)

    def createCardsSlots(self, layout, numberOfSlots):
        """Creates permanent empty card labels and returns them."""
        slots = []

        for i in range(numberOfSlots):
            lbl = QLabel("")
            lbl.setFixedSize(80, 120)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            font = QFont()
            font.setPointSize(20)
            font.setBold(True)
            lbl.setFont(font)
            lbl.setStyleSheet("""
                   background: white;
                   border: 2px solid black;
                   border-radius: 6px;
               """)
            layout.addWidget(lbl)
            slots.append(lbl)

        return slots

    def setFeedback(self, message:str):
        self.feedbackLabel.setText(message)

        messageLower = message.lower()

        if "player wins" in messageLower:
            self.feedbackLabel.setStyleSheet("color: lightgreen; font-weight: bold; font-size: 24px;")
            self.feedbackLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        elif "dealer wins" in messageLower or "player busts" in messageLower:
            self.feedbackLabel.setStyleSheet( "color: red; font-weight: bold; font-size: 24px;")
            self.feedbackLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        elif "push" in messageLower or "tie" in messageLower:
            self.feedbackLabel.setStyleSheet( "color: gold; font-weight: bold; font-size: 24px;")
            self.feedbackLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)



# complete

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # macOS only fix for icons appearing
    app.setAttribute(Qt.ApplicationAttribute.AA_DontShowIconsInMenus, False)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
