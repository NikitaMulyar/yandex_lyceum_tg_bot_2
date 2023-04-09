import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, Bot, ReplyKeyboardRemove
from config import BOT_TOKEN


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)
bot = Bot(BOT_TOKEN)


async def start(update, context):
    reply_keyboard = [['/1', '/out']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    context.user_data[update.message.chat.id] = markup
    await update.message.reply_text(
        "\U0001F3DB Добро пожаловать в музей. Пожалуйста, сдайте верхнюю одежду в гардероб!\n"
        "Выберите зал, в который хотели бы пройти...", reply_markup=context.user_data[update.message.chat.id])
    await update.message.reply_text('Можно пройти в зал №1 с ТАРДИС.')
    return 1


async def first_response(update, context):
    reply_keyboard = [['/2', '/out']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    context.user_data[update.message.chat.id] = markup
    await update.message.reply_text(
        "Вы зашли в зал №1.\nЗдесь вы видите... Что это?\nОна замаскирована. Она замаскирована под полицейскую будку из 1963 года. Каждый раз, когда ТАРДИС приземляется в новом месте, в ту же наносекунду она анализирует окрестности, высчитывает двенадцатимерную карту всего в радиусе тысячи миль, затем определяет, какая оболочка лучше всего будет гармонировать с внешней средой... И затем маскируется под полицейскую будку из 1963 года.",
        reply_markup=context.user_data[update.message.chat.id])
    await update.message.reply_text('Далее можно либо выйти из музея, либо пройти в зал №2 с Галлифреем.')
    return 2


async def second_response(update, context):
    reply_keyboard = [['/3']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    context.user_data[update.message.chat.id] = markup
    await update.message.reply_text(
        "Вы зашли в зал №2.\nПред вами висит огромная картина Галлифрея.\n«— Ну, на первый взгляд он действительно был совершенным. Да, он был красивым. Его когда-то называли Сияющим миром Семи систем. А на континенте Диких Стремлений, в горах Утешения и Одиночества, стояла Цитадель Повелителей Времени.»\n\n— Десятый Доктор",
        reply_markup=context.user_data[update.message.chat.id])
    await update.message.reply_text('Далее можно пройти в зал №3 со Скаро.')
    return 3


async def third_response(update, context):
    reply_keyboard = [['/1', '/4']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    context.user_data[update.message.chat.id] = markup
    await update.message.reply_text(
        "Вы зашли в зал №3.\nПред вами висит огромная модель Скаро.\nСкаро — родная планета каледов и талов. В ходе их вражды талы взорвали нейтронную бомбу, уничтожив почти всех каледов, в ответ на что учёный-калед Даврос в экспериментах по мутации создал далеков, которые уничтожили почти всех талов. В будущем, Скаро - центр Империи Далеков. Скаро — двенадцатая планета в своей солнечной системе, по размеру и массе приблизительно равна Земле.",
        reply_markup=context.user_data[update.message.chat.id])
    await update.message.reply_text('Далее можно пройти либо в зал №1 с ТАРДИС, либо в зал №4 с внутренним видом ТАРДИС.')
    return 4


async def fourth_response(update, context):
    reply_keyboard = [['/1']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    context.user_data[update.message.chat.id] = markup
    await update.message.reply_text(
        "Вы зашли в зал №4.\nТут вы попадаете во внутреннюю часть ТАРДИС...\nОдна из ключевых особенностей ТАРДИС в том, что интерьер существовал в другом измерении. Основное применение этой концепции реализовывало принцип — внутри они были больше, чем снаружи. Со смертью ТАРДИС эта функция может нарушиться, из-за чего она может или стать огромной, или сильно уменьшиться в размерах.",
        reply_markup=context.user_data[update.message.chat.id])
    await update.message.reply_text('Далее можно пройти в зал №1 с ТАРДИС.')
    return 5


async def end(update, context):
    reply_keyboard = [['/start']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    context.user_data[update.message.chat.id] = markup
    await update.message.reply_text("Всего доброго, не забудьте забрать верхнюю одежду в гардеробе!",
                                    reply_markup=markup)
    return ConversationHandler.END


async def stop(update, context):
    reply_keyboard = [['/start']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    context.user_data[update.message.chat.id] = markup
    await update.message.reply_text("Вас забрали далеки... До свидания!",
                                    reply_markup=markup)
    return ConversationHandler.END


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            1: [CommandHandler("1", first_response),
                CommandHandler('out', end)],
            2: [CommandHandler("2", second_response),
                CommandHandler('out', end)],
            3: [CommandHandler("3", third_response)],
            4: [CommandHandler("1", first_response),
                CommandHandler("4", fourth_response)],
            5: [CommandHandler("1", first_response)]
        },
        fallbacks=[CommandHandler('stop', stop)],
    )
    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
