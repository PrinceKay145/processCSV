import pytest
from unittest.mock import patch, mock_open
from main import parse_condition, apply_filter, compute_aggregate, process_csv

class TestCSVProcessing:
    def setup_method(self):
        self.test_data = [
            {'id': '1', 'price':'100', 'name':'product1'},
            {'id': '2', 'price':'200', 'name':'product2'},
            {'id': '3', 'price':'150', 'name':'product3'},
            {'id': '4', 'price':'50', 'name':'product4'},
        ]
        self.headers = ['id', 'price', 'name']
    def test_parse_condition(self):
        """Test parsing of condition strings"""
        assert parse_condition('price>100') == ('price','>','100')
        assert parse_condition('name=product2') == ('name', '=', 'product2')
        assert parse_condition('id<4') == ('id', '<', '4')
    
    def test_apply_filter(self):
        """Test filtering of data"""
        #test numerical comparison
        filtered = apply_filter(self.test_data, 'price>100', self.headers)
        assert len(filtered) == 2
        assert {'id': '2', 'price': '200', 'name': 'product2'} in filtered
        assert {'id': '3', 'price': '150', 'name': 'product3'} in filtered

        #test string comparison
        filtered = apply_filter(self.test_data, 'name=product2', self.headers)
        assert len(filtered) == 1
        assert filtered[0] == {'id':'2', 'price':'200','name':'product2'}

    def test_compute_aggregate(self):
        #test max
        result = compute_aggregate(self.test_data, 'price', 'max', self.headers)
        assert result == 200.0

        #test avg
        result = compute_aggregate(self.test_data, 'price', 'avg', self.headers)
        assert result == 125.0

        #test min
        result = compute_aggregate(self.test_data, 'price', 'min', self.headers)
        assert result == 50.0

    @patch('builtins.open', create=True) #@todo find out why this is important
    def test_process_csv(self, mock_open):
        """Test complete CSV processing"""
        mock_file = mock_open.return_value.__enter__.return_value
        mock_file.__iter__.return_value = iter([
            'id,price,name',
            '1,100,product1',
            '2,200, product2'
            ]) 
        result = process_csv('test.csv', 'price>150')
        assert 'product2' in result
        
    @patch('builtins.open', create=True) 
    def test_process_csv_aggregate(self, mock_open):
        """Test complete CSV processing"""
        mock_file = mock_open.return_value.__enter__.return_value
        mock_file.__iter__.return_value = iter([
            'id,price,name',
            '1,100,product1',
            '2,200, product2'
            ])   
        result = process_csv('test.csv', aggregate='price=avg')
        assert '150' in result
    
    @patch('builtins.open', create=True) 
    def test_process_csv_filter_aggregate(self, mock_open):
        """Test complete CSV processing"""
        mock_file = mock_open.return_value.__enter__.return_value
        mock_file.__iter__.return_value = iter([
            'id,price,name',
            '1,100,product1',
            '2,200, product2'
            ])   
        result = process_csv('test.csv', condition='price>150', aggregate='price=max')
        assert '200' in result

if __name__ == '__main__':
    pytest.main(['test_main.py', '-v', '--cov=main'])

