from otree.api import *


doc = """
Application for the first phase of the experiment.
"""

class C(BaseConstants):
    NAME_IN_URL = 'phase2'
    PLAYERS_PER_GROUP = None
    correct_answers = {
        'ph2_q_instructions1': 'CHF19.5',
        'ph2_q_instructions2': 'CHF6.4',
        'ph2_q_instructions3': 'CHF14',
    }
    nb_total_questions = len(correct_answers)
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Kickout
    was_player_kicked_out_phase2 = models.BooleanField(initial=False)

    # Understanding questions
    ph2_q_instructions1 = models.StringField(
        label='If you invest CHF10 in a person with a score of 44 and CHF10 in a person with a score of 34, your bonus will be calculated as follows:<br><br>',
        choices=[
            'CHF19.5',
            'CHF39',
            'CHF78',
            'CHF20',
        ],
        widget=widgets.RadioSelect
    )
    is_ph2_q_instructions_correct1 = models.BooleanField(initial=False)

    ph2_q_instructions2 = models.StringField(
        label='In the following scenario, if you invest CHF18 in a person with a score of 12 and CHF2 in a person with a score of 20, you will receive a bonus of:<br><br>',
        choices=[
            'CHF18.2',
            'CHF6.4',
            'CHF30.8',
            'CHF32',
        ],
        widget=widgets.RadioSelect
    )
    is_ph2_q_instructions_correct2 = models.BooleanField(initial=False)

    ph2_q_instructions3 = models.StringField(
        label='In the following scenario, if you invest CHF20 in a person with a score of 28, you will receive a bonus of:<br><br>',
        choices=[
            'CHF24',
            'CHF28',
            'CHF20',
            'CHF14',
        ],
        widget=widgets.RadioSelect
    )
    is_ph2_q_instructions_correct3 = models.BooleanField(initial=False)

    # Values for videos
    input_video_0 = models.IntegerField(
        min=0, max=20, label ="", initial=0
    )
    input_video_1 = models.IntegerField(
        min=0, max=20, label ="", initial=0
    )
    input_video_2 = models.IntegerField(
        min=0, max=20, label ="", initial=0
    )
    input_video_3 = models.IntegerField(
        min=0, max=20, label ="", initial=0
    )
    input_video_4 = models.IntegerField(
        min=0, max=20, label ="", initial=0
    )
    input_video_5 = models.IntegerField(
        min=0, max=20, label ="", initial=0
    )

    # Folder id
    folder_id = models.IntegerField(initial=0)

    # did multiple videos time out?
    did_multiple_videos_timeout = models.BooleanField(initial=False)
    

# PAGES
class Videos(Page):
    form_model = 'player'
    form_fields = ['input_video_0', 'input_video_1', 'input_video_2', 'input_video_3', 'input_video_4', 'input_video_5']
    timeout_seconds = 1200

    @staticmethod
    def error_message(player, values):
        print('Valeur de la somme: ', values)
        if values['input_video_0'] + values['input_video_1'] + values['input_video_2'] + values['input_video_3'] + values['input_video_4'] + values['input_video_5'] != 20:
            return '⚠ The sum of the numbers must give 20. ⚠'

        # Check if 3 values are different than 0 and if at least 1 value is different than 0
        nb_diff_zero = 0
        for res in [values['input_video_0'], values['input_video_1'], values['input_video_2'], values['input_video_3'], values['input_video_4'], values['input_video_5']]:
            if res != 0:
                nb_diff_zero += 1
        if nb_diff_zero > 3:
            return '⚠ You have to choose at most 3 values different than 0. ⚠'
        if nb_diff_zero < 1:
            return '⚠ You have to choose at least 1 value different than 0. ⚠'

    @staticmethod
    def vars_for_template(player):
        return dict(
            vid0='https://hecxpvr.unil.ch/arc/{}/0.mp4'.format(player.folder_id),
            vid1='https://hecxpvr.unil.ch/arc/{}/1.mp4'.format(player.folder_id),
            vid2='https://hecxpvr.unil.ch/arc/{}/2.mp4'.format(player.folder_id),
            vid3='https://hecxpvr.unil.ch/arc/{}/3.mp4'.format(player.folder_id),
            vid4='https://hecxpvr.unil.ch/arc/{}/4.mp4'.format(player.folder_id),
            vid5='https://hecxpvr.unil.ch/arc/{}/5.mp4'.format(player.folder_id),
        )
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.did_multiple_videos_timeout = True
        
def create_video_page_class(video_number):
    number_to_letter = {
        0: 'First',
        1: 'Second',
        2: 'Third',
        3: 'Fourth',
        4: 'Fifth',
        5: 'Sixth',
    }

    class VideoPage(Page):
        form_model = 'player'
        template_name = 'phase2/single_video.html'

        @staticmethod
        def vars_for_template(player):
            video_file = 'https://hecxpvr.unil.ch/arc/{}/{}.mp4'.format(player.folder_id, video_number)
            return dict(video=video_file, video_letters=number_to_letter[video_number])

    VideoPage.__name__ = f"Video{video_number}Page"
    return VideoPage

class Instructions(Page):
    form_model = 'player'
    template_name = 'phase2/instructions_phase2.html'
    form_fields = ['ph2_q_instructions1']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Check if the answer is correct and update the corresponding is_correct field
        player.is_ph2_q_instructions_correct1 = player.ph2_q_instructions1 == C.correct_answers['ph2_q_instructions1']
        print(player.is_ph2_q_instructions_correct1)

class Incorrect1(Page):
    form_model = 'player'
    template_name = 'phase2/incorrect1.html'
    form_fields = ['ph2_q_instructions2']
   
    @staticmethod
    def is_displayed(player: Player):
        return not player.is_ph2_q_instructions_correct1

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Check if the answer is correct and update the corresponding is_correct field
        player.is_ph2_q_instructions_correct2 = player.ph2_q_instructions2 == C.correct_answers['ph2_q_instructions2']


class Incorrect2(Page):
    form_model = 'player'
    template_name = 'phase2/incorrect2.html'
    form_fields = ['ph2_q_instructions3']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Check if the answer is correct and update the corresponding is_correct field
        player.is_ph2_q_instructions_correct3 = player.ph2_q_instructions3 == C.correct_answers['ph2_q_instructions3']

        if not player.is_ph2_q_instructions_correct3:
            player.was_player_kicked_out_phase2 = True

    @staticmethod
    def is_displayed(player: Player):
        return not player.is_ph2_q_instructions_correct2 and not player.is_ph2_q_instructions_correct1

class KickedOut(Page):
    form_model = 'player'
    template_name = 'phase2/kickout.html'

    # If the player is kicked out, he is not allowed to continue the experiment
    @staticmethod
    def is_displayed(player: Player):
        return player.was_player_kicked_out_phase2

class Correct(Page):
    form_model = 'player'
    template_name = 'phase2/correct.html'

    @staticmethod
    def before_next_page(player: Player, timeout_happened: bool):
        import psycopg2

        # Change the string
        conn = psycopg2.connect("host=localhost dbname=test user=postgres password=pierro")

        # Modify the database
        cur = conn.cursor()
        cur.execute("UPDATE users SET id = id + 1")
        cur.execute("SELECT id FROM users")
        row = cur.fetchall()
        print("id =", row[0][0])
        player.folder_id = row[0][0]
        conn.commit()
        player.participant.vars['folder_id'] = player.folder_id

VideoPages = [create_video_page_class(i) for i in range(6)]
page_sequence = [Instructions, Incorrect1, Incorrect2, KickedOut, Correct, *VideoPages, Videos]
