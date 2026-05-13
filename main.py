import praw
import os

# Авторизація через секрети GitHub
reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    password=os.getenv('REDDIT_PASSWORD'),
    user_agent="RedditModAssistant by bakethebyte",
    username=os.getenv('REDDIT_USERNAME'),
)

# Список слів для перевірки
BANNED_WORDS = ["spam", "badword1"] 

def monitor_comments():
    print("Бот RedditModAssistant почав стежити за коментарями...")
    # Тут ми вказуємо сабреддіт (наприклад, 'all' або твій тестовий)
    subreddit = reddit.subreddit("test") 
    
    for comment in subreddit.stream.comments(skip_existing=True):
        content = comment.body.lower()
        if any(word in content for word in BANNED_WORDS):
            # М'яка модерація: бот пише відповідь
            comment.reply("Привіт! Твій коментар містить небажані слова. Будь ласка, відредагуй його, щоб спільнота була дружньою!")
            print(f"Знайдено порушення у користувача {comment.author}")

if __name__ == "__main__":
    monitor_comments()

