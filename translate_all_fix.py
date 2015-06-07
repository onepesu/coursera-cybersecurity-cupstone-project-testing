import os
import settings
from translate_break_submission import translate

for report_name in os.listdir(settings.BREAKS):
    if report_name[-3:] == 'txt':
        continue
    else:
        translate(report_name)
