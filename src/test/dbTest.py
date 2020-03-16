import unittest
import os
import sys
import traceback
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))) # 상위 경로 import 가능
import package.db as db

class DbTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(DbTest, self).__init__(*args, **kwargs)
        self.testRowName = "test"
        self.testRowText = "this is test"
        self.testRowTextUpdated = "this is test, Of Course!"
 
    def setUp(self):
        try:
            db.setup("db", "dbtest")
            print(os.path.abspath(os.path.dirname(__file__)))
        except Exception:
            print("!!! setup Method Exception !!!")
            traceback.print_exc(file=sys.stdout)
            print("!!! setup Method Exception !!!")
 
    def tearDown(self):
        try:
            db.disconnect()
            os.remove(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))), "db\\dbtest.db"))
        except Exception:
            print("!!! teardown Method Exception !!!")
            traceback.print_exc(file=sys.stdout)
            print("!!! teardown Method Exception !!!")
    
    def testAppend(self):
        print("@@ Append test... @@")
        print("post appending test...")
        db.appendPost(self.testRowName, self.testRowText)
        print("post append success!\n")
        print("getting post which appended...")
        res = db.getPost(self.testRowName)
        self.assertTrue(res is not None, "after append post, it should exists, but post is not exists.")
        print("post exists!")
        print("@@ Append test Success! @@", end="\n\n\n")
    
    def testUpdate(self):
        print("@@ update test... @@")
        print("post appending test...")
        db.appendPost(self.testRowName, self.testRowText)
        print("post append success!\n")
        print("post updating...")
        db.updatePost(self.testRowName, self.testRowTextUpdated)
        print("post updated!")
        print("Getting updated Post")
        res = db.getPost(self.testRowName)
        self.assertEqual(self.testRowTextUpdated, res[0])
        print("context equals!")
        print("@@ update test Success! @@", end="\n\n\n")
    
    def testDelete(self):
        print("@@ delete test... @@")
        print("post appending test...")
        db.appendPost(self.testRowName, self.testRowText)
        print("post append success!\n")
        print("post deleting...")
        db.deletePost(self.testRowName)
        res = db.getPost(self.testRowName)
        self.assertIsNone(res)
        print("post deleted!")
        print("@@ delete test Success! @@", end="\n\n\n")


 
if __name__ == '__main__':
    print("@@@ DB test Executing... @@@")
    unittest.main()
    print("@@@ DB test Success! @@@")