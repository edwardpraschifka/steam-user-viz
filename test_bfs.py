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
            return [{"steamid": "Bob", "relationship": ..., "friend_since": ...},
                    {"steamid": "Jones", "relationship": ..., "friend_since": ...},
                    {"steamid": "Fred", "relationship": ..., "friend_since": ...},]
        
        case "Bob":
            return [{"steamid": "Alice", "relationship": ..., "friend_since": ...},
                    {"steamid": "Alex", "relationship": ..., "friend_since": ...}]

        case "Fred":
            return [{"steamid": "Alice", "relationship": ..., "friend_since": ...},
                    {"steamid": "Bill", "relationship": ..., "friend_since": ...}]

        case "Jones":
            return [{"steamid": "Alice", "relationship": ..., "friend_since": ...},
                    {"steamid": "Alex", "relationship": ..., "friend_since": ...},
                    {"steamid": "Dave", "relationship": ..., "friend_since": ...}]

        case "Bill":
            return [{"steamid": "Fred", "relationship": ..., "friend_since": ...}]

        case "Dave":
            return [{"steamid": "Jones", "relationship": ..., "friend_since": ...}]

        case "Alex":
            return [{"steamid": "Jones", "relationship": ..., "friend_since": ...},
                    {"steamid": "Bob", "relationship": ..., "friend_since": ...},
                    {"steamid": "Ron", "relationship": ..., "friend_since": ...}]

        case "Ron":
            return [{"steamid": "Alex", "relationship": ..., "friend_since": ...}]
        
        case _:
            return []


def test_bfs_depth_one():
    out = bfs("Alice", depth=1, process=simulate_api)
    assert len(out["Alice"]) == 3
    assert len(out.keys()) == 1
    
def test_bfs_depth_two():
    out = bfs("Alice", depth=2, process=simulate_api)
    assert len(out["Fred"]) == 2
    assert len(out["Jones"]) == 3
    assert len(out["Bob"]) == 2
    assert len(out.keys()) == 4

def test_bfs_depth_three():
    out = bfs("Alice", depth=3, process=simulate_api)
    assert len(out["Bill"]) == 1
    assert len(out["Dave"]) == 1
    assert len(out["Alex"]) == 3
    assert len(out.keys()) == 7

def test_bfs_depth_four():
    out = bfs("Alice", depth=4, process=simulate_api)
    assert len(out["Ron"]) == 1
    assert len(out.keys()) == 8