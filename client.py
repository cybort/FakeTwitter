import json
import server

def request(site, head, body):
    data = server.blocking_req(site.addr, site.port, json.dumps({"head": head, "body": body}))
    return data

def init(node, sites):
    my_site = sites[node]
    print "Welcom user \"%s\", Node(SID): %d, Addr: %s:%d"%(my_site.name, my_site.node, my_site.addr, my_site.port)
    print "Global Tweeter users:",
    for site in sites:
        print "\"" + site.name + "\"",
    print "\nType 'tweet <message>', 'block/unblock <username>', 'view' and 'Ctrl-c' to terminate:"
    while True:
        command = raw_input(my_site.name + "> ")
        if command.startswith("tweet "):
            message = command[6:]
            print "Sending Tweet: \"" + message + "\""
            print request(my_site, "tweet", message)
        elif command.startswith("block "):
            toblock = command[6:]
            print "Blocking user: \"" + toblock + "\""
            print request(my_site, "block", toblock)
        elif command.startswith("unblock "):
            tounblock = command[8:]
            print "Unblocking user: \"" + tounblock + "\""
            print request(my_site, "unblock", tounblock)
        elif command == "view":
            resp = json.loads(request(my_site, "view", ""))
            if resp['stat'] == 200:
                print "Tweet list: "
                for tweet in json.loads(resp['body']):
                    print "@" + tweet[0] + " " + tweet[2].split(".")[0].replace("T", " ") + "\n" + tweet[1]
        else:
            print "Invalid command! Usage:"
            print "tweet <message> - tweet a message"
            print "block <username> - block a user by user name"
            print "unblock <username> - unblock a user by user name"
            print "view - view the timeline"