__author__ = 'p.slodkiewicz@gmail.com'
__name__ = 'befitScheduler'
from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.common.exceptions import NoSuchElementException
import datetime
import time
import logging
import ConfigParser

PROP_FILE = 'befitScheduler.properties'
LOG_FILE = 'befitScheduler.log'
logging.basicConfig(filename=LOG_FILE,
                    level=logging.INFO,
                    datefmt='%A-%m-%d %H:%M:%S',
                    format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger(__name__)
config = ConfigParser.RawConfigParser()
config.read(PROP_FILE)


class Scheduller:
    def __init__(self):
        pass

    def getNowDayName(self):
        return datetime.date.today().strftime("%A")

    def getWorkoutDayName(self):
        sign_day = datetime.date.today() + datetime.timedelta(days=5)
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
            return log.info('No workouts to sign today ...')

    def isWorkoutInSchedule(self, workout_day_name):
        try:
            config.get('app', workout_day_name)
            return True
        except ConfigParser.NoOptionError:
            log.info('No workouts to sign today ...')
            return False


class Selenium:
    def __init__(self):

        display = Display(visible=0, size=(1024, 768))
        display.start()

        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)
        self.driver.set_page_load_timeout(30)
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

        if scheduler.getNowDayName() in ('Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'):
            driver.find_element_by_css_selector("div.week_chooser > a.right").click()

        try:
            driver.find_element_by_xpath(
                '//*[@id=\"scheduler\"]/div[1]/table/tbody/tr[{0}]/td[{1}]/div/p[1]'.format(str(tr), str(td))).click()
            driver.find_element_by_xpath('//*[@id="calendar-register-for-class"]').click()
            log.info(scheduler.getWorkoutDayName() + ' workout sign succeed :)')
            return True
        except NoSuchElementException:
            return False
        driver.quit()


log.info('Befit scheduller started')

while True:
    isWorkoutAlredySigned = False
    Now = datetime.date.today().strftime("%A")
    time.sleep(float(config.get('conf', 'interval')))
    if Now == datetime.date.today().strftime("%A"):
        log.info('Day changed, looking for workouts')
        s = Scheduller()
        if s.isWorkoutInSchedule(s.getWorkoutDayName()):
            for i in range(0, 5):
                if isWorkoutAlredySigned:
                    break
                else:
                    try:
                        log.info('Starting selenium')
                        selenium = Selenium()
                        isWorkoutAlredySigned = selenium.sign_to_workout()
                    except Exception:
                        time.sleep(float(config.get('conf', 'interval')))