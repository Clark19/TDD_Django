# 기능 테스트 파일
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time


class NewVisitorTest(LiveServerTestCase):

  def setUp(self):
    self.browser = webdriver.Firefox()
    self.browser.implicitly_wait(1)

  def tearDown(self) -> None:
    self.browser.quit()

  def check_for_row_in_list_table(self, row_text):
    table = self.browser.find_element_by_id('id_list_table')
    rows = table.find_elements_by_tag_name('tr')
    self.assertIn(row_text, [row.text for row in rows])

  def test_can_start_a_list_and_retrieve_it_later(self):
    # 유저는 작업 목록 웹서비스를 브라우저로 확인한다.
    self.browser.get(self.live_server_url)

    # 웹 페이지 타이틀과 헤더가 'To-Do'를 표시하고 있다.
    self.assertIn('To-Do', self.browser.title)
    header_text = self.browser.find_element_by_tag_name('h1').text
    self.assertIn('To-Do', header_text)

    # 그녀는 바로 작업을 추가하기로 한다
    inputbox = self.browser.find_element_by_id('id_new_item')
    self.assertEqual(inputbox.get_attribute('placeholder'), '작업 아이템 입력')
    
    # "공작깃털 사기"라고 텍스트 상자에 입력한다
		# (에디스의 취미는 날치 잡이용 그물을 만드는 것이다)
    inputbox.send_keys('공작깃털 사기')

		#엔터키를 치면 페이지가 갱신되고 작업 목록에
		# "1: 공작깃털 사기" 아이템이 추가된다
    inputbox.send_keys(Keys.ENTER)
    edith_list_url = self.browser.current_url
    self.assertRegex(edith_list_url, '/lists/.+')
    time.sleep(1)
    self.check_for_row_in_list_table('1: 공작깃털 사기')


		# 추가 아이템을 입력할 수 있는 여분의 텍스트 상자가 존재한다
		# 다시 "공작깃털을 사용해서 그물 만들기"라고 입력한다 (에디스는 매우 체계적인 사람이다)
    inputbox = self.browser.find_element_by_id('id_new_item')
    inputbox.send_keys('공작깃털을 이용해서 그물 만들기')
    inputbox.send_keys(Keys.ENTER)
    time.sleep(1)

		# 페이지는 다시 갱신되고, 2개 아이템이 목록에 보여진다
    self.check_for_row_in_list_table('2: 공작깃털을 이용해서 그물 만들기')
    self.check_for_row_in_list_table('1: 공작깃털 사기')

    # 새로운 사용자인 프란시스가 사이트에 접속한다.

    ## 새로운 브라우저 세션을 이용해서 에디스의 정보가
    ## 쿠키를 통해서 유입되는 것을 방지한다
    self.browser.quit()
    self.browser = webdriver.Firefox()

    # 프란시스가 홈페이지에 접속한다
    # 에디스의 리스트는 보이지 않는다.
    self.browser.get(self.live_server_url)
    page_text = self.browser.find_element_by_tag_name('body').text
    self.assertNotIn('공작깃털사기', page_text)
    self.assertNotIn('그물 만들기', page_text)

    # 프란시스가 새로운 작업 아이템을 입력하기 시작한다.
    # 그는 에디스보다 재미가 없다.
    inputbox = self.brwoser.find_elememt_by_id('id_new_item')
    inputbox.send_keys('우유 사기')
    inputbox.send_keys(Keys.ENTER)

    # 프란시스가 전용 url을 취득한다
    francis_list_url = self.browser.current_url
    self.assertRegex(francis_list_url, '/lists/.+')
    self.assertNotEqual(francis_list_url, edith_list_url)

    # 에디스가 입력한 흔적이 없다는 것을 다시 확인한다.
    page_text = self.browser.find_element_by_tag_name('body').text
    self.assertNotIn('공작깃털 사기', page_text)
    self.assertIn('우유 사기', page_text)

    # 둘 다 만족하고 잠자리에 든다    


		# 에디스는 사이트가 입력한 목록을 저장하고 있는지 궁금하다.
		# 사이트는 그녀를 위한 특정 URL을 생성해 준다.
		# 이때 URL에 대한 설명도 함께 제공된다.
		# 해당 URL에 접속하면 그녀가 만든 작업 목록이 그대로 있는 것을 확인할 수 있다.
		# 만족하고 잠자리에 든다.

    self.fail('Finish the test!')


# if __name__ == '__main__':
#   unittest.main(warnings='ignore')