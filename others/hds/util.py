from gsheet_func import get_indi_urls, write_view_heart_num
from others.hds.indi_job import work


urls = get_indi_urls()
view_nums, heart_nums = work(urls)
write_view_heart_num(view_nums, input_type="view")
write_view_heart_num(heart_nums, input_type="heart")