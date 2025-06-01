from otree.api import *
from .models import C, Subsession, Group, Player


class Block2Intro(Page):
    def is_displayed(self):
        return self.round_number == 1


class PollSupport(Page):
    form_model = 'player'
    form_fields = ['poll_vote']

    def is_displayed(self):
        return self.round_number != 1 and self.player.treatment == 'T2'


    def vars_for_template(self):
        return {
            'seller_A': self.session.vars.get('seller_A_id', 'A'),
            'seller_B': self.session.vars.get('seller_B_id', 'B'),
        }

    def before_next_page(self):
        if self.player.poll_vote:
            self.group.num_supporters += 1


class WaitForT2Decisions(WaitPage):
    wait_for_all_groups = False

    def is_displayed(self):
        return (
            self.round_number > 1 and
            self.player.treatment == 'T2'
        )

    def get_players_for_group(self, waiting_players):
        # Filter only players in this round with treatment T2
        t2_players = [p for p in waiting_players
                      if p.round_number == self.round_number and
                         p.treatment == 'T2']

        # Proceed once all T2 players for this round have arrived
        expected_count = sum(
            1 for p in self.session.get_participants()
            if p.vars.get('treatment_order', [])[self.round_number - 1] == 'T2'
        )

        if len(t2_players) == expected_count:
            return t2_players
        return None


class BuyerDecision(Page):
    form_model = 'player'
    form_fields = ['buyer_choice']

    def vars_for_template(self):
        treatment = self.player.treatment
        all_players = self.subsession.get_players()

        # Count only players with same treatment in this round
        group_size = len([p for p in all_players if p.treatment == 'T2'])

        return {
            'treatment': treatment,
            'seller_A': self.session.vars.get('seller_A_id', 'A'),
            'seller_B': self.session.vars.get('seller_B_id', 'B'),
            'num_supporters': self.group.num_supporters if treatment == 'T2' else None,
            'group_size': group_size if treatment == 'T2' else None,
            'round_number': self.round_number,
            'player_id': self.player.id_in_group,
        }

    def before_next_page(self):
        if self.player.buyer_choice == 'A':
            self.group.buyers_A += 1
        elif self.player.buyer_choice == 'B':
            self.group.buyers_B += 1


class Block2Results(Page):
    def vars_for_template(self):
        if self.player.field_maybe_none('purchase_price') is None:
            self.player.set_payoffs()
        return {
            'price_paid': self.player.purchase_price,
            'net_payoff': self.player.net_payoff,
        }


class SessionResults(Page):
    def is_displayed(self):
        return self.round_number == C.NUM_ROUNDS

    def vars_for_template(self):
        block1 = self.participant.vars.get('block1_payoff', cu(0))
        block2 = self.player.payoff
        total_points = block1 + block2

        conversion_rate = self.session.config.get('real_world_currency_per_point', 1)
        total_earnings = float(total_points) * conversion_rate

        return {
            'block1_payoff': block1,
            'block2_payoff': block2,
            'total_points': total_points,
            'total_earnings': f"${total_earnings:.2f}",
            'conversion_rate': conversion_rate,
        }



page_sequence = [
    Block2Intro,
    PollSupport,
    WaitForT2Decisions,
    BuyerDecision,
    Block2Results,
    SessionResults,
]
