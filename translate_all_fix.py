import os
import settings
from translate_break_submission import translate

for report_name in os.listdir(settings.BREAKS):
    translate(report_name)