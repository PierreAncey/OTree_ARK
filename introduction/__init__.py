from otree.api import *


doc = """
Introduction
"""


class C(BaseConstants):
    NAME_IN_URL = 'introduction'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    correct_answers = {
        'in_q1': '12645',
        'in_q2': '31782',
        'in_q3': '59682',
    }


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Time start study
    time_start_study = models.FloatField(initial=0)
    
    # Kicked out
    was_player_kicked_out_introduction_audio = models.BooleanField(initial=False)

    # Audio
    in_q1 = models.StringField(
        label='In the previous recording, I heard the following sequence of numbers:<br><br>',
        choices=[
            '15642',
            '12645',
            '32546',
            '65432',
        ],
        widget=widgets.RadioSelect
    )
    is_in_q1_correct = models.BooleanField(initial=False)

    in_q2 = models.StringField(
        label='In the previous recording, I heard the following sequence of numbers:<br><br>',
        choices=[
            '17983',
            '31782',
            '38712',
            '13798',
        ],
        widget=widgets.RadioSelect
    )
    is_in_q2_correct = models.BooleanField(initial=False)

    in_q3 = models.StringField(
        label='In the previous recording, I heard the following sequence of numbers:<br><br>',
        choices=[
            '38965',
            '96835',
            '52869',
            '59682',
        ],
        widget=widgets.RadioSelect
    )
    is_in_q3_correct = models.BooleanField(initial=False)

    # Captcha
    was_captcha_completed = models.BooleanField(initial=False)

    # Consent
    was_consent_given = models.BooleanField(
        label="Do you agree to participate?",
        widget=widgets.RadioSelectHorizontal,
        choices=[
            [True, "I agree to participate"],
            [False, "I refuse to participate"],
        ],
    )

    # Prolific ID
    prolific_id = models.StringField(
        label="Please enter your Prolific ID:<br><br>"
    )

# PAGES
class Consent(Page):
    template_name = 'introduction/consent.html'
    form_model = 'player'
    
    @staticmethod
    def live_method(player, data):
        player.was_consent_given = data['was_consent_given']

    @staticmethod
    def before_next_page(player: Player, timeout_happened: bool):
        import time
        player.time_start_study = time.time()
        
class ProlificID(Page):
    form_model = 'player'
    template_name = 'introduction/prolific.html'
    form_fields = ['prolific_id']

class Captcha(Page):
    form_model = 'player'
    template_name = 'introduction/captcha.html'

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.was_captcha_completed  = True

class Audio1(Page):
    form_model = 'player'
    template_name = 'introduction/audio1.html'
    form_fields = ['in_q1']
    timeout_seconds = 30

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Check if the answer is correct and update the corresponding is_correct field
        player.is_in_q1_correct = player.in_q1 == C.correct_answers['in_q1']

class Audio2(Page):
    form_model = 'player'
    template_name = 'introduction/audio2.html'
    form_fields = ['in_q2']
    timeout_seconds = 30

    @staticmethod
    def is_displayed(player: Player):
        return not player.is_in_q1_correct

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Check if the answer is correct and update the corresponding is_correct field
        player.is_in_q2_correct = player.in_q2 == C.correct_answers['in_q2']

class Audio3(Page):
    form_model = 'player'
    template_name = 'introduction/audio3.html'
    form_fields = ['in_q3']
    timeout_seconds = 30

    @staticmethod
    def is_displayed(player: Player):
        return not player.is_in_q2_correct and not player.is_in_q1_correct

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Check if the answer is correct and update the corresponding is_correct field
        player.is_in_q3_correct = player.in_q3 == C.correct_answers['in_q3']

        if not player.is_in_q3_correct:
            player.was_player_kicked_out_introduction_audio = True

class Instructions(Page):
    template_name = 'introduction/instructions.html'
    form_model = 'player'

class Kickout_Audio(Page):
    form_model = 'player'
    template_name = 'introduction/kickout_audio.html'

    # If the player is kicked out, he is not allowed to continue the experiment
    @staticmethod
    def is_displayed(player: Player):
        return player.was_player_kicked_out_introduction_audio

class Kickout_Consent(Page):
    form_model = 'player'
    template_name = 'introduction/kickout_consent.html'

    # If the player is kicked out, he is not allowed to continue the experiment
    @staticmethod
    def is_displayed(player: Player):
        return not player.was_consent_given

page_sequence = [Consent, Kickout_Consent, Captcha, ProlificID, Audio1, Audio2, Audio3, Kickout_Audio, Instructions]
