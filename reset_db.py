from app import db
from models import Mentor, Mentee, Technology, Match


MODELS = [Mentor, Mentee, Technology, Match]
TECHS = ['Classical Data Science', 'Data Science ML', 'Data Science CV', 'Data Science NLP',
         'Backend Software Engineering', 'Frontend Software Engineering', 'Full-stack Software Engineering',
         'Big Data Engineering', 'Embedded Software Engineering', 'Algorithms Developer/Researcher',
         'Team Lead', 'VP R&D', 'CEO/Co-CEO', 'Tech Lead', 'Architect', 'Mobile Software Engineer (Android/iOS)',
         'Automation Engineer']


def drop_tables():
    with db:
        db.drop_tables(MODELS)


def create_tables():
    with db:
        db.create_tables(MODELS)
        

def init_technologies(techs=TECHS):
    Technology.insert_many([{'name': tech} for tech in techs]).execute()


if __name__ == '__main__':
    drop_tables()
    create_tables()
    init_technologies()
