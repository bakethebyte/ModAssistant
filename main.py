
import praw
import os
import time

# Авторизація через секрети GitHub
reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    password=os.getenv('REDDIT_PASSWORD'),
    user_agent="RedditModAssistant v1.1 by bakethebyte",
    username=os.getenv('REDDIT_USERNAME'),
)

# Налаштування фільтрів (можна змінювати під потреби сабреддіта)
MIN_ACCOUNT_AGE_DAYS = 7  # "Червоний прапорець", якщо акаунту менше тижня
MIN_KARMA = 10            # Підозріло, якщо карма дуже низька
BANNED_WORDS = ["spam", "scam", "click here", "free money"] 

def check_user_reliability(author):
    """Функція OSINT-аналізу користувача"""
    flags = []
    
    # 1. Перевірка віку акаунта
    created_date = author.created_utc
    age_days = (time.time() - created_date) / (24 * 3600)
    if age_days < MIN_ACCOUNT_AGE_DAYS:
        flags.append(f"НОВИЙ АКАУНТ ({int(age_days)} днів)")
        
    # 2. Перевірка карми
    total_karma = author.link_karma + author.comment_karma
    if total_karma < MIN_KARMA:
        flags.append(f"НИЗЬКА КАРМА ({total_karma})")
        
    return flags

def monitor_comments():
    print("Бот RedditModAssistant v1.1 запущено...")
    print("Режим: Розумна модерація (OSINT-аналіз активовано)")
    
    # Рекомендую почати з тестового сабреддіта
    subreddit = reddit.subreddit("test") 
    
    for comment in subreddit.stream.comments(skip_existing=True):
        # Ігноруємо самого бота
        if comment.author == reddit.user.me():
            continue
            
        content = comment.body.lower()
        user_flags = check_user_reliability(comment.author)
        has_bad_words = any(word in content for word in BANNED_WORDS)
        
        # ЛОГІКА ДІЇ
        if has_bad_words or user_flags:
            # Формуємо звіт для логів
            report = f"\n[!] Знайдено підозрілу активність: u/{comment.author}"
            if user_flags:
                report += f" | Прапорці: {', '.join(user_flags)}"
            if has_bad_words:
                report += " | Причина: Стоп-слова"
            
            print(report)

            # Якщо є і стоп-слова, і червоні прапорці — це критично
            if has_bad_words and user_flags:
                comment.reply(
                    f"⚠️ [RedditModAssistant Alert]\n\n"
                    f"Привіт, u/{comment.author}! Твій акаунт або коментар видаються підозрілими нашому фільтру.\n"
                    f"Ми цінуємо безпеку спільноти, тому твій пост буде перевірено модератором вручну."
                )
                # Опціонально: comment.mod.remove() # Видаляє коментар (потрібні права модератора)

if __name__ == "__main__":
    monitor_comments()
