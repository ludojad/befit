__author__ = 'p.slodkiewicz@gmail.com'
__name__ = 'befitSheduller'
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import datetime
import time
import logging
import ConfigParser

PROP_FILE = 'befitSheduller.properties'
LOG_FILE = 'befitSheduller.log'
logging.basicConfig(filename=LOG_FILE,
                    level=logging.INFO,
                    datefmt='%A-%m-%d %H:%M',
                    format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger(__name__)
config = ConfigParser.RawConfigParser()
config.read(PROP_FILE)
isWorkoutAlredySigned = False


class Scheduller:
    def __init__(self):
        pass

    def getNowDayName(self):
        return datetime.date.today().strftime("%A")

    def getWorkoutDayName(self):
        sign_day = datetime.date.today() + datetime.timedelta(days=3)
        return sign_day.strftime("%A")

    def getTrTableWorkout(self, workout_day_name):
        try:
            return config.get('app', workout_day_name).split(';')[0]
        except ConfigParser.NoOptionError:
            return log.debug('No workouts to sign today ...')

    def getTdTableWorkout(self, workout_day_name):
        try:
            return config.get('app', workout_day_name).split(';')[1]
        except ConfigParser.NoOptionError:
            return log.debug('No workouts to sign today ...')

    def isWorkoutInSchedule(self, workout_day_name):
        try:
            config.get('app', workout_day_name)
            return True
        except ConfigParser.NoOptionError:
            log.debug('No workouts to sign today ...')
            return False


class Selenium:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(5)
        self.base_url = "https://befit-cms.efitness.com.pl/"
        self.verificationErrors = []
        self.accept_next_alert = True
        pass

    def sign_to_workout(self):
        scheduler = Scheduller()
        tr = scheduler.getTrTableWorkout(scheduler.getWorkoutDayName())
        td = scheduler.getTdTableWorkout(scheduler.getWorkoutDayName())

        driver = self.driver
        driver.get(self.base_url + "/kalendarz-zajec")
        driver.find_element_by_id("loginmenu_log_in").click()
        driver.find_element_by_id("Login").clear()
        driver.find_element_by_id("Login").send_keys(config.get('auth', 'pesel'))
        driver.find_element_by_id("Password").clear()
        driver.find_element_by_id("Password").send_keys(config.get('auth', 'password'))
        driver.find_element_by_id("SubmitCredentials").click()

        if scheduler.getNowDayName() in ('Friday', 'Saturday', 'Sunday'):
            driver.find_element_by_css_selector("div.week_chooser > a.right").click()

        try:
            driver.find_element_by_xpath(
                '//*[@id=\"scheduler\"]/div[1]/table/tbody/tr[{0}]/td[{1}]/div/p[1]'.format(str(tr), str(td))).click()
            driver.find_element_by_xpath('//*[@id="calendar-register-for-class"]').click()
            log.info(scheduler.getWorkoutDayName() + ' workout sign succeed :)')
        except NoSuchElementException:
            global isWorkoutAlredySigned
            isWorkoutAlredySigned = True
            log.info(scheduler.getWorkoutDayName() + ' workout allready signed ...')
        driver.quit()
        return None


log.info('Befit scheduller started')
while True:
    with open(LOG_FILE, 'a') as f:
        f.write('.')
    Now = datetime.date.today().strftime("%A")
    tries = 5
    time.sleep(120)
    if Now != datetime.date.today().strftime("%A"):
        s = Scheduller()
        if s.isWorkoutInSchedule(s.getWorkoutDayName()):
            for i in range(0, tries):
                if isWorkoutAlredySigned:
                    tries = 0
                else:
                    selenium = Selenium()
                    selenium.sign_to_workout()
                    tries -= 1