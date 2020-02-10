from django.test import TestCase

# Create your tests here.
from system.mappers import Dict_mapper


class systemTest(TestCase):
    def setUp(self):
        '''测试函数执行前执行'''
        pass


    def testDemo(self):
        Dict_mapper.insert(type="test",key="test",value="Test",valid=0)



    def tearDown(self):
        '''测试函数执行后执行'''
        pass