from otree.api import *
import random

class C(BaseConstants):
    NAME_IN_URL = 'block2_market'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 3
    VALUE_OF_OBJECT = cu(7)
    PRICE_A = cu(4)
    PRICE_B = cu(4.5)

class Subsession(BaseSubsession):
    treatment = models.StringField()

    def creating_session(self):
        if self.round_number == 1:
            self.session.vars['block2_payoff_round'] = random.randint(1, C.NUM_ROUNDS)

            for i, p in enumerate(self.session.get_participants()):
                # assign treatment orders once on round 1
                if i % 2 == 0:
                    p.vars['treatment_order'] = ['T0', 'T1', 'T2']
                else:
                    p.vars['treatment_order'] = ['T0', 'T2', 'T1']

            employer_data = []
            for pp in self.session.get_participants():
                block1_player = pp.get_players()[0]
                if block1_player.role() == 'employer':
                    final_wage = block1_player.group.field_maybe_none('final_wage')
                    if final_wage is not None:
                        employer_data.append({'participant': pp, 'final_wage': final_wage})

            sorted_employers = sorted(employer_data, key=lambda x: x['final_wage'])

            if len(sorted_employers) >= 2:
                unfair = sorted_employers[0]['participant']
                fair = sorted_employers[-1]['participant']
                unfair.vars['seller_label'] = 'A'
                fair.vars['seller_label'] = 'B'
                self.session.vars['seller_A_id'] = 'A'
                self.session.vars['seller_B_id'] = 'B'

        # ✅ Assign treatment for this round to all players, every round
        for p in self.get_players():
            treatment_order = p.participant.vars.get('treatment_order')
            if treatment_order:
                treatment = treatment_order[self.round_number - 1]
                p.participant.vars['current_treatment'] = treatment
                p.treatment = treatment
            else:
                print(f"⚠️ Missing treatment_order for participant {p.participant.code}")
                p.treatment = 'T0'  # fallback (safe default)

        # Optional: backward compatibility for templates
        self.treatment = self.get_players()[0].treatment


class Group(BaseGroup):
    num_supporters = models.IntegerField(initial=0)
    buyers_A = models.IntegerField(initial=0)
    buyers_B = models.IntegerField(initial=0)

class Player(BasePlayer):
    treatment = models.StringField()
    poll_vote = models.BooleanField(blank=True)

    buyer_choice = models.StringField(
        choices=[['A', 'Seller A ($4)'], ['B', 'Seller B ($4.5)']],
        widget=widgets.RadioSelect,
        blank=True
    )

    purchase_price = models.CurrencyField(blank=True)
    net_payoff = models.CurrencyField(blank=True)

    def set_payoffs(self):
        if self.buyer_choice == 'A':
            self.purchase_price = C.PRICE_A
        elif self.buyer_choice == 'B':
            self.purchase_price = C.PRICE_B
        else:
            self.purchase_price = cu(0)

        self.net_payoff = C.VALUE_OF_OBJECT - self.purchase_price

        # Assign payoff only for selected round
        if self.round_number == self.session.vars.get('block2_payoff_round'):
            self.payoff = self.net_payoff
        else:
            self.payoff = cu(0)
