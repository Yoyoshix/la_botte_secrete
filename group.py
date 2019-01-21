def group(bot, msg_split):
    apprenant_list = []
    member_list = bot.get_all_members()
    for i in member_list:
        for j in i.roles:
            if (str(j) == "Apprenant"):
                apprenant_list.append(i)
    count = int(msg_split[1])
    return apprenant_list
