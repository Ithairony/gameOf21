from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QPushButton, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
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

        self.game = Game21()    # Imports the gameLogic.py


        # # Invokes first round UI
        # self.new_round_setup()

        self.initUI()
        # self.new_round_setup()

    def initUI(self):
        # TODO: Dealer Section with cards
        # Dealer Section at the top
        self.dealerLabel = QLabel("Dealer Hand :")
        self.dealerCardsLayout = QHBoxLayout()  # QV : vertical layout  || QH : horizontal layout
        self.dealerCardsSlot = self.createCardsSlots(self.dealerCardsLayout, 3 )# Declares a fix layout of 6 cards

        # TODO: Player Section with cards
        # Player section at the bottom
        self.playerLabel = QLabel("Player Hand :")
        self.playerCardsLayout = QHBoxLayout()  # QV : vertical layout  || QH : horizontal layout
        self.playerCardsSlots = self.createCardsSlots(self.playerCardsLayout, 3)  # Declares a fix layout of 6 cards

        #  TODO: Buttons for hit, stand, new round
        self.hitBtn = QPushButton("Hit")  # Declares hit button
        self.hitBtn.setStyleSheet("padding: 10px; background:white; color: black;")
        self.hitBtn.clicked.connect(self.on_hit)  # Connects btn to "eventHandler"

        self.standBtn = QPushButton("Stand")  # Declares stand button
        self.standBtn.setStyleSheet("padding: 10px; background:white; color: black;")
        self.standBtn.clicked.connect(self.on_stand)  # Connects btn to "eventHandler"

        self.newRowndBtn = QPushButton("New Round")  # Declares newRound button
        self.newRowndBtn.setStyleSheet("padding: 10px; background:white; color: black;")
        self.newRowndBtn.clicked.connect(self.on_new_round)  # Connects btn to "eventHandler"

        #  TODO: Feedback
        self.feedbackLabel = QLabel("Feedback :")
        self.feedbackLayout = QHBoxLayout()

        #  TODO: Add widgets to layout
        container = QWidget()
        mainLayout = QVBoxLayout()

        # Buttons at the bottom of the screen
        buttonsLayout = QHBoxLayout()

        # Adding buttons and other sections to the layout
        mainLayout.addWidget(self.dealerLabel)
        mainLayout.addLayout(self.dealerCardsLayout)

        mainLayout.addWidget(self.playerLabel)
        mainLayout.addLayout(self.playerCardsLayout)

        buttonsLayout.addWidget(self.hitBtn)
        buttonsLayout.addWidget(self.standBtn)
        buttonsLayout.addWidget(self.newRowndBtn)
        mainLayout.addWidget(self.feedbackLabel)
        mainLayout.addLayout(buttonsLayout)

        container.setLayout(mainLayout)
        self.setCentralWidget(container)

        #  TODO: Trigger a new layout with a new round



    # BUTTON ACTIONS

    def on_hit(self):
        print("Hit")
        # Player takes a card
        card = self.game.player_hit()

        self.add_card(self.playerCardsLayout, card)

        if card is None:
            print("No card")
            return  # ignore until logic is ready

        if self.game.player_total() > 21:
            # TODO: what should happen if a player goes over 21? Remove pass when complete
            # Player is busted if goes over 21
            self.feedbackLabel.setText("Busted")
            self.end_round()    # Ends round


    def on_stand(self):
        # TODO: Player ends turn; dealer reveals their hidden card and plays. Remove pass when complete
        pass

    def on_new_round(self):
        self.game.new_round()
        self.new_round_setup()

    # HELPER METHODS

    def clear_layout(self, layout):
        # Remove all widgets from a layout
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def add_card(self, layout, card_text):
        # Pick which slot to use ( player or dealer)
        slots = self.playerCardsSlots if layout is self.playerCardsLayout else self.dealerCardsSlot

        for label in slots:
            if label.text() == "":
                label.setText(card_text)
                return

    def update_dealer_cards(self, full=False):
        # Show dealer cards; hide the first card until revealed
        self.clear_layout(self.dealerCardsLayout)

        for i, card in enumerate(self.game.dealer_hand):
            if i == 0 and not full:
                self.add_card(self.dealerCardsLayout, "??")   # face-down
            else:
                self.add_card(self.dealerCardsLayout, card)

        # TODO: update relevant labels in response to dealer actions. Remove pass when complete
        if full:
            pass
        else:
            pass

    def new_round_setup(self):
        # TODO: Prepare a fresh visual layout
        self.clear_layout(self.dealerCardsLayout)
        self.clear_layout(self.playerCardsLayout)

        # TODO: update relevant labels (reset dealer and player totals)

        # TODO: display new cards for dealers and players

        # TODO: enable buttons for Stand and Hit - Remove pass when complete
        self.standBtn.show()
        self.hitBtn.show()


    def end_round(self):
        # TODO: Disable button actions after the round ends. Remove pass when complete
        pass


    def createCardsSlots(self, layout, numberOfSlots):
        """Creates permanent empty card labels and returns them."""
        slots = []

        for i in range(numberOfSlots):
            lbl = QLabel("")
            lbl.setFixedSize(80, 120)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet("""
                   background: white;
                   border: 2px solid black;
                   border-radius: 6px;
                   font-size: 20px;
                   font-weight: bold;
               """)
            layout.addWidget(lbl)
            slots.append(lbl)

        return slots


# complete

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # macOS only fix for icons appearing
    app.setAttribute(Qt.ApplicationAttribute.AA_DontShowIconsInMenus, False)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
