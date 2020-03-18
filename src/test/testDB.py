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
            os.remove(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))), "db/dbtest.db"))
        except Exception:
            print("!!! teardown Method Exception !!!")
            traceback.print_exc(file=sys.stdout)
            print("!!! teardown Method Exception !!!")
    
    def testPostAppend(self):
        print("@@ Append test... @@")
        print("post appending test...")
        db.appendPost(self.testRowName, str(557197552336896010), self.testRowText)
        print("post append success!\n")
        print("getting post which appended...")
        res = db.getPostByName(self.testRowName)
        self.assertTrue(res, "after append post, it should exists, but post is not exists.")
        print("post exists!")
        print("@@ Append test Success! @@", end="\n\n\n")
    
    def testPostUpdate(self):
        print("@@ update test... @@")
        print("post appending test...")
        db.appendPost(self.testRowName, str(557197552336896010), self.testRowText)
        print("post append success!\n")
        print("post updating...")
        db.updatePost(self.testRowName, self.testRowTextUpdated)
        print("post updated!")
        print("Getting updated Post")
        res = db.getPostByName(self.testRowName)
        self.assertEqual(self.testRowTextUpdated, res[2])
        print("context equals!")
        print("@@ update test Success! @@", end="\n\n\n")
    
    def testPostDelete(self):
        print("@@ delete test... @@")
        print("tag appending test...")
        db.appendPost(self.testRowName, str(557197552336896010), self.testRowText)
        print("tag append success!\n")
        print("tag deleting...")
        db.deletePost(self.testRowName)
        res = db.getPostByName(self.testRowName)
        self.assertIsNone(res)
        print("tag deleted!")
        print("@@ delete test Success! @@", end="\n\n\n")

    def testTagAppend(self):
        print("@@ Append test... @@")
        print("tag appending test...")
        db.appendTag(self.testRowName, str(557197552336896010), self.testRowText)
        print("tag append success!\n")
        print("getting tag which appended...")
        res = db.getTagByName(self.testRowName)
        self.assertTrue(res, "after append tag, it should exists, but tag is not exists.")
        print("tag exists!")
        print("@@ Append test Success! @@", end="\n\n\n")
    
    def testTagUpdate(self):
        print("@@ update test... @@")
        print("tag appending test...")
        db.appendTag(self.testRowName, str(557197552336896010), self.testRowText)
        print("tag append success!\n")
        print("tag updating...")
        db.updateTag(self.testRowName, self.testRowTextUpdated)
        print("tag updated!")
        print("Getting updated Tag")
        res = db.getTagByName(self.testRowName)
        self.assertEqual(self.testRowTextUpdated, res[2])
        print("context equals!")
        print("@@ update test Success! @@", end="\n\n\n")
    
    def testTagDelete(self):
        print("@@ delete test... @@")
        print("tag appending test...")
        db.appendTag(self.testRowName, str(557197552336896010), self.testRowText)
        print("tag append success!\n")
        print("tag deleting...")
        db.deleteTag(self.testRowName)
        res = db.getTagByName(self.testRowName)
        self.assertIsNone(res)
        print("tag deleted!")
        print("@@ delete test Success! @@", end="\n\n\n")


 
if __name__ == '__main__':
    print("@@@ DB test Executing... @@@")
    unittest.main()
    print("@@@ DB test Success! @@@")