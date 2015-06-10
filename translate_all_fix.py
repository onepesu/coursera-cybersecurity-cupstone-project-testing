import os
import settings
from translate_break_submission import translate

for report_name in os.listdir(settings.READ_TESTS):
    if report_name[-5:] != '.json':
        continue
    else:
        base_name = report_name[:-5]
        translate(base_name)
