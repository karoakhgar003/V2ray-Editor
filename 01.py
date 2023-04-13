import re
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi, send me a vless string to edit.")

def edit_vless_string(update, context):
    vless_string = update.message.text
    # Use regular expression to extract the hostname from the vless string
    pattern = r"vless://(.+?)@"
    match = re.search(pattern, vless_string)
    if match:
        hostname = match.group(1)
        # Replace the hostname with the new one
        new_hostname = context.args[0]
        edited_vless_string = vless_string.replace(hostname, new_hostname)
        context.bot.send_message(chat_id=update.effective_chat.id, text=edited_vless_string)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid vless string format.")

def update_hostname(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Enter the new hostname:")
    # Register the next message from the user as the new hostname
    context.user_data['command'] = 'update_hostname'

def update_hostname_callback(update, context):
    new_hostname = update.message.text
    # Update the hostname in the context
    context.user_data['hostname'] = new_hostname
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hostname updated.")

def main():
    # Set up the bot
    updater = Updater(token='6028445924:AAG7oHvC4e2Z8LOJP5u7xdqZAaMAJVCeKWA', use_context=True)
    dispatcher = updater.dispatcher
    
    # Set up handlers for commands and messages
    start_handler = CommandHandler('start', start)
    edit_vless_string_handler = MessageHandler(Filters.regex(r'^vless://'), edit_vless_string)
    update_hostname_handler = CommandHandler('update_hostname', update_hostname)
    update_hostname_callback_handler = MessageHandler(Filters.text & ~Filters.command, update_hostname_callback)
    
    # Add the handlers to the dispatcher
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(edit_vless_string_handler)
    dispatcher.add_handler(update_hostname_handler)
    dispatcher.add_handler(update_hostname_callback_handler)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
