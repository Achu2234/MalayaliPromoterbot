
# Copyright 2021 @ @Yeageristbotsdev

import os
import time
import logging
from config import Config
from pyrogram import Client, filters
from pyrogram.types import ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, UsernameNotOccupied, ChatAdminRequired, PeerIdInvalid

logging.basicConfig(level=logging.INFO)

Jebot = Client(
   "Malayali Promoter bot",
   api_id=Config.APP_ID,
   api_hash=Config.API_HASH,
   bot_token=Config.TG_BOT_TOKEN,
)

# get mute request
static_data_filter = filters.create(lambda _, __, query: query.data == "hukaidaala")

@Jebot.on_callback_query(static_data_filter)
def _onUnMuteRequest(client, lel):
  user_id = lel.from_user.id
  chat_id = lel.message.chat.id
  chat_u = Config.CHANNEL_USERNAME #channel for force sub
  if chat_u:
    channel = chat_u
    chat_member = client.get_chat_member(chat_id, user_id)
    if chat_member.restricted_by:
      if chat_member.restricted_by.id == (client.get_me()).id:
          try:
            client.get_chat_member(channel, user_id)
            client.unban_chat_member(chat_id, user_id)
            if lel.message.reply_to_message.from_user.id == user_id:
              lel.message.delete()
          except UserNotParticipant:
            client.answer_callback_query(lel.id, text="❗ സൂചിപ്പിച്ച 'ചാനലിൽ' ചേരുക, 'അൺമ്യൂട്ട് മി' ബട്ടൺ വീണ്ടും അമർത്തുക.", show_alert=True)
      else:
        client.answer_callback_query(lel.id, text="❗ മറ്റ് കാരണങ്ങളാൽ അഡ്മിൻമാർ നിങ്ങളെ മ്യൂട്ട് ചെയ്യുന്നു.", show_alert=True)
    else:
      if not client.get_chat_member(chat_id, (client.get_me()).id).status == 'administrator':
        client.send_message(chat_id, f"❗ **{lel.from_user.mention} സ്വയം അൺമ്യൂട്ട് ചെയ്യാൻ ശ്രമിക്കുന്നു, പക്ഷേ ഈ ചാറ്റിൽ ഞാൻ അഡ്മിൻ അല്ലാത്തതിനാൽ എനിക്ക് അവനെ അൺമ്യൂട്ട് ചെയ്യാൻ കഴിയില്ല.")
      else:
        client.answer_callback_query(lel.id, text="❗ ❗ മുന്നറിയിപ്പ്: നിങ്ങൾക്ക് സ്വതന്ത്രമായി സംസാരിക്കാൻ കഴിയുമെങ്കിൽ ബട്ടൺ ക്ലിക്കുചെയ്യരുത്.", show_alert=True)

@Jebot.on_message(filters.text & ~filters.private & ~filters.edited, group=1)
def _check_member(client, message):
  chat_id = message.chat.id
  chat_u = Config.CHANNEL_USERNAME #channel for force sub
  if chat_u:
    user_id = message.from_user.id
    if not client.get_chat_member(chat_id, user_id).status in ("administrator", "creator"):
      channel = chat_u
      try:
        client.get_chat_member(channel, user_id)
      except UserNotParticipant:
         try: #tahukai daala
              chat_u = chat_u.replace('@','')
              tauk = message.from_user.mention
              sent_message = message.reply_text(
                Config.WARN_MESSAGE,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                  [[InlineKeyboardButton("എന്നെ അൺമ്യൂട്ട് ചെയ്യുക", callback_data="hukaidaala")],
                  [InlineKeyboardButton("ചാനലിൽ ചേരുക", url=f"https://t.me/{chat_u}")]]))
              client.restrict_chat_member(chat_id, user_id, ChatPermissions(can_send_messages=False))

         except ChatAdminRequired:
            sent_message.edit("❗ **ഞാൻ ഇവിടെ അഡ്മിൻ അല്ല.**n__ഉണ്ടാക്കുക എന്റെ അഡ്മിൻ ബാൻ യൂസർ അനുമതിയോടെ__")

      except ChatAdminRequired:
         client.send_message(chat_id, text=f"❗ **ഞാൻ ഒരു അഡ്മിൻ അല്ല {chat_u}**\n__ചാനലിൽ എന്നെ അഡ്മിൻ ആക്കുക__")

@Jebot.on_message(filters.command("start") & ~filters.group & ~filters.channel)
def start(client, message):
   message.reply(Config.START_MESSAGE)


Jebot.run()
