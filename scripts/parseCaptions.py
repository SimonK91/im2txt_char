def parseCaptions(filename):
    retVal = []
    with open(filename, 'r') as f:
        for line in f.read().split("\n"):
            if ("Captions for image" in line):
                image = line[19:-1]
                #print("\""+image+"\"")
            if ("  0)" in line):
                best = line[5:-13]
                #print("\""+best+"\"")
                retVal.append((image, best))
            #print(line)
            #time.sleep(1)
    return retVal
