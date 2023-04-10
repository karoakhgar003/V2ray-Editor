from telegram.ext import *


print('Starting up bot...')
host_name = "ws.tond-vpn.works"

# Lets us use the /start command
def start_command(update, context):
    update.message.reply_text('Hello there! I\'m a bot. What\'s up?')
def update_command(update, context):

    global host_name
    host_name = context.args[0]
    update.message.reply_text(f"Host name set to: {host_name}")  

def handle_response(text) -> str:
    # Create your own response logic

    if 'vless://' in text:
        # Split the input string into its components
        split_str = text.split('@')
        uuid = split_str[0].split('//')[1]
        server_info = split_str[1].split('?')[0].split(':')
        host = host_name
        port = '443'
        encryption = 'none'
        security = 'tls'
        path = ''
        # Check if the input string contains query parameters
        if len(split_str[1].split('?')) > 1:
            params = split_str[1].split('?')[1]
            # Check if the query parameters contain 'type' and 'path'
            if 'type=' in params:
                type_val = params.split('type=')[1].split('&')[0]
                if 'path=' in params:
                    path_val = params.split('path=')[1].split('&')[0]
                    path = f'{path_val}'
            # Check if the query parameters contain 'encryption' and 'security'
            if 'encryption=' in params:
                encryption = params.split('encryption=')[1].split('&')[0]
            if 'security=' in params:
                security = params.split('security=')[1].split('&')[0]
        # Construct the response string
        response = f'vless://{uuid}@{host}:{port}?encryption={encryption}&security={security}&type={type_val}&path={path}'
        return response

    return 'I don\'t understand'

def handle_message(update, context):
    # Get basic info of the incoming message
    message_type = update.message.chat.type
    text = str(update.message.text).lower()
    response = ''

    # Print a log for debugging
    print(f'User ({update.message.chat.id}) says: "{text}" in: {message_type}')

    # React to group messages only if users mention the bot directly
    if message_type == 'group':
        # Replace with your bot username
        if '@bot19292bot' in text:
            new_text = text.replace('@bot19292bot', '').strip()
            response = handle_response(new_text)
    else:
        response = handle_response(text)

    # Reply normal if the message is in private
    update.message.reply_text(response)

# Log errors
def error(update, context):
    print(f'Update {update} caused error {context.error}')


# Run the program
if __name__ == '__main__':
    updater = Updater("6028445924:AAG7oHvC4e2Z8LOJP5u7xdqZAaMAJVCeKWA", use_context=True)
    dp = updater.dispatcher

    # Commands
    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('update', update_command))

    # Messages
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    # Add a handler for the input command
    # Log all errors
    dp.add_error_handler(error)

    # Run the bot
    updater.start_polling(1.0)
    updater.idle()

