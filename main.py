import telebot
import os
import pickle
import datetime
from telegram.ext import Updater, CommandHandler, CallbackContext


DATA_FILE = 'bot_data.pkl'

bot = telebot.TeleBot('6207980085:AAEWImd2AzOt5QnWiEdKr5VaXG6aCAltguk')


@bot.message_handler(commands=['add_expense'])
def add_expense(message):
    text = message.text
    category = text.split(' ')[1]
    amount = text.split(' ')[2]

    data['expenses'].append({'category': category, 'amount': amount, 'timestamp': datetime.datetime.now()})
    save_data()

    bot.reply_to(message, f"Expense added in {category} category: {amount}")


categories = ['Food', 'Transport', 'Entertainment', 'Utilities', 'Other']


@bot.message_handler(commands=['list_categories'])
def list_categories(message):
    category_list = '\n'.join(categories)
    bot.reply_to(message, f"Available categories:\n{category_list}")


@bot.message_handler(commands=['add_income'])
def add_income(message):
    text = message.text
    category = text.split(' ')[1]
    amount = text.split(' ')[2]

    data['income'].append({'category': category, 'amount': amount, 'timestamp': datetime.datetime.now()})
    save_data()

    bot.reply_to(message, f"Income added in {category} category: {amount}")


@bot.message_handler(commands=['list_expenses'])
def list_expenses(message):
    expenses_list = '\n'.join([f"{expense['category']}: {expense['amount']}" for expense in data['expenses']])
    bot.reply_to(message, f"Expenses:\n{expenses_list}")


@bot.message_handler(commands=['delete'])
def delete_item(message):
    item_type = message.text.split(' ')[1]
    index = int(message.text.split(' ')[2])

    if item_type == 'expense':
        deleted_item = data['expenses'].pop(index)
    elif item_type == 'income':
        deleted_item = data['income'].pop(index)

    save_data()
    bot.reply_to(message, f"Deleted {item_type} at index {index}: {deleted_item}")


@bot.message_handler(commands=['stats'])
def get_stats(message):
    period = message.text.split(' ')[1]
    category = message.text.split(' ')[2]

    bot.reply_to(message, f"Statistics for {category} in {period}: Total: X, Average: Y")


def save_data():
    with open(DATA_FILE, 'wb') as f:
        pickle.dump({'expenses': expenses, 'income': income}, f)


if __name__ == "__main__":
    expenses = []
    income = []

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'rb') as f:
            data = pickle.load(f)
            expenses = data.get('expenses', [])
            income = data.get('income', [])

    bot.polling()


