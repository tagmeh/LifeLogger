import random


class HabitProvider:
    def negative_habit(self):
        habits = [
            "Procrastinating",
            "Binge-watching TV",
            "Eating junk food",
            "Skipping exercise",
            "Phone addiction",
            "Late to bed and rise",
            "Impulsive spending",
            "Being critical",
            "Social isolation",
            "Poor hygiene",
            "Unreliability",
            "Poor listening",
            "Avoiding difficult conversations",
            "Leaving things incomplete",
            "Blaming others",
        ]
        return random.choice(habits)

    def positive_habit(self):
        habits = [
            "Drink enough water",
            "Take a walk",
            "Eat vegetables",
            "Meditate daily",
            "Practice gratitude",
            "Get enough sleep",
            "Exercise regularly",
            "Read every day",
            "Limit social media",
            "Practice good posture",
            "Say 'thank you'",
            "Write in a journal",
            "Listen to music",
            "Be present in the moment",
            "Connect with friends",
        ]
        return random.choice(habits)
