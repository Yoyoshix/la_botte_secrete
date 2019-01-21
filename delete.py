async def delete(bot, message, msg_split):
    await bot.delete_message(message)
    return_msg = ""
    for i in msg_split[1:]:
        return_msg += i + " "
    return return_msg
