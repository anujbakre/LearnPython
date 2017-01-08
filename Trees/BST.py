import random


class BS_Tree():
    def __init__(self, data = None):
        self.right = self.left = None
        self.data = data
        self.node_count = 0

    def insert(self,root,data):
        if root ==  None:
            self.node_count += 1
            return BS_Tree(data)

        elif root.data > data:
            cur = self.insert(root.left, data)
            root.left = cur
        else:
            cur = self.insert(root.right, data)
            root.right = cur
        return root


    def get_node_count(self,root):
        return self.node_count

    def get_height(self,root):
        if root:
            return 1 + max(self.get_height(root.left), self.get_height(root.right))
        else:
            return 0


    def inorder_traversal(self,root):
        if root:
            self.inorder_traversal(root.left)
            print(root.data, end= " ")
            self.inorder_traversal(root.right)

    def preorder_traversal(self,root):
        if root:
            print(root.data, end= " ")
            self.preorder_traversal(root.left)
            self.preorder_traversal(root.right)

    def postorder_traversal(self,root):
        #depth first search
        if root:
            self.postorder_traversal(root.left)
            self.postorder_traversal(root.right)
            print(root.data, end= " ")

    def levelorder_traversal(self,root):
        #Breadth first search
        q = [root] if root else []

        while q:
            node = q.pop()
            print(node.data, end=" ")

            if node.left : self.levelorder_traversal(node.left)
            if node.right : self.levelorder_traversal(node.right)


    def min_value(self,root):
        if root:
            while root.left: root = root.left
            return root.data

    def find(self,root, to_find):
        if root == None:
            return False
        elif root.data == to_find:
            return True
        elif root.data > to_find:
            return self.find(root.left, to_find)
        else:
            return self.find(root.right, to_find)


    def all_paths(self,root, node_list):


        if root is None:
            return
        node_list.append(root)

        if root.right is None and root.left is None:
            for x in node_list: print(x.data, end = " ")
            print()
        else:
            self.all_paths(root.left,node_list)
            self.all_paths(root.right,node_list)










def main():
    # code to test BST
    my_tree = BS_Tree()
    root  = None


    #create BST from random data
    rand = random.randrange(0,20)
    x = random.sample(range(-100,100),k=rand)
    print("Data to be inserted:",*x)

    for num in x:
       root =  my_tree.insert(root,num)


    #print Inorder
    print("Inorder")
    my_tree.inorder_traversal(root)

    #print postorder
    print("\nPostorder")
    my_tree.postorder_traversal(root)

    #print preorder
    print("\nPreorder")
    my_tree.preorder_traversal(root)

    #print levelorder
    print("\nLevelorder")
    my_tree.levelorder_traversal(root)

    #number of nodes
    count = my_tree.get_node_count(root)
    print("\nNumber of nodes:",count)

    #height of tree
    height = my_tree.get_height(root)
    print("Height of tree:",height)

    #min value
    minimum = my_tree.min_value(root)
    print(minimum)

    #find a number
    if my_tree.find(root, x[rand - 1]):
        print("Number",x[rand - 1],"Found")
    else:
        print("Number",x[rand - 1],"not Found")

    if my_tree.find(root,200):
        print("Number 200 Found")
    else:
        print("Number 200 not Found")


    # print all paths
    node_list = []
    my_tree.all_paths(root, node_list)

if __name__ == '__main__':
    main()


