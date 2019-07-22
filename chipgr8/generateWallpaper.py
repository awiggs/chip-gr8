def getLines():
    f = open("./404.txt")
    lines = [line.rstrip("\n") for line in f]
    f.close()
    return lines
    
def initializeChunks():
    chunks = []
    for _ in range(8):
        chunks.append([])
    return chunks

def breakLinesIntoChunks(lines):
    chunks = initializeChunks()
    for line in lines:
        for x in range(8):
            chunks[x].append(line[x * 8 : x * 8 + 8])
    return chunks

def breakChunksIntoSprites(chunks):
    sprites = []
    for chunk in chunks:
        sprites.append(chunk[:15])
        sprites.append(chunk[15:30])
        sprites.append(chunk[30:])
    return sprites

def outPutSprites(sprites):
    f = open("output.txt", "w")
    for s in range(len(sprites)):
        f.write(".label_" + str(s) + "\n")
        for r in sprites[s]:
            f.write("BYTE 0b" + r + "\n")
        
def Main():
    lines = getLines()
    chunks = breakLinesIntoChunks(lines)
    sprites = breakChunksIntoSprites(chunks)
    outPutSprites(sprites)

Main()