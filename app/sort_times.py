
class TreeNode:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

class BST:
    INITIAL_DATA = None
    SORTED_DATA = None
    def __init__(self, data: list) -> None:
        self.INITIAL_DATA = data

    def __insert(self, root, key) -> TreeNode:
        if root is None:
            return TreeNode(key)
        _root = root.val.time.timestamp()
        _key = key.time.timestamp()
        # key > root, to get the date desc or key < root
        if _key > _root:
            root.left = self.__insert(root.left, key)
        else:
            root.right = self.__insert(root.right, key)
        
        return root

    def __inorder_traversal(self, root, res) -> None:
        if root:
            self.__inorder_traversal(root.left, res)
            res.append(root.val)
            self.__inorder_traversal(root.right, res)

    def sort(self) -> None:
        if not self.INITIAL_DATA:
            return self.INITIAL_DATA
        
        root = None
        for key in self.INITIAL_DATA:
            root = self.__insert(root, key)
        
        sorted_arr = []
        self.__inorder_traversal(root, sorted_arr)
        self.SORTED_DATA = sorted_arr