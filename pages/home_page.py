import tkinter as tk


class HomePage(tk.Frame):

    def __init__(self, parent, context):
        super().__init__(
            parent,
            bg="#f5f5f5"
        )

        self.context = context

        self.create_cards()

    # ==================================================
    # CARDS
    # ==================================================

    def create_cards(self):

        cards_container = tk.Frame(
            self,
            bg="#f5f5f5"
        )

        cards_container.pack(
            fill="x",
            padx=26,
            pady=(122, 0)
        )

        # Equal width columns
        cards_container.columnconfigure(0, weight=1)
        cards_container.columnconfigure(1, weight=1)
        cards_container.columnconfigure(2, weight=1)

        # ==================================================
        # POWER
        # ==================================================

        power_card = self.create_card(
            cards_container,
            title="Power",
            value="--"
        )

        power_card.grid(
            row=0,
            column=0,
            padx=(0, 10),
            sticky="nsew"
        )

        # ==================================================
        # INSTRUMENT
        # ==================================================

        instrument_card = self.create_card(
            cards_container,
            title="Instrument",
            value="Connected"
        )

        instrument_card.grid(
            row=0,
            column=1,
            padx=10,
            sticky="nsew"
        )

        # ==================================================
        # TEST STATUS
        # ==================================================

        test_card = self.create_card(
            cards_container,
            title="Test Status",
            value="Stop"
        )

        test_card.grid(
            row=0,
            column=2,
            padx=(10, 0),
            sticky="nsew"
        )

    # ==================================================
    # CARD CREATION
    # ==================================================

    def create_card(self, parent, title, value):

        card = tk.Frame(
            parent,
            bg="white",
            height=170,
            highlightbackground="#d0d0d0",
            highlightthickness=1
        )

        # Prevent height from being changed by children
        card.pack_propagate(False)

        # ==================================================
        # TITLE
        # ==================================================

        title_label = tk.Label(
            card,
            text=title,
            font=("Bookman Antiqua", 23),
            fg="#123d7a",
            bg="white"
        )

        title_label.pack(
            pady=(35, 10)
        )

        # ==================================================
        # VALUE
        # ==================================================

        value_label = tk.Label(
            card,
            text=value,
            font=("Bookman Antiqua", 38, "bold"),
            fg="black",
            bg="white"
        )

        value_label.pack()

        return card