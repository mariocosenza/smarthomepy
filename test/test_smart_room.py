import unittest
import mock.GPIO as GPIO
from unittest.mock import patch, PropertyMock
from unittest.mock import Mock

from mock.adafruit_bmp280 import Adafruit_BMP280_I2C
from src.smart_room import SmartRoom
from mock.senseair_s8 import SenseairS8


class TestSmartRoom(unittest.TestCase):

    @patch.object(GPIO, "input")
    def test_check_occupancy_occupied(self, mock_input: Mock):
        mock_input.return_value = True
        smart = SmartRoom()
        occupied = smart.check_room_occupancy()
        mock_input.assert_called_once_with(SmartRoom.INFRARED_PIN)
        self.assertTrue(occupied)

    @patch.object(GPIO, "input")
    def test_check_occupancy_empty(self, mock_input: Mock):
        mock_input.return_value = False
        smart = SmartRoom()
        occupied = smart.check_room_occupancy()
        mock_input.assert_called_once_with(SmartRoom.INFRARED_PIN)
        self.assertFalse(occupied)

    @patch.object(GPIO, "input")
    def test_check_enough_light_bright(self, mock_input: Mock):
        mock_input.return_value = True
        smart = SmartRoom()
        occupied = smart.check_enough_light()
        mock_input.assert_called_once_with(SmartRoom.PHOTO_PIN)
        self.assertTrue(occupied)

    @patch.object(GPIO, "input")
    def test_check_enough_light_dark(self, mock_input: Mock):
        mock_input.return_value = False
        smart = SmartRoom()
        occupied = smart.check_enough_light()
        mock_input.assert_called_once_with(SmartRoom.PHOTO_PIN)
        self.assertFalse(occupied)


    @patch.object(SmartRoom, "check_enough_light")
    @patch.object(SmartRoom, "check_room_occupancy")
    @patch.object(GPIO, "output")
    def test_manage_light_level_person_inside_room_few_light(self, output: Mock, check_occupancy: Mock, check_enough_light: Mock):
        check_enough_light.return_value = False
        check_occupancy.return_value = True
        smart = SmartRoom()
        smart.manage_light_level()
        output.assert_called_once_with(SmartRoom.LED_PIN, True)
        self.assertTrue(smart.light_on)


    @patch.object(SmartRoom, "check_enough_light")
    @patch.object(SmartRoom, "check_room_occupancy")
    @patch.object(GPIO, "output")
    def test_manage_light_level_no_person_inside_room_enough_light(self, output: Mock, check_occupancy: Mock, check_enough_light: Mock):
        check_enough_light.return_value = True
        check_occupancy.return_value = False
        smart = SmartRoom()
        smart.manage_light_level()
        output.assert_called_once_with(SmartRoom.LED_PIN, False)
        self.assertFalse(smart.light_on)