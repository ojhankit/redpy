from datastore import datastore

def parse_commands(command:str):
    " Take input a command and Parse the command and excutes method "
    tokens = command.strip().split()

    if not tokens:
        return "ERROR: Empty command"
    
    cmd = tokens[0]

    if cmd == "SET":
        if len(tokens) != 3:
            return "ERROR: Usage SET key value"
        key ,value = tokens[1] ,tokens[2]
        datastore[key] = value
        return "OK"

    elif cmd == "GET":
        if len(tokens) != 2:
            return "ERROR: Usage GET key"
        key = tokens[1]
        return datastore.get(key,"(nil)")
    
    else:
        return f"ERROR: Unknown command {cmd}"