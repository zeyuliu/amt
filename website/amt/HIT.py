import datetime

from boto.mturk.connection import MTurkConnection
from boto.mturk.question import ExternalQuestion
from boto.mturk.qualification import PercentAssignmentsApprovedRequirement
from boto.mturk.qualification import Qualifications

from poll.settings import SANDBOX
from poll.settings import ACCESS_KEY_ID
from poll.settings import SECRET_ACCESS_KEY
from poll.settings import TITLE
from poll.settings import DESCRIPTION
from poll.settings import KEYWORDS
from poll.settings import EXTERNAL_URL
from poll.settings import MAX_ASSIGNMENTS
from poll.settings import HIT_LIFETIME
from poll.settings import REWARD
from poll.settings import DURATION
from poll.settings import FRAMEHEIGHT
from poll.settings import PERCENT_APPROVED_REQUIREMENT

class AMTConnection(object):
    def __init__(self):
        if SANDBOX:
            host = 'mechanicalturk.sandbox.amazonaws.com'
        else:
            host = 'mechanicalturk.amazonaws.com'
        login_params = {
            'aws_access_key_id': ACCESS_KEY_ID,
            'aws_secret_access_key': SECRET_ACCESS_KEY,
            'host': host
        }
        self.connection = MTurkConnection(**login_params)

        question = ExternalQuestion(EXTERNAL_URL, FRAMEHEIGHT)

        qualifications = Qualifications()
        qualifications.add(PercentAssignmentsApprovedRequirement("GreaterThanOrEqualTo", PERCENT_APPROVED_REQUIREMENT))
        self.hit_parameters = {
            'hit_type' : None,
            'question' : question,
            'title' : TITLE,
            'description' : DESCRIPTION,
            'keywords' : KEYWORDS,
            'max_assignments' : MAX_ASSIGNMENTS,
            'lifetime' : datetime.timedelta(hours=HIT_LIFETIME),
            'reward' : REWARD,
            'duration' : datetime.timedelta(DURATION),
            'approval_delay' : None,
            'questions' : None,
            'qualifications' : qualifications
        }

    def create_hit(self):
        return self.connection.create_hit(**self.hit_parameters)[0]
