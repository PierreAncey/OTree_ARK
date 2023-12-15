from otree.api import *

class C(BaseConstants):
    NAME_IN_URL = 'Matthieu_ARK'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
     pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Demographics
    gender = models.StringField(
        label='What is your gender?',
        choices=[
            'Woman',
            'Man',
            'Other'
        ],
        widget=widgets.RadioSelect
    )

    # Potential other gender
    show_other_gender = models.BooleanField(initial=False)
    other_gender = models.StringField(initial=None, label='Could you please specify your gender?')

    education = models.StringField(
        label="What is your highest degree of education?",
        choices=[
            'Some high school, no diploma',
            'High school degree or equivalent',
            'Apprenticeship',
            "Bachelor's degree (e.g. BA, BS)",
            "Master's degree (e.g. MA, MS, MEd)",
            "Doctorate (e.g. PhD)",
            'Other'
        ],
        widget=widgets.RadioSelect
    )
    english_proficiency = models.StringField(
        label="How would you rate your English language proficiency?",
        choices=['A1', 'A2', 'B1', 'B2', 'C1', 'C2'],
        widget=widgets.RadioSelect
    )
    leadership_experience = models.BooleanField(
        label="Did you have any previous experience in leadership positions?",
        choices=[[True, 'Yes'], [False, 'No']],
        widget=widgets.RadioSelect
    )
    age = models.IntegerField()

    # Leadership month of experience
    leadership_experience_month = models.IntegerField()
    show_leadership_experience_month = models.BooleanField(initial=False)

    # Temp variables for the bias survey
    temp_perceived_age = models.IntegerField()
    temp_ethnicity =  models.StringField(label="What is the ethnicity of the person in the video?", choices=['White', 'Black', 'Asian', 'Other'], widget=widgets.RadioSelect())
    temp_gender = models.StringField(label="What is the gender of the person in the video?", choices=['Man', 'Woman', 'Other'], widget=widgets.RadioSelect())
    temp_likability = models.IntegerField()
    temp_expressiveness = models.IntegerField()

    # General guesses
    goal_study = models.StringField(label="According to you, what was the goal of the study?", blank=True)
    improve_study = models.StringField(label="According to you, how can we improve the study?", blank=True)


# Add lots of fields for each video
for i in range(6):
    # Add the question field to check if the answer is correct
    perceived_age_vid = f'perceived_age_vid{i}'
    setattr(Player, perceived_age_vid, models.IntegerField())

    ethnicity_vid = f'ethnicity_vid{i}'
    setattr(Player, ethnicity_vid, models.StringField(label="What is the ethnicity of the person in the video?", choices=['White', 'Black', 'Asian', 'Other'], widget=widgets.RadioSelect()))

    gender_vid = f'gender_vid{i}'
    setattr(Player, gender_vid, models.StringField(label="What is the gender of the person in the video?", choices=['Man', 'Woman', 'Other'], widget=widgets.RadioSelect()))

    likability_vid = f'likability_vid{i}'
    setattr(Player, likability_vid, models.IntegerField())

    expressiveness_vid = f'expressiveness_vid{i}'
    setattr(Player, expressiveness_vid, models.IntegerField())
    

# ======================================================================================================================
#                                                       REST
# ======================================================================================================================

# PAGES
class info(Page):
    form_model = 'player'
    form_fields = ['prolific_id', 'age', 'gender']

class thanks(Page):
    form_model = 'player'
    form_fields = ['age', 'gender']

    # Def var succeeded = 1

class questions(Page):
    form_model = 'player'
    form_fields = ['iq']

class Gender(Page):
    form_model = 'player'
    form_fields = ['gender']
    template_name = 'end/gender.html'

    @staticmethod
    def before_next_page(player: Player, timeout_happened: bool):
        # If the player selected "Other", set show_other_gender to True
        if player.gender == "Other":
            player.show_other_gender = True

class OtherGender(Page):
    form_model = 'player'
    form_fields = ['other_gender']
    template_name = 'end/other_gender.html'

    @staticmethod
    def is_displayed(player: Player):
        return player.show_other_gender

class OtherDemographics(Page):
    form_model = 'player'
    form_fields = ['age', 'education', 'english_proficiency', 'leadership_experience']
    template_name = 'end/other_demographics.html'

    @staticmethod
    def before_next_page(player: Player, timeout_happened: bool):
        # If the player selected "Other", set show_other_gender to True
        if player.leadership_experience:
            player.show_leadership_experience_month = True

class LeadershipExperienceMonth(Page):
    form_model = 'player'
    form_fields = ['leadership_experience_month']
    template_name = 'end/leadership_experience_month.html'

    @staticmethod
    def is_displayed(player: Player):
        return player.show_leadership_experience_month

def create_video_page_class(video_number):
    number_to_letter = {
        0: 'First',
        1: 'Second',
        2: 'Third',
        3: 'Fourth',
        4: 'Fifth',
        5: 'Sixth',
    }

    class BiasSurvey(Page):
        form_model = 'player'
        form_fields = ['temp_perceived_age', 'temp_ethnicity', 'temp_gender', 'temp_likability', 'temp_expressiveness']
        template_name = 'end/bias_survey.html'

        @staticmethod
        def vars_for_template(player):
            folder_id = player.participant.vars['folder_id']
            print("folder id from vars_for_template", folder_id)
            return dict(
                img='https://hecxpvr.unil.ch/arc/{}/images/{}.jpg'.format(folder_id, video_number),
                video_letters=number_to_letter[video_number],
            )

        @staticmethod
        def before_next_page(player: Player, timeout_happened: bool):
            # Write the temp fields to the corresponding fields
            setattr(player, f'perceived_age_vid{video_number}', player.temp_perceived_age)
            setattr(player, f'ethnicity_vid{video_number}', player.temp_ethnicity)
            setattr(player, f'gender_vid{video_number}', player.temp_gender)
            setattr(player, f'likability_vid{video_number}', player.temp_likability)
            setattr(player, f'expressiveness_vid{video_number}', player.temp_expressiveness)
    
    BiasSurvey.__name__ = f"BiasSurvey{video_number}"

    return BiasSurvey

class GoalStudy(Page):
    form_model = 'player'
    form_fields = ['goal_study']
    template_name = 'end/requests.html'

class ImproveStudy(Page):
    form_model = 'player'
    form_fields = ['improve_study']
    template_name = 'end/requests.html'

BiasPages = [create_video_page_class(i) for i in range(6)]
page_sequence = [Gender, OtherGender, OtherDemographics, LeadershipExperienceMonth, *BiasPages, GoalStudy, ImproveStudy, thanks] 