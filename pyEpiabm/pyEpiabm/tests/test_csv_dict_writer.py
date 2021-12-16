import unittest
import pyEpiabm as pe
from unittest.mock import patch, mock_open, call, MagicMock


class TestCsvDictWriter(unittest.TestCase):
    """Test the three methods of the '_CsvDictWriter' class.
    """

    def test_init(self):
        """Test the __init__ method of the _CsvDictWriter class.
        """
        mo = mock_open()
        with patch('pyEpiabm._csv_dict_writer.open', mo):
            mock_categories = ['Cat1', 'Cat2', 'Cat3']
            m = pe._CsvDictWriter('mock_filename', mock_categories)
            del(m)
        mo.assert_called_once_with('mock_filename', 'w')
        mo().write.assert_called_once_with('Cat1,Cat2,Cat3\r\n')

    def test_write(self):
        """Test the write method of the _CsvDictWriter class.
        """
        mo = mock_open()
        with patch('pyEpiabm._csv_dict_writer.open', mo):
            mock_categories = ['Cat1', 'Cat2', 'Cat3']
            new_content = {'Cat1': 'a', 'Cat3': 'c', 'Cat2': 'b'}
            m = pe._CsvDictWriter('mock_filename', mock_categories)
            m.write(new_content)
        mo().write.assert_has_calls([call('Cat1,Cat2,Cat3\r\n'),
                                    call('a,b,c\r\n')])

    def test_del(self):
        """Test the __del__ method of the _CsvDictWriter class.
        """
        fake_file = MagicMock()
        with patch("builtins.open", return_value=fake_file, create=True):
            mock_content = ['1', '2', '3']
            m = pe._CsvDictWriter('mock_filename', mock_content)
            m.__del__()
            fake_file.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
