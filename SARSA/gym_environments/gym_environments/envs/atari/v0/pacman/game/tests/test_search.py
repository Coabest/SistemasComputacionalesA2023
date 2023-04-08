import unittest

from src import search


class StackTestCase(unittest.TestCase):
    def setUp(self):
        self.stack = search.Stack(5)
    
    def test_empty_stack(self):
        self.assertTrue(self.stack.is_empty())

    def test_take_from_emtpy_stack(self):
        with self.assertRaises(RuntimeError) as ex:
            self.stack.take()
        
        self.assertEqual(str(ex.exception), "Stack is empty")

    def test_add_elements(self):
        for i in range(5):
            self.stack.add(i)

        self.assertFalse(self.stack.is_empty())
        self.assertTrue(self.stack.is_full())

        with self.assertRaises(RuntimeError) as ex:
            self.stack.add(i)
        
        self.assertEqual(str(ex.exception), "Stack is full")
    
    def test_take_element(self):
        for i in range(3):
            self.stack.add(i)

        self.assertFalse(self.stack.is_empty())
        self.assertFalse(self.stack.is_full())
        self.assertEqual(self.stack.take(), 2)

    def test_add_remove_add(self):
        for i in range(4):
            self.stack.add(i)

        for _ in range(3):
            self.stack.take()

        for i in range(4):
            self.stack.add(i)
        
        self.assertEqual(self.stack.take(), 3)



class QueueTestCase(unittest.TestCase):
    def setUp(self):
        self.queue = search.Queue(5)
    
    def test_empty_queue(self):
        self.assertTrue(self.queue.is_empty())

    def test_take_from_emtpy_queue(self):
        with self.assertRaises(RuntimeError) as ex:
            self.queue.take()
        
        self.assertEqual(str(ex.exception), "Queue is empty")

    def test_add_elements(self):
        for i in range(5):
            self.queue.add(i)

        self.assertFalse(self.queue.is_empty())
        self.assertTrue(self.queue.is_full())

        with self.assertRaises(RuntimeError) as ex:
            self.queue.add(i)
        
        self.assertEqual(str(ex.exception), "Queue is full")

    def test_take_element(self):
        for i in range(3):
            self.queue.add(i)

        self.assertFalse(self.queue.is_empty())
        self.assertFalse(self.queue.is_full())
        self.assertEqual(self.queue.take(), 0)

    def test_add_remove_add(self):
        for i in range(5):
            self.queue.add(i)

        for _ in range(4):
            self.queue.take()

        for i in range(3):
            self.queue.add(i)
        
        self.assertEqual(self.queue.take(), 4)
