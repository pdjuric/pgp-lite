
def open_child(parent, child):
    child.parent = parent
    child.show()
    parent.hide()

def lambda_w_capture(f, key_id):
    currId = key_id
    return lambda: f(currId)

def lambda_show(f):
    return lambda: f.show()

def back(t):
    t.parent.show()
    t.hide()
