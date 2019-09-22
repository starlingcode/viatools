from scales import Scales

bot = Scales()

bot.read_scale_set()
bot.parse_scale_set()
bot.write_vcvrack_key()
bot.write_scale_header()
bot.write_scale_code()

