# call data call.page_id,content_id

def get_reply(contents,content, page_id, content_id):
    numbers = {0:"0️⃣", 1:"1️⃣",2:"2️⃣",3:"3️⃣",4:"4️⃣",5:"5️⃣",6:"6️⃣",7:"7️⃣",8:"8️⃣",9:"9️⃣"}
    page_id_icon = ""
    for i in str(page_id):
        page_id_icon += numbers[int(i)]

    contents_ = len(contents[page_id].keys()) -1
    text_reply = f"""*Page: {page_id_icon}*                {content_id}/{contents_}
*Product Name:* [{content["title"]}]({content["url"]})
*Price:* *${content["price"]}*
"""
    return text_reply
def call_back(bot, call, target, types, contents, keyboards):
    call_data = call.data
    index_call = call_data.index(".")
    call_ = call_data[:index_call]
    call_data = call_data[index_call+1:]
    index = call_data.index(",")
    content_id = int(call_data[index+1:])
    page_id = int(call_data[:index])
    results = contents["results"]
    contents_count = len(contents[page_id].keys()) -1
    ##########
    if call_ == "LEFT":
        if 1 >= content_id:
            if page_id > 1:
                page_id -= 1
                content_id = len(contents[page_id].keys())
            else:
                content_id = 2
        content = contents[page_id][content_id - 1]
        text = get_reply(contents,content, page_id, content_id - 1)
        media = types.InputMedia(type='photo', media=content["image"], caption=text,parse_mode="Markdown")
        target = bot.edit_message_media(media, call.message.chat.id, target.message_id, reply_markup=keyboards.btn(contents, page_id,content_id -1))
    if call_ == "RIGHT":
        if contents_count <= content_id:
            if page_id < results:
                page_id += 1
                content_id = 0
            else:
                content_id = contents_count
        content = contents[page_id][content_id + 1]
        text = get_reply(contents,content, page_id, content_id+1)
        media = types.InputMedia(type='photo', media=content["image"], caption=text,parse_mode="Markdown")
        target = bot.edit_message_media(media, call.message.chat.id,target.message_id, reply_markup=keyboards.btn(contents, page_id,content_id +1))
    print(call.data)

