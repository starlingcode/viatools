from scales import Scales
import os

if not os.path.isdir("generated_code"):
    os.mkdir("generated_code")

bot = Scales()

bot.read_scale_set()
bot.parse_scale_set()
bot.write_vcvrack_key()
bot.write_scale_header()
bot.write_scale_code()

