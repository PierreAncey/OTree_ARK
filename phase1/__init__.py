from otree.api import *


doc = """
Application for the first phase of the experiment.
"""


class C(BaseConstants):
    NAME_IN_URL = 'phase1'
    PLAYERS_PER_GROUP = None
    correct_answers = {
        'ph1_q1': 'Donald Duck',
        'ph1_q2': 'The 400 meter hurdles',
        'ph1_q3': 'Sicilia',
        'ph1_q4': 'Heatwaves',
        'ph1_q5': 'Franquin',
        'ph1_q6': '15 years',
    }
    nb_total_questions = len(correct_answers)
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    def creating_session(subsession):
        for p in subsession.get_players():
            p.participant.vars['current_question_num'] = 1


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    was_player_kicked_out_phase1 = models.BooleanField(initial=False)

    ph1_q1 = models.StringField(
        label='Who is the idol of the Donaldists?<br><br>',
        choices=[
            'Gladstone Gander',
            'Scrooge McDuck',
            'Donald Duck',
            'Huey, Dewey and Louie Duck',
        ],
        widget=widgets.RadioSelect,
        blank=True
    )

    ph1_q2 = models.StringField(
        label='What was the specialty of Ugandan athlete John Akii-Bua?<br><br>',
        choices=[
            'The 200 meter hurdles',
            'The 400 meter hurdles',
            '4x400m relay',
            'Long jump',
        ],
        widget=widgets.RadioSelect,
        blank=True
    )

    ph1_q3 = models.StringField(
        label='What is the biggest Mediterranean island?<br><br>',
        choices=[
            'Corsica',
            'Sicilia',
            'Sardaigna',
            'Cyprus',
        ],
        widget=widgets.RadioSelect,
        blank=True
    )

    ph1_q4 = models.StringField(
        label='What caused ten thousand deaths in France in 2003?<br><br>',
        choices=[
            'Domestic fires',
            'Obesity',
            'Heatwaves',
            'Mosquitos',
        ],
        widget=widgets.RadioSelect,
        blank=True
    )

    ph1_q5 = models.StringField(
        label='Which drawer created Gaston Lagaffe?<br><br>',
        choices=[
            'Franquin',
            'Uderzo',
            'Uderzo and Goscinny',
            'Gottlieb',
        ],
        widget=widgets.RadioSelect,
        blank=True
    )

    ph1_q6 = models.StringField(
        label='How long does a chicken die a natural death?<br><br>',
        choices=[
            '15 years',
            '20 years',
            '14 years',
            '18 years',
        ],
        widget=widgets.RadioSelect,
        blank=True
    )

# Dynamically add fields
for i in range(1, C.nb_total_questions + 1):
    # Add the question field to check if the answer is correct
    is_question_correct = f'is_ph1_q{i}_correct'
    setattr(Player, is_question_correct, models.BooleanField(initial=False))

    # Add the field to check if the question timed out
    did_timeout_occur = f'did_timeout_occur_ph1_q{i}'
    setattr(Player, did_timeout_occur, models.BooleanField(initial=False))


# PAGES
class Instructions(Page):
    form_model = 'player'
    template_name = 'phase1/instructions_phase1.html'

class GenericQuestionPage(Page):
    form_model = 'player'
    template_name = 'phase1/questions.html'
    timeout_seconds = 15

    # @staticmethod
    # def is_displayed(player: Player):
    #     # Display the page only if there are no timeouts in the previous questions
    #     current_question_num = player.participant.vars.get('current_question_num', 1)
    #     if player.was_player_kicked_out_phase1:
    #         return False

    #     return True

    @staticmethod
    def get_form_fields(player: Player):
        # Return the name of the question field
        current_question_num = player.participant.vars.get('current_question_num', 1)
        question_name = f'ph1_q{current_question_num}'
        return [question_name]

    @staticmethod
    def before_next_page(player: Player, timeout_happened: bool):
        # Get the current question number
        current_question_num = player.participant.vars.get('current_question_num', 1)

        # # Deal with timeout
        # if timeout_happened:
        #     # Mark the question as timed out
        #     did_timeout_occur = f'did_timeout_occur_ph1_q{current_question_num}'
        #     player.was_player_kicked_out_phase1 = True
        #     setattr(player, did_timeout_occur, True)

        # Update the current question number
        player.participant.vars['current_question_num'] = current_question_num + 1

        # Get the name of the question field and the corresponding is_correct field
        question_name = f'ph1_q{current_question_num}'
        is_correct_field_name = f'is_{question_name}_correct'

        # Check if the answer is correct and update the corresponding is_correct field
        # Use field_maybe_none() to avoid an error if the field is not defined
        question_value = player.field_maybe_none(question_name)
        if question_value is not None:
            correct_answer = C.correct_answers.get(question_name)
            if correct_answer is not None:
                setattr(player, is_correct_field_name, question_value == correct_answer)

class KickedOut(Page):
    form_model = 'player'
    template_name = 'phase1/kickout.html'

    # If the player is kicked out, he is not allowed to continue the experiment
    @staticmethod
    def is_displayed(player: Player):
        return player.was_player_kicked_out_phase1
    

# Automaticaly generate page classes for each question
questions_pages = [type(f'Question{num}', (GenericQuestionPage,), {}) for num in range(1, C.nb_total_questions + 1)]
page_sequence = [Instructions, *questions_pages, KickedOut]
