from wavetables import Wavetable
import os

if not os.path.isdir("generated_code"):
    os.mkdir("generated_code")

worker_bee = Wavetable()

worker_bee.generate_table_code()