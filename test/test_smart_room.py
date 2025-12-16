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