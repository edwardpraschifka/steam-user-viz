from main import bfs

def simulate_api(user_id):
    """
    simulate_api simulates the following relationship graph:

    Fred - Alice -   Bob
    |        \\        \\
    Bill     Jones -  Alex -  Ron
               |
              Dave
    
    layer 1: Alice
    layer 2: Fred, Jones, Bob
    layer 3: Bill, Alex, Dave
    layer 4: Ron
    """

    match user_id:
        case "Alice":
            return {"Bob", "Jones", "Fred"}
        case "Bob":
            return {"Alice", "Alex"}
        case "Fred":
            return {"Alice", "Bill"}
        case "Jones":
            return {"Alice", "Alex", "Dave"}
        case "Bill":
            return {"Fred"}
        case "Dave":
            return {"Jones"}
        case "Alex":
            return {"Jones", "Bob", "Ron"}
        case "Ron":
            return {"Alex"}
        case _:
            return []


def test_bfs_depth_one():
    id_to_friends = bfs("Alice", depth=1, get_friends_func=simulate_api)
    assert id_to_friends["Alice"] == {"Bob", "Jones", "Fred"}
    
def test_bfs_depth_two():
    id_to_friends = bfs("Alice", depth=2, get_friends_func=simulate_api)
    assert id_to_friends["Bob"] == {"Alice", "Alex"}
    assert id_to_friends["Jones"] == {"Alice", "Alex", "Dave"}
    assert id_to_friends["Fred"] == {"Alice", "Bill"}


def test_bfs_depth_three():
    id_to_friends = bfs("Alice", depth=3, get_friends_func=simulate_api)
    assert id_to_friends["Bill"] == {"Fred"}
    assert id_to_friends["Alex"] == {"Jones", "Bob", "Ron"}
    assert id_to_friends["Dave"] == {"Jones"}
    

def test_bfs_depth_four():
    id_to_friends = bfs("Alice", depth=4, get_friends_func=simulate_api)
    assert id_to_friends["Ron"] == {"Alex"}