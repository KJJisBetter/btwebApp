import os
from faker import Faker
from app import create_app, db
from app.models import User, Transaction
from datetime import datetime, timedelta
import random

app = create_app()
fake = Faker()

def add_fake_data(user_id, num_transactions=1000):
    with app.app_context():
        for _ in range(num_transactions):
            transaction = Transaction(
                amount=round(random.uniform(5.00, 10000.00), 2),
                category=fake.word(),
                date=fake.date_between(start_date='-1y', end_date='today'),
                description=fake.sentence(),
                user_id=user_id
            )
            db.session.add(transaction)
        db.session.commit()
        print(f'Added {num_transactions} fake transactions for user_id {user_id}')

if __name__ == '__main__':
    with app.app_context():
        # Create a fake user for testing
        if not User.query.filter_by(email='testuser@example.com').first():
            user = User(username='testuser', email='testuser@example.com')
            user.set_password('password')
            db.session.add(user)
            db.session.commit()
            print('Added fake user with email testuser@example.com')
        
        # Get the user_id of the created user
        user = User.query.filter_by(email='testuser@example.com').first()
        add_fake_data(user.id, num_transactions=100)
