from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models

from octofit_tracker import settings

from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Connect to MongoDB
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        # Drop collections if they exist
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Create unique index on email for users
        db.users.create_index('email', unique=True)

        # Sample data
        users = [
            {"name": "Iron Man", "email": "ironman@marvel.com", "team": "marvel"},
            {"name": "Captain America", "email": "cap@marvel.com", "team": "marvel"},
            {"name": "Hulk", "email": "hulk@marvel.com", "team": "marvel"},
            {"name": "Batman", "email": "batman@dc.com", "team": "dc"},
            {"name": "Superman", "email": "superman@dc.com", "team": "dc"},
            {"name": "Wonder Woman", "email": "wonderwoman@dc.com", "team": "dc"},
        ]
        teams = [
            {"name": "marvel", "members": ["ironman@marvel.com", "cap@marvel.com", "hulk@marvel.com"]},
            {"name": "dc", "members": ["batman@dc.com", "superman@dc.com", "wonderwoman@dc.com"]},
        ]
        activities = [
            {"user_email": "ironman@marvel.com", "activity": "run", "distance": 5},
            {"user_email": "cap@marvel.com", "activity": "cycle", "distance": 20},
            {"user_email": "hulk@marvel.com", "activity": "swim", "distance": 2},
            {"user_email": "batman@dc.com", "activity": "run", "distance": 10},
            {"user_email": "superman@dc.com", "activity": "fly", "distance": 100},
            {"user_email": "wonderwoman@dc.com", "activity": "jump", "distance": 15},
        ]
        leaderboard = [
            {"team": "marvel", "points": 100},
            {"team": "dc", "points": 120},
        ]
        workouts = [
            {"name": "Morning Cardio", "suggested_for": "marvel"},
            {"name": "Strength Training", "suggested_for": "dc"},
        ]

        db.users.insert_many(users)
        db.teams.insert_many(teams)
        db.activities.insert_many(activities)
        db.leaderboard.insert_many(leaderboard)
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
